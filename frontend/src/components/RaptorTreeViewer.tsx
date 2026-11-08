import React, { useState } from 'react';
import { Layers, ChevronDown, ChevronRight, Hash } from 'lucide-react';
import type { KnowledgeChunk } from '../types/lakehouse';

interface RaptorTreeViewerProps {
  chunks: KnowledgeChunk[];
}

export const RaptorTreeViewer: React.FC<RaptorTreeViewerProps> = ({ chunks }) => {
  // 1. Level 2 Root node
  const l2Root = chunks.find((c) => c.raptor_level === 2);

  // 2. Level 1 Cluster nodes
  const l1Clusters = chunks.filter((c) => c.raptor_level === 1);

  // 3. Level 0 Leaf nodes
  const l0Leaves = chunks.filter((c) => (c.raptor_level ?? 0) === 0);

  // UI States
  const [isL2Expanded, setIsL2Expanded] = useState<boolean>(true);
  const [expandedL1Id, setExpandedL1Id] = useState<string | null>(null);

  React.useEffect(() => {
    if (expandedL1Id === null && l1Clusters.length > 0) {
      setExpandedL1Id(l1Clusters[0].chunk_id);
    }
  }, [l1Clusters, expandedL1Id]);

  const toggleL1 = (id: string) => {
    setExpandedL1Id((prev) => (prev === id ? null : id));
  };

  return (
    <div className="space-y-4">
      {/* Streamlined Header & Summary Stats */}
      <div className="bg-white border border-fr-border p-3.5 shadow-sm flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-2">
          <Layers className="w-5 h-5 text-fr-blue" />
          <h2 className="text-sm font-extrabold text-fr-navy uppercase tracking-wider">
            RAPTOR Hierarchical Tree
          </h2>
        </div>
        <div className="flex items-center gap-2 text-[11px] mono">
          <span className="px-2 py-0.5 bg-purple-50 text-purple-900 border border-purple-200 font-bold">
            Level 2: 1 Root
          </span>
          <span className="px-2 py-0.5 bg-blue-50 text-fr-navy border border-blue-200 font-bold">
            Level 1: {l1Clusters.length} Clusters
          </span>
          <span className="px-2 py-0.5 bg-emerald-50 text-emerald-900 border border-emerald-200 font-bold">
            Level 0: {l0Leaves.length} Leaf Chunks
          </span>
        </div>
      </div>

      {/* Visual 3-Tier Tree Explorer */}
      <div className="bg-white border-2 border-fr-navy shadow-sm overflow-hidden">
        {/* LEVEL 2: GLOBAL ROOT BAR */}
        {l2Root && (
          <div className="bg-gradient-to-r from-purple-900 via-fr-navy to-slate-900 text-white p-3.5">
            <div
              onClick={() => setIsL2Expanded(!isL2Expanded)}
              className="flex items-center justify-between cursor-pointer"
            >
              <div className="flex items-center gap-2.5">
                <span className="px-2 py-0.5 bg-purple-600 text-white text-[10px] font-extrabold uppercase mono tracking-wider border border-purple-300">
                  LEVEL 2 ROOT
                </span>
                <span className="text-xs font-extrabold tracking-wide text-white">
                  Architectural Knowledge Tree
                </span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-[10px] text-purple-200 mono">
                  {l1Clusters.length} Clusters Connected
                </span>
                {isL2Expanded ? (
                  <ChevronDown className="w-4 h-4 text-white" />
                ) : (
                  <ChevronRight className="w-4 h-4 text-white" />
                )}
              </div>
            </div>

            {/* L2 Summary */}
            {isL2Expanded && (
              <div className="mt-2 text-xs text-purple-100 font-sans leading-relaxed border-t border-purple-800/60 pt-2">
                {l2Root.content}
              </div>
            )}
          </div>
        )}

        {/* LEVEL 1 CLUSTERS LIST */}
        {isL2Expanded && (
          <div className="p-3.5 bg-slate-100 space-y-3">
            {l1Clusters.map((l1) => {
              const isL1Expanded = expandedL1Id === l1.chunk_id;
              const childLeaves = l0Leaves.filter(
                (leaf) => leaf.raptor_parent_l1 === l1.chunk_id
              );

              return (
                <div
                  key={l1.chunk_id}
                  className={`bg-white border transition-all ${
                    isL1Expanded
                      ? 'border-fr-blue shadow-sm ring-1 ring-fr-blue'
                      : 'border-fr-border hover:border-slate-400'
                  }`}
                >
                  {/* L1 Header Toggle */}
                  <div
                    onClick={() => toggleL1(l1.chunk_id)}
                    className="p-3 flex items-center justify-between cursor-pointer bg-slate-50 hover:bg-blue-50/50 transition-colors"
                  >
                    <div className="flex items-center gap-2 flex-wrap">
                      <span className="px-1.5 py-0.5 bg-fr-navy text-white text-[10px] font-extrabold uppercase mono">
                        L1
                      </span>
                      <span className="text-xs font-bold text-fr-navy">
                        {l1.title.replace(/^\[RAPTOR (Level-1 Summary|L1 Cluster)\]\s*/i, '').replace(/^[A-Za-z0-9_-]+:\s*/, '')}
                      </span>
                      <span className="px-1.5 py-0.5 bg-blue-100 text-fr-navy text-[10px] font-semibold border border-blue-200">
                        {l1.category}
                      </span>
                    </div>

                    <div className="flex items-center gap-3">
                      <span className="text-[10px] mono text-slate-500 font-bold">
                        {childLeaves.length} Chunks
                      </span>
                      <span className="text-xs font-bold text-fr-blue inline-flex items-center gap-1">
                        {isL1Expanded ? (
                          <ChevronDown className="w-4 h-4" />
                        ) : (
                          <ChevronRight className="w-4 h-4" />
                        )}
                      </span>
                    </div>
                  </div>

                  {/* L1 Summary */}
                  <div className="px-3 py-2 bg-blue-50/60 border-t border-b border-blue-100 text-xs text-slate-700 leading-relaxed">
                    {l1.content}
                  </div>

                  {/* LEVEL 0 LEAF CHUNKS — ONLY CHUNK NAMES */}
                  {isL1Expanded && (
                    <div className="p-3 bg-white">
                      <div className="text-[10px] font-bold text-slate-500 uppercase tracking-wider mb-2 flex items-center gap-1">
                        <Hash className="w-3.5 h-3.5 text-fr-blue" />
                        Leaf Chunks ({childLeaves.length}):
                      </div>

                      {childLeaves.length > 0 ? (
                        <div className="flex flex-wrap gap-1.5">
                          {childLeaves.map((leaf) => (
                            <span
                              key={leaf.chunk_id}
                              title={leaf.title}
                              className="inline-flex items-center gap-1.5 px-2 py-1 bg-slate-50 border border-slate-200 text-[11px] mono text-fr-navy font-semibold hover:border-fr-blue hover:bg-blue-50/60 transition-colors select-all"
                            >
                              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 shrink-0"></span>
                              {leaf.chunk_id}
                            </span>
                          ))}
                        </div>
                      ) : (
                        <div className="p-2 text-center text-xs text-slate-400">
                          No leaf chunks connected.
                        </div>
                      )}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
};
