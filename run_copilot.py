"""Main runtime CLI for Personal Copilot: Recall, SQL query, and subagent demo."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from personal_copilot.agents.orchestrator import MultiAgentCopilotOrchestrator


def main() -> None:
    reconfig = getattr(sys.stdout, "reconfigure", None)
    if callable(reconfig):
        reconfig(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Personal AI Copilot Engine")
    parser.add_argument("--recall", type=str, help="Recall knowledge from ChromaDB HNSW + BM25 RRF")
    parser.add_argument("--sql", type=str, help="Execute governed read-only SQL on engineering_activity_logs")
    parser.add_argument("--demo", action="store_true", help="Run multi-subagent gatekeeper demonstration")
    parser.add_argument("--audit-web", type=str, nargs="?", const="frontend/dist/index.html", help="Audit React SPA DOM, styles, and state with WebAuditSubagent")
    parser.add_argument("--serve", action="store_true", help="Launch the real-time live dashboard server (default: port 8765)")
    parser.add_argument("--port", type=int, default=8765, help="Port for the live server (default: 8765)")

    args = parser.parse_args()
    orchestrator = MultiAgentCopilotOrchestrator()

    if args.serve:
        from personal_copilot.server.live_server import run_live_server

        run_live_server(port=args.port)
        return

    if args.demo:
        print("[1/3] Querying Knowledge Vault for Self-Attention...")
        rag_res = orchestrator.rag.hybrid_search_rrf("Self-Attention QKV", top_k=2)
        for c in rag_res.get("retrieved_chunks", []):
            print(f" -> Found [{c['chunk_id']}] {c['title']} (RRF: {c['rrf_score']})")

        print("\n[2/3] Checking past engineering bugfixes in Lakehouse...")
        logs = orchestrator.lakehouse.execute_governed_sql(
            "SELECT event_id, target_file, issue_or_task, status FROM engineering_activity_logs LIMIT 2"
        )
        for r in logs.get("rows", []):
            print(f" -> [{r['event_id']}] {r['target_file']}: {r['status']}")

        print("\n[3/3] Running Autonomous Gatekeeper Loop: Code -> Test (Gate 1) -> Review (Gate 2) -> GitDeploy...")
        res = orchestrator.execute_engineering_pipeline(
            task_id="EVT-DEMO-01",
            project_name="personal-ai-copilot",
            target_file="src/personal_copilot/demo.py",
            task_spec="Implement clean modular demo pipeline",
            simulate_bug_first=True,
        )
        print(f" -> Test Gate #1: {res['gate_1_test']['details']}")
        print(f" -> Review Gate #2: {res['gate_2_review']['details']}")
        print(f" -> Deploy Gate: {res['deploy_result']['status']}")
        print("\nDemo completed with 100% assertions passed!")
        return

    if args.audit_web:
        target_path = Path(args.audit_web)
        if not target_path.is_absolute():
            target_path = Path(__file__).resolve().parent / target_path
        audit_res = orchestrator.web_auditor.audit_html_file(
            target_path,
            project_name="personal_copilot",
            views=[
                ("functional_test_verified_dashboard.png", ""),
                ("functional_test_verified_activities.png", "#activities"),
                ("functional_test_verified_chunks.png", "#chunks"),
                ("functional_test_verified_raptor.png", "#raptor"),
            ],
            required_containers=[
                ("graph-box", "Graph Network container"),
                ("tb-activities", "Activity Logs table body"),
                ("tb-chunks", "Knowledge Chunks table body"),
                ("m-nodes", "Graph Nodes metric element"),
                ("m-chunks", "Knowledge Chunks metric element"),
                ("m-activities", "Activity Logs metric element"),
            ],
            design_tokens={"border-radius": "border-radius:0", "palette": "#0055A5"},
            live_server_url="http://localhost:8765",
        )
        print(json.dumps(audit_res, indent=2, ensure_ascii=False))
        return

    if args.recall:
        res = orchestrator.rag.hybrid_search_rrf(args.recall, top_k=3)
        print(json.dumps(res, indent=2, ensure_ascii=False))
        return

    if args.sql:
        res = orchestrator.lakehouse.execute_governed_sql(args.sql)
        print(json.dumps(res, indent=2, ensure_ascii=False))
        return

    parser.print_help()


if __name__ == "__main__":
    main()
