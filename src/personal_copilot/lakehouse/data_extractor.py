"""
Data Extractor Service (`src/personal_copilot/lakehouse/data_extractor.py`)
Queries Lakehouse SQLite, ChromaDB, and Knowledge Vault to build the live JSON payload
consumed by the React SPA and REST API endpoints.
"""

from __future__ import annotations

import datetime
import hashlib
import json
import sqlite3
from typing import Any

from personal_copilot.config import CHROMA_DIR, LAKEHOUSE_DB_PATH, SNAPSHOTS_DIR, VAULT_PATH


def extract_live_data() -> dict[str, Any]:
    vault_data: dict[str, Any] = {"chunks": [], "knowledge_graph": {}}
    if VAULT_PATH.exists():
        try:
            vault_data = json.loads(VAULT_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass

    chunks = vault_data.get("chunks", [])
    raw_graph = vault_data.get("knowledge_graph", {})

    node_set: set[str] = set(raw_graph.keys())
    forward_edges: list[dict[str, str]] = []
    for src, neighbors in raw_graph.items():
        for dst, rel, cid in neighbors:
            node_set.add(dst)
            if not rel.startswith("inverse_"):
                forward_edges.append({
                    "from": src,
                    "to": dst,
                    "label": rel,
                    "chunk_id": cid,
                })

    nodes: list[dict[str, Any]] = [
        {"id": node_id, "label": node_id.replace("_", " ")}
        for node_id in sorted(node_set)
    ]

    activities: list[dict[str, Any]] = []
    if LAKEHOUSE_DB_PATH.exists():
        try:
            conn = sqlite3.connect(LAKEHOUSE_DB_PATH)
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("""
                SELECT event_id, event_date, project_name, activity_type,
                       target_file, issue_or_task, resolution_applied, tests_passed, status
                FROM engineering_activity_logs
                ORDER BY event_date DESC, rowid DESC
            """)
            activities = [dict(row) for row in cur.fetchall()]
            conn.close()
        except Exception:
            pass

    chroma_count = 0
    chroma_sqlite = CHROMA_DIR / "chroma.sqlite3"
    if chroma_sqlite.exists():
        try:
            conn_c = sqlite3.connect(chroma_sqlite)
            cur_c = conn_c.cursor()
            cur_c.execute("SELECT COUNT(*) FROM embeddings")
            chroma_count = cur_c.fetchone()[0]
            conn_c.close()
        except Exception:
            chroma_count = len(chunks)

    snapshots: list[dict[str, Any]] = []
    if SNAPSHOTS_DIR.exists():
        for f in sorted(SNAPSHOTS_DIR.rglob("*.png")):
            folder = f.parent.name if f.parent != SNAPSHOTS_DIR else "general"
            rel_path = f.relative_to(SNAPSHOTS_DIR.parent.parent).as_posix()
            snapshots.append({
                "name": f.name,
                "folder": folder,
                "rel_path": rel_path,
                "size_kb": round(f.stat().st_size / 1024, 1),
            })

    version_str = f"{len(nodes)}_{len(forward_edges)}_{len(chunks)}_{len(activities)}_{len(snapshots)}_{chroma_count}"
    version_hash = hashlib.md5(version_str.encode("utf-8")).hexdigest()[:10]

    return {
        "version": version_hash,
        "updated_at": datetime.datetime.now().isoformat(),
        "nodes": nodes,
        "edges": forward_edges,
        "chunks": chunks,
        "activities": activities,
        "snapshots": snapshots,
        "stats": {
            "total_nodes": len(nodes),
            "total_edges": len(forward_edges),
            "total_chunks": len(chunks),
            "active_chunks": sum(1 for c in chunks if c.get("is_latest", True)),
            "total_activities": len(activities),
            "total_snapshots": len(snapshots),
            "chroma_vectors": chroma_count,
        },
    }

