import React, { useEffect, useRef, useState } from 'react';
import { Network, DataSet } from 'vis-network/standalone/esm/vis-network';
import { X, ArrowRight, ArrowLeft } from 'lucide-react';
import type { GraphNode, GraphEdge, KnowledgeChunk } from '../types/lakehouse';

interface GraphViewProps {
  nodes: GraphNode[];
  edges: GraphEdge[];
  chunks: KnowledgeChunk[];
}

export const GraphView: React.FC<GraphViewProps> = ({ nodes, edges, chunks }) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const networkRef = useRef<Network | null>(null);
  const vNodesRef = useRef<DataSet<any> | null>(null);
  const vEdgesRef = useRef<DataSet<any> | null>(null);

  const [selectedNode, setSelectedNode] = useState<string | null>(null);

  useEffect(() => {
    if (!containerRef.current) return;

    const nodeItems = nodes.map((n) => ({
      id: n.id,
      label: n.label,
      shape: 'box',
      borderWidth: 1.5,
      color: {
        background: '#FFFFFF',
        border: '#002654',
        highlight: { background: '#0055A5', border: '#002654' },
      },
      font: { color: '#002654', size: 11, face: 'Segoe UI', bold: true },
      margin: 7,
    }));

    const edgeItems = edges.map((e, idx) => ({
      id: `edge-${idx}`,
      from: e.from,
      to: e.to,
      label: e.label,
      arrows: 'to',
      font: { size: 8.5, color: '#0055A5', face: 'Consolas' },
      color: { color: '#002654', highlight: '#0055A5' },
      smooth: { type: 'continuous' },
    }));

    if (!networkRef.current) {
      const vNodes = new DataSet<any>(nodeItems);
      const vEdges = new DataSet<any>(edgeItems);
      vNodesRef.current = vNodes;
      vEdgesRef.current = vEdges;

      const opts: any = {
        physics: {
          barnesHut: {
            gravitationalConstant: -3200,
            centralGravity: 0.3,
            springLength: 130,
            springConstant: 0.05,
          },
          stabilization: { iterations: 90 },
        },
        interaction: { hover: true },
      };

      const network = new Network(
        containerRef.current,
        { nodes: vNodes as any, edges: vEdges as any },
        opts
      );
      network.on('click', (params) => {
        if (params.nodes && params.nodes.length > 0) {
          setSelectedNode(String(params.nodes[0]));
        }
      });
      networkRef.current = network;
    } else {
      if (vNodesRef.current && vEdgesRef.current) {
        vNodesRef.current.clear();
        vNodesRef.current.add(nodeItems);
        vEdgesRef.current.clear();
        vEdgesRef.current.add(edgeItems);
      }
    }
  }, [nodes, edges]);

  const connectedEdges = selectedNode
    ? edges.filter((e) => e.from === selectedNode || e.to === selectedNode)
    : [];

  const relatedChunks = selectedNode
    ? chunks.filter(
        (c) =>
          (c.entities || []).includes(selectedNode) ||
          (c.content || '').toLowerCase().includes(selectedNode.toLowerCase())
      )
    : [];

  return (
    <div className="relative w-full h-[580px] bg-white border border-fr-border">
      <div id="graph-box" ref={containerRef} className="w-full h-full" />

      {selectedNode && (
        <div className="absolute right-3 top-3 w-80 bg-white border-2 border-fr-navy p-3.5 text-xs max-h-[540px] overflow-y-auto shadow-sm z-10">
          <div className="flex justify-between items-center border-b border-fr-hairline pb-2 mb-2">
            <h3 className="font-extrabold text-fr-navy uppercase text-sm mono">
              {selectedNode}
            </h3>
            <button
              onClick={() => setSelectedNode(null)}
              className="text-fr-navy hover:text-fr-blue font-bold p-1"
            >
              <X className="w-4 h-4" />
            </button>
          </div>

          <div className="text-[11px] font-bold text-fr-muted uppercase mb-1">
            Connected Edges ({connectedEdges.length})
          </div>
          <div className="space-y-1 mb-3 text-xs">
            {connectedEdges.length > 0 ? (
              connectedEdges.map((e, idx) => (
                <div key={idx} className="flex items-center gap-1.5 text-slate-700">
                  {e.from === selectedNode ? (
                    <>
                      <ArrowRight className="w-3 h-3 text-fr-blue shrink-0" />
                      <span className="font-semibold">{e.label}</span>
                      <code className="mono text-xs bg-slate-100 px-1">{e.to}</code>
                    </>
                  ) : (
                    <>
                      <ArrowLeft className="w-3 h-3 text-fr-blue shrink-0" />
                      <code className="mono text-xs bg-slate-100 px-1">{e.from}</code>
                      <span className="font-semibold">{e.label}</span>
                    </>
                  )}
                </div>
              ))
            ) : (
              <div className="text-slate-400 italic">No direct connections.</div>
            )}
          </div>

          <div className="text-[11px] font-bold text-fr-muted uppercase mb-1">
            Linked Knowledge ({relatedChunks.length})
          </div>
          <div className="space-y-1.5">
            {relatedChunks.length > 0 ? (
              relatedChunks.map((c) => (
                <div
                  key={c.chunk_id}
                  className="p-2 bg-slate-50 border border-slate-200 text-xs"
                >
                  <div className="flex items-center gap-1.5 mb-1">
                    <span className="px-1.5 py-0.2 bg-fr-navy text-white text-[10px] font-bold uppercase mono">
                      {c.chunk_id}
                    </span>
                    <strong className="text-fr-navy text-xs truncate">{c.title}</strong>
                  </div>
                  <p className="text-[11px] text-slate-600 line-clamp-3 leading-snug">
                    {c.content}
                  </p>
                </div>
              ))
            ) : (
              <div className="text-slate-400 text-[11px] italic">Core graph entity.</div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
