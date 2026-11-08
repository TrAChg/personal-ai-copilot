"""GraphRAG knowledge graph storage and multi-hop traversal."""

from __future__ import annotations

from collections import deque
from typing import Any


class KnowledgeGraphStore:
    def __init__(self, raw_graph: dict[str, list[Any]] | None = None) -> None:
        self.adj: dict[str, list[tuple[str, str, str]]] = {}
        if raw_graph:
            for k, edges in raw_graph.items():
                self.adj[k] = [(e[0], e[1], e[2]) for e in edges]

    def add_edge(self, src: str, relation: str, dst: str, source_chunk_id: str) -> None:
        existing = self.adj.setdefault(src, [])
        if (dst, relation, source_chunk_id) not in existing:
            existing.append((dst, relation, source_chunk_id))
        inv_existing = self.adj.setdefault(dst, [])
        if (src, f"inverse_{relation}", source_chunk_id) not in inv_existing:
            inv_existing.append((src, f"inverse_{relation}", source_chunk_id))

    def node_count(self) -> int:
        nodes: set[str] = set(self.adj.keys())
        for edges in self.adj.values():
            for dst, _, _ in edges:
                nodes.add(dst)
        return len(nodes)

    def forward_edges_count(self) -> int:
        cnt = 0
        for edges in self.adj.values():
            for _, rel, _ in edges:
                if not rel.startswith("inverse_"):
                    cnt += 1
        return cnt

    def traverse(self, start_entity: str, max_hops: int = 2) -> dict[str, Any]:
        if start_entity not in self.adj:
            return {"error": f"Entity '{start_entity}' not in Graph. Available: {sorted(self.adj.keys())}"}

        visited: set[str] = {start_entity}
        queue: deque[tuple[str, int, list[str]]] = deque([(start_entity, 0, [start_entity])])
        discovered_paths: list[str] = []
        linked_chunk_ids: set[str] = set()

        while queue:
            current, depth, path = queue.popleft()
            if depth >= max_hops:
                continue
            for neighbor, relation, chunk_id in self.adj.get(current, []):
                new_path = path + [f"--({relation})-->", neighbor]
                discovered_paths.append(" ".join(new_path))
                linked_chunk_ids.add(chunk_id)
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, depth + 1, new_path))

        return {
            "start_entity": start_entity,
            "max_hops": max_hops,
            "discovered_graph_paths": discovered_paths,
            "supporting_chunk_ids": sorted(linked_chunk_ids),
        }

    def to_dict(self) -> dict[str, list[list[str]]]:
        return {k: [list(edge) for edge in edges] for k, edges in self.adj.items()}

