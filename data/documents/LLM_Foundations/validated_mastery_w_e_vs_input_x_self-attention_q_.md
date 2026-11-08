# [VALIDATED MASTERY] W_E vs Input X, Self-Attention (Q,K,V) & FFN World Memory

**Category**: `llm_foundations` | **Authority Rank**: 5/5 | **Date**: 2026-11-06

## Overview & Key Concepts

Validated Note (2026-11-06): W_E in R^(V x d_model) is the fixed Vocabulary Dictionary of V=128,256 isolated tokens. When a prompt of length T arrives, we pluck T rows from W_E to build the sentence matrix X in R^(T x d_model). Self-Attention (softmax(QK^T / sqrt(d_k) + M)V) computes token-to-token relationships inside X, while the Feed-Forward Network (FFN, ~75% of parameters) stores general world knowledge learned from pre-training. Private facts live outside the LLM in ChromaDB (RAG) or SQL (MCP).

## Connected GraphRAG Entities

- `W_E_Dictionary`
- `Sentence_Matrix_X`
- `Self_Attention_QKV`
- `FFN_World_Memory`
- `KV_Cache`
