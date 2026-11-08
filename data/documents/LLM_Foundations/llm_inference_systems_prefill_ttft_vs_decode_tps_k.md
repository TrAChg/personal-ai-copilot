# LLM Inference Systems: Prefill (TTFT) vs Decode (TPS), KV-Cache & GQA

**Category**: `llm_foundations` | **Authority Rank**: 5/5 | **Date**: 2026-11-05

## Overview & Key Concepts

Prefill processes all T prompt tokens in parallel (Matrix-Matrix multiplication, Compute-bound, measured by TTFT). Decode generates tokens 1-by-1 auto-regressively (Vector-Matrix multiplication, Memory-Bandwidth bound, measured by TPS). KV-Cache saves past Keys and Values so Decode is O(t) instead of O(t^2), costing VRAM = 2 * L * H_kv * d_h * S * B * P. Grouped-Query Attention (GQA) shares 1 KV head across G Query heads, shrinking KV-Cache by 4x-8x.

## Connected GraphRAG Entities

- `KV_Cache`
- `Grouped_Query_Attention`
- `Self_Attention_QKV`
