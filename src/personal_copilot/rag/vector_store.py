"""ChromaDB Persistent Client wrapper for HNSW Cosine Index."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from personal_copilot.config import CHROMA_COLLECTION_NAME, CHROMA_DIR
from personal_copilot.models import KnowledgeChunk
from personal_copilot.rag.embeddings import compute_normalized_embedding

try:
    import chromadb  # pyright: ignore[reportMissingImports]
    HAS_CHROMADB = True
except Exception:
    chromadb = None
    HAS_CHROMADB = False


class ChromaVectorStore:
    def __init__(self, chroma_dir: Path = CHROMA_DIR, collection_name: str = CHROMA_COLLECTION_NAME) -> None:
        self.chroma_dir = chroma_dir
        self.collection_name = collection_name
        self.chroma_dir.mkdir(parents=True, exist_ok=True)
        self.client: Any = None
        self.collection: Any = None

        if HAS_CHROMADB and chromadb is not None:
            try:
                client = chromadb.PersistentClient(path=str(self.chroma_dir))
                self.client = client
                self.collection = client.get_or_create_collection(
                    name=self.collection_name,
                    metadata={"hnsw:space": "cosine"},
                )
            except Exception:
                self.client = None
                self.collection = None

    def count(self) -> int:
        if self.collection is not None:
            try:
                return int(self.collection.count())
            except Exception:
                return 0
        return 0

    def sync_chunks(self, chunks: list[KnowledgeChunk]) -> None:
        if self.collection is None or not chunks:
            return

        ids = [c.chunk_id for c in chunks]
        embeddings = [compute_normalized_embedding(f"{c.title} {c.content}") for c in chunks]
        documents = [f"{c.title}\n{c.content}" for c in chunks]
        metadatas = [
            {
                "title": c.title,
                "category": c.category,
                "raptor_level": c.raptor_level,
                "created_date": c.created_date,
                "authority_rank": c.authority_rank,
                "is_latest": c.is_latest,
                "topic_key": c.topic_key,
            }
            for c in chunks
        ]

        try:
            self.collection.upsert(
                ids=ids,
                embeddings=embeddings,
                documents=documents,
                metadatas=metadatas,
            )
        except Exception:
            pass

    def query(self, query_text: str, n_results: int) -> dict[str, Any]:
        if self.collection is None:
            return {"ids": [[]], "distances": [[]]}
        q_vec = compute_normalized_embedding(query_text)
        try:
            res = self.collection.query(
                query_embeddings=[q_vec],
                n_results=n_results,
            )
            return dict(res) if res is not None else {"ids": [[]], "distances": [[]]}
        except Exception:
            return {"ids": [[]], "distances": [[]]}

