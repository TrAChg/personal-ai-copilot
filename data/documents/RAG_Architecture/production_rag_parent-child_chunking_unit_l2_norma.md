# Production RAG: Parent-Child Chunking, Unit L2 Normalization, HNSW, BM25+RRF, RAPTOR & GraphRAG

**Category**: `rag_architecture` | **Authority Rank**: 5/5 | **Date**: 2026-11-05

## Overview & Key Concepts

When vectors are L2-normalized (||u||=||v||=1), ||u-v||_2^2 = 2(1 - cos(theta)), so Dot Product, Cosine Similarity, and Euclidean L2 produce the exact same ranking (3x faster via Dot Product). ChromaDB uses HNSW (3-layer skip-list graph, O(log N)). Hybrid Search combines Dense Vector + BM25 via Reciprocal Rank Fusion RRF = 1/(60+rank_dense) + 1/(60+rank_bm25), followed by Cross-Encoder re-ranking. For massive datasets: RAPTOR builds a hierarchical summary tree by topic, whereas GraphRAG connects scattered entities across different documents via multi-hop edges.

## Connected GraphRAG Entities

- `ChromaDB_HNSW`
- `Hybrid_BM25_RRF`
- `RAPTOR_Tree`
- `GraphRAG_Network`
