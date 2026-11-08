import React from 'react';

export type TabType = 'graph' | 'activities' | 'chunks' | 'raptor';

interface TabsNavProps {
  activeTab: TabType;
  onSelectTab: (tab: TabType) => void;
}

export const TabsNav: React.FC<TabsNavProps> = ({ activeTab, onSelectTab }) => {
  const tabs: { id: TabType; label: string }[] = [
    { id: 'graph', label: '1. Knowledge Graph (GraphRAG)' },
    { id: 'activities', label: '2. Engineering Activity Lakehouse' },
    { id: 'chunks', label: '3. Technical Knowledge Chunks' },
    { id: 'raptor', label: '4. RAPTOR Hierarchical Trees' },
  ];

  return (
    <div className="flex border-b border-fr-border mb-3.5">
      {tabs.map((t) => {
        const isActive = activeTab === t.id;
        return (
          <button
            key={t.id}
            onClick={() => onSelectTab(t.id)}
            className={`px-4 py-2 text-xs font-extrabold uppercase tracking-wider mr-1 -mb-[1px] border border-b-0 transition-colors ${
              isActive
                ? 'bg-fr-navy text-white border-fr-navy'
                : 'bg-transparent text-fr-navy border-transparent hover:bg-slate-100'
            }`}
          >
            {t.label}
          </button>
        );
      })}
    </div>
  );
};

