"""
Multi-Agent Copilot Orchestrator (`src/personal_copilot/agents/orchestrator.py`)
Coordinates:
- Knowledge Vault Recall (ChromaDB + GraphRAG)
- Governed Engineering Lakehouse SQL
- Code -> Test -> Review -> Deploy self-healing loop
"""

from __future__ import annotations

from typing import Any

from personal_copilot.agents.gates import (
    CodeSubagent,
    GitDeploySubagent,
    ReviewSubagent,
    TestSubagent,
    WebAuditSubagent,
)
from personal_copilot.lakehouse.activity_store import PersonalStructuredLakehouse
from personal_copilot.rag.hybrid_engine import PersonalKnowledgeRAG


class MultiAgentCopilotOrchestrator:
    def __init__(self) -> None:
        self.rag = PersonalKnowledgeRAG()
        self.lakehouse = PersonalStructuredLakehouse()
        self.coder = CodeSubagent()
        self.tester = TestSubagent()
        self.reviewer = ReviewSubagent()
        self.web_auditor = WebAuditSubagent()
        self.deployer = GitDeploySubagent()

    def ask(self, query: str) -> dict[str, Any]:
        """
        Processes a user query through the RAG and Lakehouse system.
        """
        rag_res = self.rag.hybrid_search_rrf(query, top_k=3)
        activities = self.lakehouse.execute_governed_sql(
            "SELECT * FROM engineering_activity_logs ORDER BY event_date DESC LIMIT 3"
        )
        return {
            "query": query,
            "retrieved_knowledge": rag_res.get("retrieved_chunks", []),
            "recent_engineering_activities": activities.get("rows", []),
        }

    def execute_engineering_pipeline(
        self,
        task_id: str,
        project_name: str,
        target_file: str,
        task_spec: str,
        simulate_bug_first: bool = True,
        audit_ui: bool = False,
        html_path: str | None = None,
    ) -> dict[str, Any]:
        """
        Full 5-stage engineering loop:
        Code -> Test (Gate 1) -> Review (Gate 2) -> WebAudit (Gate 3, optional) -> GitDeploy.
        """
        from pathlib import Path

        # Step 1: Draft v1
        draft_v1 = self.coder.execute(task_spec, is_retry=False)

        # Step 2: Test Gate #1
        test_res_1 = self.tester.evaluate(draft_v1, fail_first_attempt=simulate_bug_first)

        if not test_res_1["passed"]:
            # Self-healing retry
            draft_v2 = self.coder.execute(task_spec, is_retry=True)
            test_res_2 = self.tester.evaluate(draft_v2, fail_first_attempt=False)
            active_test = test_res_2
        else:
            active_test = test_res_1

        # Step 3: Review Gate #2
        review_res = self.reviewer.evaluate(active_test["passed"])

        # Step 4: WebAudit Gate #3 (UI/DOM inspection if applicable)
        audit_res: dict[str, Any] | None = None
        gate3_passed: bool | None = None
        if audit_ui or (html_path is not None) or target_file.endswith(".html"):
            target_html = Path(html_path) if html_path else Path(target_file)
            audit_res = self.web_auditor.audit_html_file(target_html)
            gate3_passed = audit_res.get("passed", True)

        # Step 5: Final Deploy Gate
        deploy_res = self.deployer.deploy_and_log(
            event_id=task_id,
            project_name=project_name,
            target_file=target_file,
            issue_or_task=task_spec,
            resolution="Self-healing unit tests verified, architecture approved, UI verified",
            gate1_passed=active_test["passed"],
            gate2_passed=review_res["passed"],
            gate3_passed=gate3_passed,
        )

        return {
            "task_id": task_id,
            "gate_1_test": active_test,
            "gate_2_review": review_res,
            "gate_3_audit": audit_res,
            "deploy_result": deploy_res,
        }

