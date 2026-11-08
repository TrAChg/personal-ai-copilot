"""One-line CLI for logging engineering activity & knowledge into ChromaDB & Lakehouse."""

from __future__ import annotations

import argparse
import datetime
import json
import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from personal_copilot.dag import run_daily_knowledge_dag
from personal_copilot.lakehouse.activity_store import PersonalStructuredLakehouse
from personal_copilot.models import KnowledgeChunk
from personal_copilot.rag.hybrid_engine import PersonalKnowledgeRAG


def main() -> None:
    reconfig = getattr(sys.stdout, "reconfigure", None)
    if callable(reconfig):
        reconfig(encoding="utf-8")

    parser = argparse.ArgumentParser(description="One-line Logger for ChromaDB RAG & Engineering Lakehouse")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # 1. note
    p_note = subparsers.add_parser("note", help="Add technical knowledge note to ChromaDB & GraphRAG")
    p_note.add_argument("--id", required=True, help="Unique Note ID, e.g., NOTE-LLM-05")
    p_note.add_argument("--title", required=True, help="Note title")
    p_note.add_argument("--content", required=True, help="Note technical content")
    p_note.add_argument("--category", default="technical_core", help="Category")
    p_note.add_argument("--topic", default="", help="Topic key for superseding old notes")
    p_note.add_argument("--edge", default="", help="Graph edge: SrcNode,RELATION,DstNode")
    p_note.add_argument("--date", default=datetime.date.today().isoformat())

    # 2. bugfix / activity
    p_bug = subparsers.add_parser("bugfix", help="Log verified engineering work to Lakehouse")
    p_bug.add_argument("--id", required=True, help="Event ID, e.g., EVT-10")
    p_bug.add_argument("--project", required=True, help="Project name")
    p_bug.add_argument("--type", default="BUG_FIX", help="BUG_FIX | CODE_IMPL | TEST_RUN | CI_CD_SETUP | GIT_COMMIT")
    p_bug.add_argument("--file", required=True, help="Target file path")
    p_bug.add_argument("--issue", required=True, help="Issue or task description")
    p_bug.add_argument("--fix", required=True, help="Resolution applied")
    p_bug.add_argument("--subagents", default="CodeSubagent -> TestSubagent -> WebAuditSubagent -> GitDeploySubagent", help="Subagents gate chain")
    p_bug.add_argument("--tests", type=int, default=1, help="Tests passed count")
    p_bug.add_argument("--status", default="RESOLVED", help="Status")
    p_bug.add_argument("--date", default=datetime.date.today().isoformat())

    # 3. sync / dag
    subparsers.add_parser("sync", help="Run daily automated DAG scan across AI_Engineer and update viewer")

    args = parser.parse_args()
    rag = PersonalKnowledgeRAG()
    lakehouse = PersonalStructuredLakehouse()
    action_result: dict = {}

    if args.command == "note":
        action_result = rag.upsert_knowledge_note(
            KnowledgeChunk(
                chunk_id=args.id,
                title=args.title,
                content=args.content,
                category=args.category,
                raptor_level=0,
                created_date=args.date,
                authority_rank=5,
                is_latest=True,
                topic_key=args.topic or args.id,
            )
        )
        if args.edge and len(args.edge.split(",")) == 3:
            src, rel, dst = [x.strip() for x in args.edge.split(",")]
            rag.add_graph_edge(src, rel, dst, args.id)
            action_result["added_graph_edge"] = f"{src} --({rel})--> {dst}"

    elif args.command == "bugfix":
        fix_text = args.fix.strip()
        if not fix_text.startswith("["):
            sub_chain = args.subagents or "CodeSubagent -> TestSubagent -> WebAuditSubagent -> GitDeploySubagent"
            fix_text = f"[{sub_chain}] {fix_text}"

        action_result = lakehouse.record_verified_activity(
            event_id=args.id,
            event_date=args.date,
            project_name=args.project,
            activity_type=args.type,
            target_file=args.file,
            issue_or_task=args.issue,
            resolution_applied=fix_text,
            tests_passed=args.tests,
            status=args.status,
        )

    elif args.command == "sync":
        action_result = run_daily_knowledge_dag()

    print(json.dumps({"action": args.command, "result": action_result}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
