# Corrective RAG (CRAG) External Search & Dynamic Graph Node Ingestion

**Category**: `rag_architecture` | **Authority Rank**: 5/5 | **Date**: 2026-11-06

## Overview & Key Concepts

When internal ChromaDB retrieval confidence is below threshold, CRAG triggers External Search (Web/ArXiv via Antigravity search_web) and dynamically ingests new Nodes and Edges into the internal GraphRAG Knowledge Graph.

## Connected GraphRAG Entities

- `GraphRAG_Network`
- `CRAG_External_Search`
