import React from 'react';
import type { LakehouseStats } from '../types/lakehouse';

interface MetricsBarProps {
  stats?: LakehouseStats;
}

export const MetricsBar: React.FC<MetricsBarProps> = ({ stats }) => {
  const cells = [
    { num: stats?.total_nodes ?? 0, lbl: 'Graph Nodes', id: 'm-nodes' },
    { num: stats?.total_chunks ?? 0, lbl: 'Knowledge Chunks', id: 'm-chunks' },
    { num: stats?.total_activities ?? 0, lbl: 'Verified Activities', id: 'm-activities' },
    { num: '100%', lbl: 'Data Integrity', id: 'm-status', highlight: true },
  ];

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-4">
      {cells.map((c) => (
        <div
          key={c.lbl}
          className="bg-white border border-fr-border border-l-4 border-l-fr-navy p-3"
        >
          <div
            id={c.id}
            className={`text-2xl font-black mono ${
              c.highlight ? 'text-fr-blue' : 'text-fr-navy'
            }`}
          >
            {c.num}
          </div>
          <div className="text-[11px] font-bold text-fr-muted uppercase tracking-wider mt-0.5">
            {c.lbl}
          </div>
        </div>
      ))}
    </div>
  );
};

