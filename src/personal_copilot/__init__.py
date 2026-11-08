"""
Personal Copilot: Modular Second-Brain Hub & Autonomous Subagent Engine.
"""

from personal_copilot.agents.orchestrator import MultiAgentCopilotOrchestrator
from personal_copilot.lakehouse.activity_store import PersonalStructuredLakehouse
from personal_copilot.models import EngineeringLog, KnowledgeChunk
from personal_copilot.rag.hybrid_engine import PersonalKnowledgeRAG

__all__ = [
    "EngineeringLog",
    "KnowledgeChunk",
    "MultiAgentCopilotOrchestrator",
    "PersonalKnowledgeRAG",
    "PersonalStructuredLakehouse",
]

