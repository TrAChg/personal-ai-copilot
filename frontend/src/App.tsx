import { useState, useMemo } from 'react';
import { useLakehouseData } from './hooks/useLakehouseData';
import { Header } from './components/Header';
import { MetricsBar } from './components/MetricsBar';
import { TabsNav, type TabType } from './components/TabsNav';
import { SearchBar } from './components/SearchBar';
import { GraphView } from './components/GraphView';
import { ActivitiesTable } from './components/ActivitiesTable';
import { ChunksTable } from './components/ChunksTable';
import { RaptorTreeViewer } from './components/RaptorTreeViewer';
import { SnapshotsModal } from './components/SnapshotsModal';

export function App() {
  const { data, isConnected, isSyncing, triggerSync } = useLakehouseData();

  const [activeTab, setActiveTab] = useState<TabType>(() => {
    if (typeof window !== 'undefined') {
      const h = window.location.hash.replace('#', '').trim();
      if (h === 'activities' || h === 'chunks' || h === 'graph' || h === 'raptor') {
        return h as TabType;
      }
    }
    return 'graph';
  });

  const [searchQuery, setSearchQuery] = useState<string>('');
  const [isSnapshotsOpen, setIsSnapshotsOpen] = useState<boolean>(false);

  const handleSelectTab = (tab: TabType) => {
    setActiveTab(tab);
    if (typeof window !== 'undefined') {
      window.location.hash = tab;
    }
  };

  const filteredActivities = useMemo(() => {
    if (!data?.activities) return [];
    const q = searchQuery.toLowerCase().trim();
    if (!q) return data.activities;
    return data.activities.filter(
      (a) =>
        (a.event_id || '').toLowerCase().includes(q) ||
        (a.project_name || '').toLowerCase().includes(q) ||
        (a.target_file || '').toLowerCase().includes(q) ||
        (a.issue_or_task || '').toLowerCase().includes(q) ||
        (a.resolution_applied || '').toLowerCase().includes(q)
    );
  }, [data?.activities, searchQuery]);

  const filteredChunks = useMemo(() => {
    if (!data?.chunks) return [];
    const q = searchQuery.toLowerCase().trim();
    if (!q) return data.chunks;
    return data.chunks.filter(
      (c) =>
        (c.chunk_id || '').toLowerCase().includes(q) ||
        (c.title || '').toLowerCase().includes(q) ||
        (c.content || '').toLowerCase().includes(q) ||
        (c.category || '').toLowerCase().includes(q)
    );
  }, [data?.chunks, searchQuery]);

  return (
    <div className="min-h-screen p-5 md:p-7 max-w-[1700px] mx-auto">
      <Header
        isConnected={isConnected}
        isSyncing={isSyncing}
        snapshotCount={data?.snapshots?.length ?? 0}
        onSync={triggerSync}
        onOpenSnapshots={() => setIsSnapshotsOpen(true)}
      />

      <MetricsBar stats={data?.stats} />

      <TabsNav activeTab={activeTab} onSelectTab={handleSelectTab} />

      <SearchBar value={searchQuery} onChange={setSearchQuery} />

      <main>
        {activeTab === 'graph' && (
          <GraphView
            nodes={data?.nodes ?? []}
            edges={data?.edges ?? []}
            chunks={data?.chunks ?? []}
          />
        )}

        {activeTab === 'activities' && (
          <ActivitiesTable activities={filteredActivities} />
        )}

        {activeTab === 'chunks' && (
          <ChunksTable chunks={filteredChunks} />
        )}

        {activeTab === 'raptor' && (
          <RaptorTreeViewer chunks={data?.chunks ?? []} />
        )}
      </main>

      <SnapshotsModal
        isOpen={isSnapshotsOpen}
        snapshots={data?.snapshots ?? []}
        onClose={() => setIsSnapshotsOpen(false)}
      />
    </div>
  );
}

export default App;

