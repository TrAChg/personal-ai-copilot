# FlashAttention GPU SRAM Tiling

**Category**: `technical_mastery` | **Authority Rank**: 5/5 | **Date**: 2026-11-06

## Overview & Key Concepts

FlashAttention fuses QK^T, softmax, and V multiplication inside fast on-chip GPU SRAM via online softmax tiling, avoiding O(T^2) HBM reads/writes.

## Connected GraphRAG Entities

- `Self_Attention_QKV`
- `FlashAttention_SRAM`
