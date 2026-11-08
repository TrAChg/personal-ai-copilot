"""Configuration and environment paths for personal_copilot."""

from __future__ import annotations

import sys
from pathlib import Path

# Base Paths
PACKAGE_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = PACKAGE_ROOT.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
AI_ENGINEER_ROOT = Path(r"c:\Users\TC\AI_Engineer")

# Database Paths
VAULT_PATH = DATA_DIR / "knowledge_vault.json"
LAKEHOUSE_DB_PATH = DATA_DIR / "second_brain_lakehouse.db"
CHROMA_DIR = DATA_DIR / "chroma_db"
DOCUMENTS_DIR = DATA_DIR / "documents"
SNAPSHOTS_DIR = DATA_DIR / "snapshots"
FRONTEND_DIST_DIR = PROJECT_ROOT / "frontend" / "dist"

# ChromaDB Venv Injection
VENV_SITE = PROJECT_ROOT / ".venv" / "Lib" / "site-packages"
if VENV_SITE.exists() and str(VENV_SITE) not in sys.path:
    sys.path.insert(0, str(VENV_SITE))

# RAG & Embedding Constants
EMBEDDING_DIM = 128
CHROMA_COLLECTION_NAME = "second_brain_vault_128d"
BM25_K1 = 1.5
BM25_B = 0.75
RRF_K = 60

