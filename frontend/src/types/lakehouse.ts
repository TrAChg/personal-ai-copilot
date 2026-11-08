export interface GraphNode {
  id: string;
  label: string;
}

export interface GraphEdge {
  from: string;
  to: string;
  label: string;
  chunk_id: string;
}

export interface KnowledgeChunk {
  chunk_id: string;
  title: string;
  content: string;
  category: string;
  raptor_level: number;
  created_date: string;
  is_latest: boolean;
  entities?: string[];
}

export interface ActivityLog {
  event_id: string;
  event_date: string;
  project_name: string;
  activity_type: string;
  target_file: string;
  issue_or_task: string;
  resolution_applied: string;
  tests_passed: number;
  status: string;
}

export interface SnapshotMeta {
  name: string;
  folder?: string;
  rel_path: string;
  size_kb: number;
}

export interface LakehouseStats {
  total_nodes: number;
  total_edges: number;
  total_chunks: number;
  active_chunks: number;
  total_activities: number;
  total_snapshots: number;
  chroma_vectors: number;
}

export interface LakehousePayload {
  version: string;
  updated_at: string;
  nodes: GraphNode[];
  edges: GraphEdge[];
  chunks: KnowledgeChunk[];
  activities: ActivityLog[];
  snapshots: SnapshotMeta[];
  stats: LakehouseStats;
}

