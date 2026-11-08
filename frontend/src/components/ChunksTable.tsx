import React, { useState } from 'react';
import { ChevronDown, ChevronRight, Folder, Database, Network, Calendar, CheckCircle } from 'lucide-react';
import type { KnowledgeChunk } from '../types/lakehouse';

interface ChunksTableProps {
  chunks: KnowledgeChunk[];
}

export const ChunksTable: React.FC<ChunksTableProps> = ({ chunks }) => {
  // Filter for raw knowledge chunks (Level 0) - RAPTOR summaries are in Tab 4
  const leafChunks = chunks.filter((c) => (c.raptor_level ?? 0) === 0);

  const [expandedId, setExpandedId] = useState<string | null>(() => {
    return leafChunks.length > 0 ? leafChunks[0].chunk_id : null;
  });

  const toggleExpand = (chunkId: string) => {
    setExpandedId((prev) => (prev === chunkId ? null : chunkId));
  };

  const formatFolder = (category: string) => {
    return category
      .replace(/_/g, ' ')
      .toUpperCase();
  };

  return (
    <div className="bg-white border border-fr-border overflow-x-auto">
      <table className="w-full border-collapse text-xs text-left">
        <thead>
          <tr className="bg-fr-navy text-white text-[11px] font-bold uppercase tracking-wider">
            <th className="p-2 border-r border-blue-900 w-[140px]">Chunk ID</th>
            <th className="p-2 border-r border-blue-900">
              Folder in Documents &amp; Knowledge Title (Click to Expand Markdown Content)
            </th>
            <th className="p-2 border-r border-blue-900 w-[180px]">Graph Entities</th>
            <th className="p-2 border-r border-blue-900 w-[95px]">Created</th>
            <th className="p-2 w-[85px]">Status</th>
          </tr>
        </thead>
        <tbody id="tb-chunks" className="divide-y divide-slate-200">
          {leafChunks.map((c) => {
            const isExpanded = expandedId === c.chunk_id;
            const folderName = formatFolder(c.category || 'general');

            return (
              <React.Fragment key={c.chunk_id}>
                {/* Main Row */}
                <tr
                  onClick={() => toggleExpand(c.chunk_id)}
                  className={`cursor-pointer transition-colors ${
                    isExpanded ? 'bg-blue-50/60' : 'hover:bg-slate-50'
                  }`}
                >
                  <td className="p-2 mono font-bold text-fr-navy border-r border-slate-200 align-top">
                    {c.chunk_id}
                  </td>
                  <td className="p-2 border-r border-slate-200 align-top">
                    <div className="flex items-center gap-2 flex-wrap">
                      {/* Folder Name from documents */}
                      <span className="inline-flex items-center gap-1 px-2 py-0.5 text-[10px] font-extrabold bg-blue-100 text-fr-navy border border-fr-blue uppercase">
                        <Folder className="w-3 h-3 text-fr-navy" />
                        {folderName}
                      </span>
                      <strong className="text-fr-navy text-xs">{c.title}</strong>
                      <span className="ml-auto inline-flex items-center gap-1 text-[10px] font-bold text-fr-blue hover:underline">
                        {isExpanded ? (
                          <>
                            <ChevronDown className="w-3 h-3" /> Hide Details
                          </>
                        ) : (
                          <>
                            <ChevronRight className="w-3 h-3" /> Click to View Content
                          </>
                        )}
                      </span>
                    </div>

                    {!isExpanded && (
                      <div className="text-slate-500 text-[11px] mt-1 line-clamp-1">
                        {c.content.length > 120
                          ? c.content.substring(0, 120) + '...'
                          : c.content}
                      </div>
                    )}
                  </td>
                  <td className="p-2 border-r border-slate-200 align-top">
                    <div className="flex flex-wrap gap-1">
                      {c.entities && c.entities.length > 0 ? (
                        c.entities.slice(0, 3).map((e) => (
                          <span
                            key={e}
                            className="inline-block px-1.5 py-0.2 text-[9px] font-bold bg-slate-100 text-slate-700 border border-slate-300"
                          >
                            {e.replace(/_/g, ' ')}
                          </span>
                        ))
                      ) : (
                        <span className="text-slate-400 text-[10px]">No entities</span>
                      )}
                      {c.entities && c.entities.length > 3 && (
                        <span className="text-[9px] text-slate-500 font-bold">
                          +{c.entities.length - 3}
                        </span>
                      )}
                    </div>
                  </td>
                  <td className="p-2 mono text-slate-600 border-r border-slate-200 align-top">
                    {c.created_date}
                  </td>
                  <td className="p-2 align-top">
                    <span
                      className={`inline-block px-1.5 py-0.5 text-[10px] font-bold uppercase border ${
                        c.is_latest
                          ? 'bg-emerald-50 text-emerald-700 border-emerald-500'
                          : 'bg-slate-100 text-slate-500 border-slate-300'
                      }`}
                    >
                      {c.is_latest ? 'LATEST' : 'ARCHIVED'}
                    </span>
                  </td>
                </tr>

                {/* Expanded Detailed Content */}
                {isExpanded && (
                  <tr className="bg-gradient-to-r from-blue-50/80 via-slate-50 to-white">
                    <td colSpan={5} className="p-4 border-b-2 border-fr-navy">
                      <div className="bg-white border border-fr-border p-4 shadow-sm">
                        {/* Header Banner */}
                        <div className="flex items-center justify-between pb-3 mb-3 border-b border-slate-200 flex-wrap gap-2">
                          <div className="flex items-center gap-2">
                            <span className="px-2 py-0.5 bg-fr-navy text-white text-[10px] font-extrabold uppercase mono">
                              {c.chunk_id}
                            </span>
                            <span className="px-2 py-0.5 bg-blue-50 text-fr-navy border border-fr-blue text-[10px] font-extrabold uppercase">
                              📁 Folder: {folderName}
                            </span>
                            <span className="text-xs font-bold text-fr-navy">
                              {c.title}
                            </span>
                          </div>

                          <div className="flex items-center gap-2 text-[10px] mono">
                            <span className="inline-flex items-center gap-1 px-1.5 py-0.5 bg-emerald-50 text-emerald-700 border border-emerald-300 font-bold">
                              <Database className="w-3 h-3 text-emerald-600" /> ChromaDB HNSW Vectorized
                            </span>
                            <span className="inline-flex items-center gap-1 text-slate-500">
                              <Calendar className="w-3 h-3" /> {c.created_date}
                            </span>
                          </div>
                        </div>

                        {/* Full Technical Content */}
                        <div className="mb-4">
                          <div className="text-[10px] font-extrabold text-fr-navy uppercase tracking-wider mb-1.5 flex items-center gap-1">
                            <CheckCircle className="w-3.5 h-3.5 text-emerald-600" />
                            Full Markdown Content (Synchronized from Documents &amp; ChromaDB):
                          </div>
                          <div className="p-3.5 bg-slate-50 border border-slate-300 text-xs text-slate-800 leading-relaxed font-sans whitespace-pre-wrap selection:bg-blue-100">
                            {c.content}
                          </div>
                        </div>

                        {/* Extracted Graph Relationships & Entities */}
                        {c.entities && c.entities.length > 0 && (
                          <div className="pt-3 border-t border-slate-200">
                            <div className="text-[10px] font-extrabold text-fr-navy uppercase tracking-wider mb-2 flex items-center gap-1">
                              <Network className="w-3.5 h-3.5 text-fr-blue" />
                              GraphRAG Connected Entity Nodes ({c.entities.length}):
                            </div>
                            <div className="flex flex-wrap gap-1.5">
                              {c.entities.map((ent) => (
                                <span
                                  key={ent}
                                  className="inline-flex items-center gap-1 px-2 py-0.5 text-[10px] font-bold bg-white text-fr-navy border border-fr-blue shadow-xs"
                                >
                                  🔹 {ent.replace(/_/g, ' ')}
                                </span>
                              ))}
                            </div>
                          </div>
                        )}
                      </div>
                    </td>
                  </tr>
                )}
              </React.Fragment>
            );
          })}
        </tbody>
      </table>
    </div>
  );
};
