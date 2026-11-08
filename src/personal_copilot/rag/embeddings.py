"""Open-vocabulary 128-D signed feature hashing with L2-normalization."""

from __future__ import annotations

import hashlib
import math
from collections import Counter

from personal_copilot.config import EMBEDDING_DIM


def tokenize(text: str) -> list[str]:
    cleaned = (
        text.lower()
        .replace(".", " ")
        .replace(",", " ")
        .replace("(", " ")
        .replace(")", " ")
        .replace(":", " ")
        .replace("-", " ")
        .replace("'", " ")
        .replace("/", " ")
        .replace('"', " ")
    )
    return [tok for tok in cleaned.split() if tok]


def compute_normalized_embedding(text: str, dim: int = EMBEDDING_DIM) -> list[float]:
    """
    Computes a 128-D L2-normalized vector (||v||_2 = 1.0) using unigram and bigram
    signed feature hashing (Weinberger et al.).
    No hardcoded word lists: any technical topic or formula is projected into R^128.
    """
    tokens = tokenize(text)
    features: Counter[str] = Counter(tokens)
    for i in range(len(tokens) - 1):
        features[f"{tokens[i]}_{tokens[i + 1]}"] += 1

    raw_vec: list[float] = [0.0] * dim
    for feat, count in features.items():
        digest = hashlib.md5(feat.encode("utf-8")).digest()
        bucket = digest[0] % dim
        sign = 1.0 if (digest[1] % 2 == 0) else -1.0
        raw_vec[bucket] += sign * (1.0 + math.log(float(count)))

    norm = math.sqrt(sum(x * x for x in raw_vec))
    if norm == 0.0:
        raw_vec[0] = 1.0
        return raw_vec
    return [x / norm for x in raw_vec]

