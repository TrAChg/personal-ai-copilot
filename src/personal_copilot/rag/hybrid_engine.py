"""Hybrid RAG Search Engine combining ChromaDB Dense HNSW and BM25 with RRF."""

from __future__ import annotations

import json
from collections import Counter
from dataclasses import asdict
from pathlib import Path
from typing import Any

from personal_copilot.config import BM25_B, BM25_K1, RRF_K, VAULT_PATH
from personal_copilot.models import KnowledgeChunk
from personal_copilot.rag.embeddings import compute_normalized_embedding, tokenize
from personal_copilot.rag.graph_store import KnowledgeGraphStore
from personal_copilot.rag.vector_store import ChromaVectorStore


class PersonalKnowledgeRAG:
    """
    Modular, pure database-backed Hybrid RAG and GraphRAG engine.
    """

    def __init__(self, vault_path: Path = VAULT_PATH) -> None:
        self.vault_path = vault_path
        self.vault_path.parent.mkdir(parents=True, exist_ok=True)
        self.chunks: list[KnowledgeChunk] = []
        self.doc_tokens: list[list[str]] = []
        self.embeddings: list[list[float]] = []
        self.avgdl: float = 0.0
        self.idf: dict[str, float] = {}

        self.vector_store = ChromaVectorStore()
        self.graph_store = KnowledgeGraphStore()

        if self.vault_path.exists():
            self._load_from_disk()

    def _load_from_disk(self) -> None:
        raw = json.loads(self.vault_path.read_text(encoding="utf-8"))
        deduped: dict[str, KnowledgeChunk] = {}
        for c in raw.get("chunks", []):
            chk = KnowledgeChunk(**c)
            deduped[chk.chunk_id] = chk
        self.chunks = list(deduped.values())
        self.graph_store = KnowledgeGraphStore(raw.get("knowledge_graph", {}))
        self._rebuild_indices()

    def _save_to_disk(self) -> None:
        payload = {
            "chunks": [asdict(c) for c in self.chunks],
            "knowledge_graph": self.graph_store.to_dict(),
        }
        self.vault_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    def _rebuild_indices(self) -> None:
        self.doc_tokens = [tokenize(f"{c.title} {c.content}") for c in self.chunks]
        self.embeddings = [compute_normalized_embedding(f"{c.title} {c.content}") for c in self.chunks]
        N = len(self.chunks)
        self.avgdl = sum(len(t) for t in self.doc_tokens) / max(N, 1)

        df: Counter[str] = Counter()
        for tokens in self.doc_tokens:
            for tok in set(tokens):
                df[tok] += 1
        self.idf.clear()
        import math
        for tok, freq in df.items():
            self.idf[tok] = math.log(1.0 + (N - freq + 0.5) / (freq + 0.5))

        self.vector_store.sync_chunks(self.chunks)

    def upsert_knowledge_note(self, chunk: KnowledgeChunk) -> dict[str, Any]:
        superseded: list[str] = []
        for existing in self.chunks:
            if chunk.topic_key and existing.topic_key == chunk.topic_key and existing.chunk_id != chunk.chunk_id and existing.is_latest:
                existing.is_latest = False
                superseded.append(existing.chunk_id)

        self.chunks = [c for c in self.chunks if c.chunk_id != chunk.chunk_id] + [chunk]
        self._rebuild_indices()
        self._save_to_disk()
        return {
            "inserted_chunk_id": chunk.chunk_id,
            "superseded_old_chunks": superseded,
            "chroma_hnsw_total_vectors": self.vector_store.count(),
        }

    def add_graph_edge(self, src: str, relation: str, dst: str, source_chunk_id: str) -> None:
        self.graph_store.add_edge(src, relation, dst, source_chunk_id)
        self._save_to_disk()

    def hybrid_search_rrf(
        self,
        query: str,
        top_k: int = 3,
        resolve_temporal_conflicts: bool = True,
    ) -> dict[str, Any]:
        q_tokens = tokenize(query)
        id_to_idx = {c.chunk_id: idx for idx, c in enumerate(self.chunks)}
        dense_ranked: list[tuple[int, float]] = []

        # Dense ChromaDB HNSW Search
        chroma_res = self.vector_store.query(query, n_results=len(self.chunks))
        queried_ids = chroma_res.get("ids", [[]])[0]
        queried_dists = chroma_res.get("distances", [[]])[0]
        for cid, dist in zip(queried_ids, queried_dists):
            if cid in id_to_idx:
                dense_ranked.append((id_to_idx[cid], 1.0 - float(dist)))

        # Fallback if ChromaDB returned empty
        if not dense_ranked:
            q_vec = compute_normalized_embedding(query)
            dense_scores = [
                (idx, sum(q_vec[d] * self.embeddings[idx][d] for d in range(len(q_vec))))
                for idx in range(len(self.chunks))
            ]
            dense_ranked = sorted(dense_scores, key=lambda x: x[1], reverse=True)

        # Sparse BM25 Search
        bm25_scores: list[tuple[int, float]] = []
        for idx, _ in enumerate(self.chunks):
            doc_toks = self.doc_tokens[idx]
            doc_len = len(doc_toks)
            tf_map = Counter(doc_toks)
            b_score = 0.0
            for qt in q_tokens:
                if qt not in tf_map:
                    continue
                tf = tf_map[qt]
                num = tf * (BM25_K1 + 1.0)
                den = tf + BM25_K1 * (1.0 - BM25_B + BM25_B * (doc_len / self.avgdl))
                b_score += self.idf.get(qt, 0.0) * (num / den)
            bm25_scores.append((idx, b_score))

        bm25_ranked = sorted(bm25_scores, key=lambda x: x[1], reverse=True)

        # Reciprocal Rank Fusion
        rrf_map: dict[int, float] = {}
        for rank, (doc_idx, _) in enumerate(dense_ranked, start=1):
            rrf_map[doc_idx] = rrf_map.get(doc_idx, 0.0) + 1.0 / (RRF_K + rank)
        for rank, (doc_idx, _) in enumerate(bm25_ranked, start=1):
            rrf_map[doc_idx] = rrf_map.get(doc_idx, 0.0) + 1.0 / (RRF_K + rank)

        sorted_indices = [idx for idx, _ in sorted(rrf_map.items(), key=lambda x: x[1], reverse=True)]

        conflicts_resolved: list[str] = []
        selected_chunks: list[dict[str, Any]] = []
        seen_topics: dict[str, KnowledgeChunk] = {}

        for idx in sorted_indices:
            chunk = self.chunks[idx]
            if resolve_temporal_conflicts and not chunk.is_latest:
                conflicts_resolved.append(
                    f"Suppressed outdated misconception '{chunk.chunk_id}' ({chunk.created_date}) "
                    f"in favor of latest validated note on topic '{chunk.topic_key}'."
                )
                continue
            if chunk.topic_key and chunk.topic_key in seen_topics:
                continue
            seen_topics[chunk.topic_key] = chunk
            selected_chunks.append({
                "chunk_id": chunk.chunk_id,
                "title": chunk.title,
                "raptor_level": chunk.raptor_level,
                "created_date": chunk.created_date,
                "authority_rank": chunk.authority_rank,
                "rrf_score": round(rrf_map[idx], 5),
                "content": chunk.content,
            })
            if len(selected_chunks) >= top_k:
                break

        return {
            "retrieved_chunks": selected_chunks,
            "temporal_conflicts_resolved": conflicts_resolved,
        }

    def graph_multi_hop_traversal(self, start_entity: str, max_hops: int = 2) -> dict[str, Any]:
        return self.graph_store.traverse(start_entity, max_hops)

