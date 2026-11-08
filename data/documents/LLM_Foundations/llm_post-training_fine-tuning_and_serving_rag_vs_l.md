# LLM Post-Training, Fine-Tuning and Serving: RAG vs. LoRA/QLoRA, DPO, Quantization and vLLM

**Category**: `llm_foundations` | **Authority Rank**: 5/5 | **Date**: 2026-11-06

## Overview & Key Concepts

Decision Rule (RAG vs. Fine-Tuning): Use RAG when facts change dynamically or require source citations; use Fine-Tuning (SFT + LoRA/QLoRA) when teaching domain tone, strict JSON/tool schemas, or distilling a large model into a fast 7B/8B model. LoRA Math: Freezes pretrained W_0 in R^(d x k) and trains low-rank delta W = W_0 + (alpha/r) * B * A where B in R^(d x r), A in R^(r x k) with rank r << min(d,k) (e.g., r=16), cutting trainable parameters by >99%. QLoRA quantizes W_0 to 4-bit NormalFloat (NF4) with Double Quantization and Paged Optimizers. Alignment uses DPO (Direct Preference Optimization on chosen vs. rejected pairs without a separate Reward Model). Production serving uses vLLM (PagedAttention eliminating KV-Cache fragmentation) + AWQ/FP8 quantization.

## Connected GraphRAG Entities

- `Self_Attention_QKV`
- `LoRA_QLoRA_vLLM`
