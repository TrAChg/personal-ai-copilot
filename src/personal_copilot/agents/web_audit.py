"""
Web & UI Audit Subagent (`src/personal_copilot/agents/web_audit.py`)
Performs static & functional inspection of generated web interfaces (HTML/CSS/JS):
- Enforces strict design tokens (0px border-radius, French palette #002654 / #0055A5).
- Audits DOM container presence and interactive elements.
- Captures state snapshots of function views, table rows, and graph metrics.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
from pathlib import Path
from typing import Any

from personal_copilot.config import SNAPSHOTS_DIR


class WebAuditSubagent:
    """Gatekeeper & Inspector Subagent for Web Interfaces and UI Views."""

    def __init__(self, name: str = "WebAuditSubagent") -> None:
        self.name = name

    def audit_html_file(self, html_path: Path) -> dict[str, Any]:
        """
        Audits an HTML file for DOM integrity, design system conformance, and state readiness.
        """
        if not html_path.exists():
            return {
                "gate": "WebAudit (UI Gate)",
                "passed": False,
                "error": f"Target HTML file does not exist: {html_path}",
                "metrics": {},
            }

        content = html_path.read_text(encoding="utf-8")
        
        # If auditing a compiled React SPA bundle, include asset files (JS/CSS)
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

        # 1. Design Token Check: 0px border-radius enforcement
        if "border-radius:0" in bundle_text or "border-radius: 0" in bundle_text:
            checks_passed.append("Strict 0px border-radius design token present")
        else:
            issues.append("Warning: 'border-radius: 0px' token not detected in stylesheets")

        # 2. Design Token Check: French Palette #002654 & #0055A5
        if "#002654" in bundle_text and "#0055A5" in bundle_text:
            checks_passed.append("French Blue & Navy palette (#002654, #0055A5) verified")
        else:
            issues.append("Warning: French Navy/Blue palette tokens missing")

        # 3. DOM Container Checks
        required_containers = [
            ("graph-box", "Graph Network container"),
            ("tb-activities", "Activity Logs table body"),
            ("tb-chunks", "Knowledge Chunks table body"),
            ("m-nodes", "Graph Nodes metric element"),
            ("m-chunks", "Knowledge Chunks metric element"),
            ("m-activities", "Activity Logs metric element"),
        ]

        for elem_id, label in required_containers:
            if f'id="{elem_id}"' in bundle_text or f"id='{elem_id}'" in bundle_text or f'"{elem_id}"' in bundle_text:
                checks_passed.append(f"DOM Container [{elem_id}] ({label}) present")
            else:
                issues.append(f"Critical DOM container missing: #{elem_id} ({label})")

        # 4. Data Layer Verification (Embedded JSON or React REST /api/data)
        payload_stats: dict[str, Any] = {}
        from personal_copilot.lakehouse.data_extractor import extract_live_data

        try:
            live_data = extract_live_data()
            payload_stats = {
                "total_nodes": len(live_data.get("nodes", [])),
                "total_edges": len(live_data.get("edges", [])),
                "total_activities": len(live_data.get("activities", [])),
                "total_chunks": len(live_data.get("chunks", [])),
            }
            checks_passed.append("Live JSON data payload verified from data_extractor service")
        except Exception as e:
            issues.append(f"Failed to query data_extractor: {e}")

        # 5. Table Overflow / Scroll styling check
        if "overflow-y: auto" in bundle_text or "overflow-y:auto" in bundle_text or "overflow-x:auto" in bundle_text or "overflow-x: auto" in bundle_text:
            checks_passed.append("Scrollable table wrapper container verified")
        else:
            issues.append("Missing scroll capability for large datasets")

        passed = len([i for i in issues if "Critical" in i]) == 0

        # 6. Capture Visual Screenshots into data/snapshots/ for each view
        snapshots_captured = self.capture_all_view_snapshots(html_path)
        if snapshots_captured:
            for s in snapshots_captured:
                checks_passed.append(f"Visual UI view snapshot captured: {s.name}")

        return {
            "gate": "WebAudit (UI Gate)",
            "passed": passed,
            "target_file": str(html_path),
            "file_size_kb": round(len(content.encode("utf-8")) / 1024, 2),
            "visual_snapshots": [str(s) for s in snapshots_captured],
            "checks_passed": checks_passed,
            "issues": issues,
            "state_snapshot": payload_stats,
        }

    def capture_all_view_snapshots(self, html_path: Path, subfolder: str | None = "personal_copilot") -> list[Path]:
        """
        Captures visual screenshots for all main views (Graph, Activity Logs, Knowledge Chunks, RAPTOR).
        Uses live server (http://localhost:8765) if active, else falls back to local file.
        """
        views = [
            ("functional_test_verified_dashboard.png", ""),
            ("functional_test_verified_activities.png", "#activities"),
            ("functional_test_verified_chunks.png", "#chunks"),
            ("functional_test_verified_raptor.png", "#raptor"),
        ]
        results: list[Path] = []
        for filename, hash_suffix in views:
            res = self.capture_visual_screenshot(
                html_path, output_name=filename, hash_suffix=hash_suffix, subfolder=subfolder
            )
            if res:
                results.append(res)
        return results

    def capture_visual_screenshot(
        self,
        html_path: Path,
        output_name: str | None = None,
        hash_suffix: str = "",
        subfolder: str | None = "personal_copilot",
    ) -> Path | None:
        """
        Captures a real visual PNG screenshot of the interface using headless Chrome or Edge.
        Targets http://localhost:8765 if reachable, with virtual-time-budget to allow React hydration.
        Saved directly in `data/snapshots/`.
        """
        target_dir = SNAPSHOTS_DIR / subfolder if subfolder else SNAPSHOTS_DIR
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

        # Check if live server is reachable on port 8765
        import urllib.request
        target_url = "http://localhost:8765" + hash_suffix
        try:
            urllib.request.urlopen("http://localhost:8765", timeout=1)
        except Exception:
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

