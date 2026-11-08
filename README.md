# Personal AI Copilot & Second Brain Lakehouse

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-18+-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Vite](https://img.shields.io/badge/Vite-6.0+-646CFF?style=for-the-badge&logo=vite&logoColor=white)](https://vitejs.dev/)
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.4+-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)](https://tailwindcss.com/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_Store-FF6F00?style=for-the-badge)](https://www.trychroma.com/)
[![SQLite](https://img.shields.io/badge/SQLite-Lakehouse-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json&style=for-the-badge)](https://github.com/astral-sh/ruff)
[![Mypy Strict](https://img.shields.io/badge/Mypy-Strict-blue?style=for-the-badge)](https://mypy-lang.org/)
[![Tests](https://img.shields.io/badge/Tests-100%25_Passed-success?style=for-the-badge&logo=pytest&logoColor=white)](https://docs.pytest.org/)

A production-grade, enterprise-architected Second Brain combining **ChromaDB HNSW Vector Storage**, **GraphRAG Adjacency Networks**, **RAPTOR Hierarchical Trees**, and an **Autonomous Engineering Lakehouse**.

---

## 1. Architectural Highlights

1. **Modern Dual-Mode React SPA**:
   - **Tab 1: Knowledge Graph (GraphRAG)**: Interactive 2D canvas visualizing multi-hop conceptual relationships between architectures, algorithms, and models.
   - **Tab 2: Engineering Activity Lakehouse**: SQLite-backed activity timeline featuring an **interactive accordion breakdown** displaying the multi-subagent execution lifecycle (`CodeSubagent` → `TestSubagent` → `ReviewSubagent` → `WebAuditSubagent` → `GitDeploySubagent`).
   - **Tab 3: Technical Knowledge Chunks**: High-density knowledge cards featuring folder-level titles, click-to-expand full Markdown rendering, and ChromaDB vector indexing indicators.
   - **Tab 4: RAPTOR Hierarchical Trees**: Stanford-paper abstractive multi-scale trees rolling up leaf chunks (Level 0) into domain syntheses (Level 1) and an executive repository root (Level 2).
   - **Project Snapshots Explorer**: Visual regression and UI verification screenshots organized by individual project folders.

2. **Automated Semantic Heading-Aware Chunking**:
   - `dag.py` scans `data/documents/` and intelligently splits large Markdown files (up to 2 MB+) by heading boundaries (`#`, `##`, `###`) to ensure **0% truncation** in ChromaDB.
   - Automatically synthesizes Level-1 RAPTOR summary nodes for multi-section documents.

3. **Governed Lakehouse Engine**:
   - SQLite persistence strictly recording verified engineering milestones, unit test metrics, and gatekeeper approvals.

---

## 2. Directory Layout

```text
personal-ai-copilot/
├── pyproject.toml                         # Python package specification (uv / pip)
├── README.md                              # System architecture and user guide
├── .gitignore                             # Git exclusion rules
├── log_activity.py                        # Fast CLI logger & DAG synchronizer
├── run_copilot.py                         # Runtime recall & governed SQL CLI
├── data/
│   ├── chroma_db/                         # Persistent ChromaDB HNSW Cosine Index (128-D)
│   ├── documents/                         # Ingestion inbox for custom Markdown notes
│   ├── snapshots/                         # Project-separated visual test screenshots
│   │   └── personal_copilot/
│   ├── knowledge_vault.json               # GraphRAG adjacency network & technical chunks
│   └── second_brain_lakehouse.db          # SQLite Lakehouse (engineering_activity_logs)
├── frontend/                              # Reactive Vite + React + Tailwind SPA
│   ├── src/
│   │   ├── components/                    # ActivitiesTable, ChunksTable, RaptorTreeViewer, SnapshotsModal
│   │   ├── hooks/                         # useLakehouseData (REST polling & state)
│   │   └── types/                         # TypeScript interfaces
│   └── dist/                              # Production compiled bundle served by live server
└── src/
    └── personal_copilot/
        ├── config.py                      # Deterministic paths and constants
        ├── models.py                      # Strongly-typed dataclasses
        ├── dag.py                         # Automated DAG scanner & semantic heading chunker
        ├── rag/                           # ChromaDB vector store, GraphRAG, and Hybrid RRF engine
        ├── lakehouse/                     # Governed SQL & activity store
        ├── agents/                        # Autonomous gatekeeper & WebAuditSubagent
        └── server/                        # Live HTTP server & MCP server
```

---

## 3. Quick-Start Guide

### A. Launch the Live React Dashboard
```powershell
# Start the live web server (serves React SPA on http://localhost:8765)
python run_copilot.py --serve
```
Open **http://localhost:8765** in your browser.

### B. Run Multi-Subagent Demo & WebAudit
```powershell
# Run the 5-stage gatekeeper demo (Code -> Test -> Review -> WebAudit -> GitDeploy)
python run_copilot.py --demo

# Run WebAuditSubagent: audit DOM, check 0px radius, capture visual test snapshots
python run_copilot.py --audit-web
```

### C. Log an Activity or Trigger Daily DAG Sync
```powershell
# Log a verified engineering bugfix / code commit into the Lakehouse
python log_activity.py bugfix --id "EVT-10" --project "personal-ai-copilot" --type "CODE_IMPL" --file "src/personal_copilot/config.py" --issue "Modular refactor" --fix "Built decoupled package structure" --tests 5 --status "RESOLVED"

# Trigger daily automated DAG sync across AI_Engineer
python log_activity.py sync
```

### D. Recall Knowledge & Run Governed SQL
```powershell
# Query knowledge from ChromaDB HNSW + BM25 RRF
python run_copilot.py --recall "Self-Attention QKV"

# Run governed read-only SQL on engineering_activity_logs
python run_copilot.py --sql "SELECT event_id, event_date, project_name, status FROM engineering_activity_logs ORDER BY rowid DESC LIMIT 5"
```
