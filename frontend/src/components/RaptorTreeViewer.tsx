import React, { useState } from 'react';
import { GitBranch, Layers, ChevronDown, ChevronRight, FileText, Network, CheckCircle, Database } from 'lucide-react';
import type { KnowledgeChunk } from '../types/lakehouse';

interface RaptorTreeViewerProps {
  chunks: KnowledgeChunk[];
}

export const RaptorTreeViewer: React.FC<RaptorTreeViewerProps> = ({ chunks }) => {
  const raptorSummaries = chunks
    .filter((c) => (c.raptor_level ?? 0) > 0)
    .sort((a, b) => (b.raptor_level ?? 0) - (a.raptor_level ?? 0));

  const leafChunks = chunks.filter((c) => (c.raptor_level ?? 0) === 0);

  const [expandedId, setExpandedId] = useState<string | null>(() => {
    return raptorSummaries.length > 0 ? raptorSummaries[0].chunk_id : null;
  });

  const toggleExpand = (id: string) => {
    setExpandedId((prev) => (prev === id ? null : id));
  };

  return (
    <div className="space-y-6">
      {/* RAPTOR Architecture Header */}
      <div className="bg-white border border-fr-border p-4 shadow-sm">
        <div className="flex items-center justify-between pb-3 border-b border-fr-hairline">
          <div className="flex items-center gap-2">
            <Layers className="w-5 h-5 text-fr-blue" />
            <h2 className="text-sm font-extrabold text-fr-navy uppercase tracking-wider">
              RAPTOR (Recursive Abstractive Processing for Tree-Organized Retrieval)
            </h2>
          </div>
          <span className="px-2 py-0.5 bg-blue-100 text-fr-navy text-[11px] font-bold uppercase mono border border-fr-blue">
            Multi-Layer Abstractive Hierarchy
          </span>
        </div>
        <p className="text-xs text-slate-600 mt-2.5 leading-relaxed">
          RAPTOR builds a hierarchical multi-scale tree over your technical documents. Level 0 raw knowledge chunks are semantically clustered and recursively summarized into Level 1 domain syntheses, which roll up into Level 2 global architectural roots. When you query the system, retrieval traverses both high-level thematic summaries and low-level granular details simultaneously.
        </p>

        {/* Tree Overview Pills */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3 mt-4 text-xs">
          <div className="p-3 bg-slate-50 border border-slate-200">
            <span className="px-1.5 py-0.5 bg-purple-100 text-purple-800 text-[10px] font-extrabold uppercase border border-purple-300">
              Level 2: Global Root
            </span>
            <div className="font-bold text-fr-navy mt-1">Global Vault Synthesis</div>
            <div className="text-[11px] text-slate-500 mt-0.5">
              Rolls up multi-domain architectures across all projects.
            </div>
          </div>
          <div className="p-3 bg-slate-50 border border-slate-200">
            <span className="px-1.5 py-0.5 bg-blue-100 text-fr-blue text-[10px] font-extrabold uppercase border border-fr-blue">
              Level 1: Cluster Nodes
            </span>
            <div className="font-bold text-fr-navy mt-1">Domain Summaries</div>
            <div className="text-[11px] text-slate-500 mt-0.5">
              Synthesizes focused technical domains (GenAI, ML, Lakehouse).
            </div>
          </div>
          <div className="p-3 bg-slate-50 border border-slate-200">
            <span className="px-1.5 py-0.5 bg-emerald-100 text-emerald-800 text-[10px] font-extrabold uppercase border border-emerald-300">
              Level 0: Leaf Nodes ({leafChunks.length})
            </span>
            <div className="font-bold text-fr-navy mt-1">Raw Document Chunks</div>
            <div className="text-[11px] text-slate-500 mt-0.5">
              Granular Markdown notes from <code>data/documents/</code>.
            </div>
          </div>
        </div>
      </div>

      {/* RAPTOR Hierarchical Trees List */}
      <div className="space-y-4">
        {raptorSummaries.map((r) => {
          const isExpanded = expandedId === r.chunk_id;
          const isLevel2 = r.raptor_level === 2;

          return (
            <div
              key={r.chunk_id}
              className={`bg-white border-2 transition-all shadow-sm ${
                isExpanded ? 'border-fr-navy ring-1 ring-fr-navy' : 'border-fr-border hover:border-slate-400'
              }`}
            >
              {/* Collapsed / Card Header */}
              <div
                onClick={() => toggleExpand(r.chunk_id)}
                className="p-3.5 flex items-center justify-between cursor-pointer bg-slate-50 hover:bg-blue-50/40 transition-colors"
              >
                <div className="flex items-center gap-3 flex-wrap">
                  <span
                    className={`px-2 py-0.5 text-[11px] font-extrabold uppercase mono border ${
                      isLevel2
                        ? 'bg-purple-700 text-white border-purple-900'
                        : 'bg-fr-navy text-white border-blue-900'
                    }`}
                  >
                    Level {r.raptor_level} {isLevel2 ? 'Root' : 'Cluster'}
                  </span>
                  <span className="mono font-bold text-fr-navy text-xs">{r.chunk_id}</span>
                  <strong className="text-fr-navy text-xs">{r.title}</strong>
                </div>

                <div className="flex items-center gap-3">
                  <span className="text-[11px] mono text-slate-500">{r.created_date}</span>
                  <span className="inline-flex items-center gap-1 text-xs font-bold text-fr-blue">
                    {isExpanded ? (
                      <>
                        <ChevronDown className="w-4 h-4" /> Close Tree
                      </>
                    ) : (
                      <>
                        <ChevronRight className="w-4 h-4" /> View Tree Architecture
                      </>
                    )}
                  </span>
                </div>
              </div>

              {/* Expanded Detail Architecture */}
              {isExpanded && (
                <div className="p-5 border-t border-fr-border bg-white space-y-5">
                  {/* Synthesis Box */}
                  <div>
                    <div className="text-[11px] font-extrabold text-fr-navy uppercase tracking-wider mb-1.5 flex items-center gap-1">
                      <CheckCircle className="w-4 h-4 text-emerald-600" />
                      Abstractive Summary Synthesis:
                    </div>
                    <div className="p-3.5 bg-blue-50/70 border border-fr-blue text-xs text-slate-800 leading-relaxed font-sans">
                      {r.content}
                    </div>
                  </div>

                  {/* Visual Tree Diagram */}
                  <div>
                    <div className="text-[11px] font-extrabold text-fr-navy uppercase tracking-wider mb-2 flex items-center gap-1">
                      <GitBranch className="w-4 h-4 text-fr-navy" />
                      Hierarchical Tree Roll-Up Architecture:
                    </div>

                    <div className="p-4 bg-slate-100 border border-slate-300 flex flex-col items-center">
                      {/* Top Node */}
                      <div className="px-4 py-2 bg-fr-navy text-white text-xs font-bold uppercase shadow-sm border border-blue-900 text-center max-w-lg">
                        <div className="text-[10px] text-emerald-400 font-mono">
                          RAPTOR LEVEL {r.raptor_level} SUMMARY NODE
                        </div>
                        <div>{r.title}</div>
                      </div>

                      {/* Tree Stem */}
                      <div className="w-0.5 h-6 bg-fr-navy"></div>

                      {/* Children Tier */}
                      <div className="w-full max-w-2xl border-t-2 border-fr-navy pt-3 flex justify-around flex-wrap gap-2">
                        {r.entities?.map((ent) => (
                          <div
                            key={ent}
                            className="flex flex-col items-center"
                          >
                            <div className="w-0.5 h-3 bg-fr-navy -mt-3"></div>
                            <div className="px-2.5 py-1 bg-white text-fr-navy border border-fr-border text-[10px] font-bold shadow-xs">
                              {ent.replace(/_/g, ' ')}
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>

                  {/* Child Entities & Knowledge Roll-Up */}
                  {r.entities && r.entities.length > 0 && (
                    <div className="pt-2">
                      <div className="text-[11px] font-extrabold text-fr-navy uppercase tracking-wider mb-2 flex items-center gap-1">
                        <Network className="w-4 h-4 text-fr-blue" />
                        Connected GraphRAG Entity Clusters ({r.entities.length}):
                      </div>
                      <div className="flex flex-wrap gap-2">
                        {r.entities.map((e) => (
                          <span
                            key={e}
                            className="inline-flex items-center gap-1 px-2.5 py-1 text-[11px] font-bold bg-slate-50 text-fr-navy border border-fr-blue shadow-xs"
                          >
                            🔷 {e.replace(/_/g, ' ')}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Storage Status */}
                  <div className="pt-3 border-t border-slate-200 flex items-center justify-between text-[11px] mono text-slate-500">
                    <span className="flex items-center gap-1 text-emerald-700 font-bold">
                      <Database className="w-3.5 h-3.5" /> Vectorized &amp; Indexed in ChromaDB Tree Store
                    </span>
                    <span>Authority Rank: {r.raptor_level === 2 ? '5/5 (Root)' : '4/5 (Cluster)'}</span>
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};

