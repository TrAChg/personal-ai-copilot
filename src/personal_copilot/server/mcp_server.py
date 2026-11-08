"""
Standard Model Context Protocol (MCP) JSON-RPC 2.0 Server (`src/personal_copilot/server/mcp_server.py`)
Exposes:
- Tools: query_engineering_lakehouse, recall_knowledge_rag, record_deployed_engineering_work
- Resources: lakehouse://engineering_activity_logs, rag://knowledge_vault
"""

from __future__ import annotations

import json
import sys
from typing import Any

from personal_copilot.lakehouse.activity_store import PersonalStructuredLakehouse
from personal_copilot.rag.hybrid_engine import PersonalKnowledgeRAG


class PersonalCopilotMCPServer:
    def __init__(self) -> None:
        self.rag = PersonalKnowledgeRAG()
        self.lakehouse = PersonalStructuredLakehouse()

    def handle_request(self, request: dict[str, Any]) -> dict[str, Any]:
        req_id = request.get("id")
        method = request.get("method")
        params = request.get("params", {})

        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "serverInfo": {"name": "personal-copilot-mcp-db", "version": "2.0.0"},
                    "capabilities": {"resources": {}, "tools": {}},
                },
            }

        if method == "tools/list":
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "tools": [
                        {
                            "name": "query_engineering_lakehouse",
                            "description": "Execute read-only SQL on engineering_activity_logs",
                            "inputSchema": {"type": "object", "properties": {"sql": {"type": "string"}}, "required": ["sql"]},
                        },
                        {
                            "name": "recall_knowledge_rag",
                            "description": "Search technical knowledge vault using ChromaDB HNSW + BM25 RRF",
                            "inputSchema": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]},
                        },
                        {
                            "name": "record_deployed_engineering_work",
                            "description": "Log verified engineering work to the Lakehouse",
                            "inputSchema": {"type": "object", "properties": {"event_id": {"type": "string"}}, "required": ["event_id"]},
                        },
                    ]
                },
            }

        if method == "tools/call":
            tool_name = params.get("name")
            args = params.get("arguments", {})

            if tool_name == "query_engineering_lakehouse":
                res = self.lakehouse.execute_governed_sql(args.get("sql", ""))
                return {"jsonrpc": "2.0", "id": req_id, "result": res}

            if tool_name == "recall_knowledge_rag":
                res = self.rag.hybrid_search_rrf(args.get("query", ""))
                return {"jsonrpc": "2.0", "id": req_id, "result": res}

            if tool_name == "record_deployed_engineering_work":
                res = self.lakehouse.record_verified_activity(
                    event_id=args.get("event_id", ""),
                    event_date=args.get("event_date", ""),
                    project_name=args.get("project_name", ""),
                    activity_type=args.get("activity_type", "CODE_IMPL"),
                    target_file=args.get("target_file", ""),
                    issue_or_task=args.get("issue_or_task", ""),
                    resolution_applied=args.get("resolution_applied", ""),
                    tests_passed=args.get("tests_passed", 1),
                    status=args.get("status", "RESOLVED"),
                )
                return {"jsonrpc": "2.0", "id": req_id, "result": res}

            return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Method not found: {tool_name}"}}

        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Method not found: {method}"}}


def run_stdio_server() -> None:
    server = PersonalCopilotMCPServer()
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            res = server.handle_request(req)
            sys.stdout.write(json.dumps(res, ensure_ascii=False) + "\n")
            sys.stdout.flush()
        except Exception as ex:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(ex)}}
            sys.stdout.write(json.dumps(err) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    run_stdio_server()

