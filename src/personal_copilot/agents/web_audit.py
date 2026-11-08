"""
Generic Web & UI Audit Subagent (`src/personal_copilot/agents/web_audit.py`)
Modular, project-agnostic Gatekeeper for inspecting any web interface (HTML/CSS/JS/React/Vue):
- Auto-discovers views and hash routes from the DOM/bundle or accepts custom view definitions.
- Captures high-resolution visual PNG snapshots via headless Chrome or Edge.
- Probes dynamic live servers or falls back gracefully to local file:// URI.
- Supports optional project-specific DOM container assertions and design token verifications.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
from pathlib import Path
from typing import Any, Callable

from personal_copilot.config import SNAPSHOTS_DIR


class WebAuditSubagent:
    """Project-Agnostic Gatekeeper & Inspector Subagent for Web Interfaces and UI Views."""

    def __init__(self, name: str = "WebAuditSubagent") -> None:
        self.name = name

    def audit_html_file(
        self,
        html_path: Path,
        project_name: str | None = None,
        views: list[tuple[str, str]] | None = None,
        required_containers: list[tuple[str, str]] | None = None,
        design_tokens: dict[str, str] | None = None,
        live_server_url: str | None = None,
        data_verifier: Callable[[], dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        """
        Audits an HTML file for DOM integrity, design system conformance, and state readiness.
        Fully generic across any project in AI_Engineer.
        """
        if not html_path.exists():
            return {
                "gate": "WebAudit (UI Gate)",
                "passed": False,
                "error": f"Target HTML file does not exist: {html_path}",
                "metrics": {},
            }

        content = html_path.read_text(encoding="utf-8")

        # Infer project name dynamically if not explicitly provided
        proj_name = project_name
        if not proj_name:
            parts = html_path.resolve().parts
            if "Project" in parts:
                idx = parts.index("Project")
                if idx + 1 < len(parts):
                    proj_name = parts[idx + 1]
            if not proj_name:
                proj_name = html_path.stem

        # Include bundled assets (JS/CSS) if present in parent or adjacent assets directory
        bundle_text = content
        assets_dir = html_path.parent / "assets"
        if assets_dir.exists():
            for asset in assets_dir.glob("*.*"):
                try:
                    bundle_text += "\n" + asset.read_text(encoding="utf-8")
                except Exception:
                    pass

        issues: list[str] = []
        checks_passed: list[str] = []

        # 1. Generic DOM Health Check
        if not content.strip():
            issues.append("Critical: HTML file is completely empty")
        elif "<body" in content.lower():
            checks_passed.append("Valid HTML5 document structure with <body> present")

        # Check for mount roots (React, Vue, or static main)
        has_mount_root = any(k in bundle_text for k in ['id="root"', 'id="app"', '<main', 'class="container"'])
        if has_mount_root:
            checks_passed.append("Application mount container (<main>, #root, or #app) present")

        # 2. Design Token Verification (Optional - only verified if provided)
        if design_tokens:
            for token_name, token_val in design_tokens.items():
                if token_val in bundle_text:
                    checks_passed.append(f"Design token [{token_name}: {token_val}] verified")
                else:
                    issues.append(f"Warning: Design token '{token_name}: {token_val}' not detected in styles")

        # 3. DOM Container Checks (Optional - verified if provided)
        if required_containers:
            for elem_id, label in required_containers:
                if f'id="{elem_id}"' in bundle_text or f"id='{elem_id}'" in bundle_text or f'"{elem_id}"' in bundle_text:
                    checks_passed.append(f"DOM Container [{elem_id}] ({label}) present")
                else:
                    issues.append(f"Critical DOM container missing: #{elem_id} ({label})")

        # 4. Optional Data Layer Verification (via callback if provided)
        payload_stats: dict[str, Any] = {}
        if data_verifier and callable(data_verifier):
            try:
                payload_stats = data_verifier()
                checks_passed.append("External data layer verified successfully")
            except Exception as e:
                issues.append(f"Data layer verifier reported error: {e}")

        # 5. Table / Container Scroll styling check (if tables exist)
        if "<table" in bundle_text or "table" in bundle_text.lower():
            if any(k in bundle_text for k in ["overflow-y: auto", "overflow-y:auto", "overflow-x:auto", "overflow-x: auto", "overflow-auto"]):
                checks_passed.append("Scrollable container wrapper verified for tabular views")

        passed = len([i for i in issues if "Critical" in i]) == 0

        # 6. Capture Visual Screenshots dynamically
        snapshots_captured = self.capture_all_view_snapshots(
            html_path=html_path,
            views=views,
            subfolder=proj_name,
            live_server_url=live_server_url,
        )
        if snapshots_captured:
            for s in snapshots_captured:
                checks_passed.append(f"Visual UI snapshot captured: {s.name}")

        return {
            "gate": "WebAudit (UI Gate)",
            "passed": passed,
            "project": proj_name,
            "target_file": str(html_path),
            "file_size_kb": round(len(content.encode("utf-8")) / 1024, 2),
            "visual_snapshots": [str(s) for s in snapshots_captured],
            "checks_passed": checks_passed,
            "issues": issues,
            "state_snapshot": payload_stats,
        }

    def discover_views_from_bundle(self, html_path: Path, bundle_text: str) -> list[tuple[str, str]]:
        """
        Dynamically discovers tab routes and hash anchors from the HTML or JS bundle.
        Falls back to a single primary overview snapshot if no tabs exist.
        """
        views: list[tuple[str, str]] = []
        stem = html_path.stem

        # Primary overview view
        views.append((f"{stem}_overview.png", ""))

        # Discover hash routes from anchors, buttons, or window.location.hash
        discovered_hashes: set[str] = set()

        for match in re.findall(r'href=["\']#([a-zA-Z0-9_-]+)["\']', bundle_text):
            if match and len(match) > 1:
                discovered_hashes.add(match)

        for match in re.findall(r'window\.location\.hash\s*=\s*["\']#?([a-zA-Z0-9_-]+)["\']', bundle_text):
            if match and len(match) > 1:
                discovered_hashes.add(match)

        for match in re.findall(r'id:\s*["\']([a-zA-Z0-9_-]+)["\'],\s*label:', bundle_text):
            if match and len(match) > 1:
                discovered_hashes.add(match)

        for h in sorted(discovered_hashes):
            views.append((f"{stem}_view_{h}.png", f"#{h}"))

        return views

    def capture_all_view_snapshots(
        self,
        html_path: Path,
        views: list[tuple[str, str]] | None = None,
        subfolder: str | None = None,
        live_server_url: str | None = None,
    ) -> list[Path]:
        """
        Captures visual screenshots for all views (dynamically discovered or explicitly configured).
        Works seamlessly for ANY web project.
        """
        if views is None:
            content = html_path.read_text(encoding="utf-8") if html_path.exists() else ""
            assets_dir = html_path.parent / "assets"
            if assets_dir.exists():
                for asset in assets_dir.glob("*.js"):
                    try:
                        content += "\n" + asset.read_text(encoding="utf-8")
                    except Exception:
                        pass
            views = self.discover_views_from_bundle(html_path, content)

        results: list[Path] = []
        for filename, hash_suffix in views:
            res = self.capture_visual_screenshot(
                html_path,
                output_name=filename,
                hash_suffix=hash_suffix,
                subfolder=subfolder,
                live_server_url=live_server_url,
            )
            if res:
                results.append(res)
        return results

    def capture_visual_screenshot(
        self,
        html_path: Path,
        output_name: str | None = None,
        hash_suffix: str = "",
        subfolder: str | None = None,
        live_server_url: str | None = None,
    ) -> Path | None:
        """
        Captures a real visual PNG screenshot of the interface using headless Chrome or Edge.
        Targets live server URL if active, with graceful fallback to local file:// URI.
        Saved in `data/snapshots/{subfolder}/`.
        """
        folder_name = subfolder or html_path.stem
        target_dir = SNAPSHOTS_DIR / folder_name if folder_name else SNAPSHOTS_DIR
        target_dir.mkdir(parents=True, exist_ok=True)
        out_filename = output_name or f"{html_path.stem}_snapshot.png"
        out_path = target_dir / out_filename

        candidates = [
            Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
            Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
            Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
        ]
        browser_exe = next((p for p in candidates if p.exists()), None)
        if not browser_exe:
            return None

        # Resolve target URL: use live server URL if specified and reachable, otherwise fall back to local file URI
        target_url: str | None = None
        if live_server_url:
            import urllib.request
            try:
                urllib.request.urlopen(live_server_url, timeout=0.8)
                target_url = live_server_url.rstrip("/") + hash_suffix
            except Exception:
                pass

        if not target_url:
            target_url = html_path.resolve().as_uri() + hash_suffix

        try:
            cmd = [
                str(browser_exe),
                "--headless=new",
                "--disable-gpu",
                "--window-size=1280,800",
                "--virtual-time-budget=3000",
                f"--screenshot={out_path}",
                target_url,
            ]
            subprocess.run(cmd, capture_output=True, timeout=12)
            if out_path.exists() and out_path.stat().st_size > 0:
                return out_path
        except Exception:
            pass
        return None

    def capture_state_snapshot(
        self,
        component_name: str,
        state_dict: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Captures and summarizes a component/function view state for debugging and lakehouse logging.
        """
        return {
            "subagent": self.name,
            "component": component_name,
            "state_keys": list(state_dict.keys()),
            "summary": {k: len(v) if isinstance(v, (list, dict)) else str(v)[:80] for k, v in state_dict.items()},
        }
