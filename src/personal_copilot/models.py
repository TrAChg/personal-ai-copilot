"""Domain models and data schemas for personal_copilot."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class KnowledgeChunk:
    chunk_id: str
    title: str
    content: str
    category: str
    raptor_level: int  # 0 = Concept Note, 1 = Domain Summary, 2 = Global Root
    created_date: str
    authority_rank: int  # 1 = Early draft / misconception, 5 = Validated mastery
    is_latest: bool = True
    topic_key: str = ""
    entities: list[str] = field(default_factory=list)
    raptor_parent_l1: str = ""
    raptor_parent_l2: str = ""
    child_count: int = 0
    file_name: str = ""


@dataclass
class EngineeringLog:
    event_id: str
    event_date: str
    project_name: str
    activity_type: str  # BUG_FIX | CODE_IMPL | TEST_RUN | CI_CD_SETUP | GIT_COMMIT
    target_file: str
    issue_or_task: str
    resolution_applied: str
    tests_passed: int
    status: str  # RESOLVED | MERGED_TO_MAIN | COMMITTED_PUSHED


@dataclass
class GraphEdge:
    source: str
    relation: str
    target: str
    chunk_id: str = ""

