"""Structured Lakehouse store strictly for engineering_activity_logs (no session bloat)."""

from __future__ import annotations

import re
import sqlite3
from pathlib import Path
from typing import Any

from personal_copilot.config import LAKEHOUSE_DB_PATH


class PersonalStructuredLakehouse:
    """
    Dedicated Engineering & Bugfix Lakehouse storing verified activity records:
    code implementation, unit testing, reviews, CI/CD, and Git commits.
    """

    def __init__(self, db_path: Path = LAKEHOUSE_DB_PATH) -> None:
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_database()

    def _init_database(self) -> None:
        conn = sqlite3.connect(self.db_path)
        try:
            with conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS engineering_activity_logs (
                        event_id TEXT PRIMARY KEY,
                        event_date TEXT NOT NULL,
                        project_name TEXT NOT NULL,
                        activity_type TEXT NOT NULL,
                        target_file TEXT NOT NULL,
                        issue_or_task TEXT NOT NULL,
                        resolution_applied TEXT NOT NULL,
                        tests_passed INTEGER NOT NULL DEFAULT 1,
                        status TEXT NOT NULL
                    )
                """)
                # Explicitly drop conversation_sessions if it still lingers
                conn.execute("DROP TABLE IF EXISTS conversation_sessions")
        finally:
            conn.close()

    def record_verified_activity(
        self,
        event_id: str,
        event_date: str,
        project_name: str,
        activity_type: str,
        target_file: str,
        issue_or_task: str,
        resolution_applied: str,
        tests_passed: int,
        status: str,
    ) -> dict[str, Any]:
        conn = sqlite3.connect(self.db_path)
        try:
            with conn:
                conn.execute(
                    """
                    INSERT INTO engineering_activity_logs (
                        event_id, event_date, project_name, activity_type,
                        target_file, issue_or_task, resolution_applied, tests_passed, status
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(event_id) DO UPDATE SET
                        event_date = excluded.event_date,
                        project_name = excluded.project_name,
                        activity_type = excluded.activity_type,
                        target_file = excluded.target_file,
                        issue_or_task = excluded.issue_or_task,
                        resolution_applied = excluded.resolution_applied,
                        tests_passed = excluded.tests_passed,
                        status = excluded.status
                    """,
                    (
                        event_id,
                        event_date,
                        project_name,
                        activity_type,
                        target_file,
                        issue_or_task,
                        resolution_applied,
                        tests_passed,
                        status,
                    ),
                )
            return {"logged_event_id": event_id, "status": status}
        finally:
            conn.close()

    def count_activities(self) -> int:
        conn = sqlite3.connect(self.db_path)
        try:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM engineering_activity_logs")
            row = cur.fetchone()
            return row[0] if row else 0
        finally:
            conn.close()

    def execute_governed_sql(self, sql_query: str) -> dict[str, Any]:
        """
        Executes read-only governed SQL against engineering_activity_logs.
        Blocks DDL/DML injection attacks.
        """
        clean_sql = sql_query.strip()
        blocked_keywords = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "TRUNCATE", "REPLACE", "CREATE"]
        first_token = clean_sql.split()[0].upper() if clean_sql else ""

        if first_token != "SELECT" or any(re.search(rf"\b{kw}\b", clean_sql, re.IGNORECASE) for kw in blocked_keywords):
            return {
                "isError": True,
                "error_message": "SecurityViolation: Only SELECT queries are permitted on the Lakehouse.",
                "sql_attempted": sql_query,
            }

        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            cur = conn.cursor()
            cur.execute(clean_sql)
            rows = [dict(r) for r in cur.fetchall()]
            return {
                "isError": False,
                "sql_executed": clean_sql,
                "row_count": len(rows),
                "rows": rows,
            }
        except sqlite3.OperationalError as ex:
            return {
                "isError": True,
                "sql_attempted": clean_sql,
                "error_message": f"OperationalError: {ex}",
                "schema_hint": {
                    "engineering_activity_logs": [
                        "event_id", "event_date", "project_name", "activity_type",
                        "target_file", "issue_or_task", "resolution_applied", "tests_passed", "status"
                    ]
                },
            }
        finally:
            conn.close()

