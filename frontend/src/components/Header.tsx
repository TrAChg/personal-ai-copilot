import React from 'react';
import { RefreshCw, Camera } from 'lucide-react';

interface HeaderProps {
  isConnected: boolean;
  isSyncing: boolean;
  snapshotCount: number;
  onSync: () => void;
  onOpenSnapshots: () => void;
}

export const Header: React.FC<HeaderProps> = ({
  isConnected,
  isSyncing,
  snapshotCount,
  onSync,
  onOpenSnapshots,
}) => {
  return (
    <header className="flex flex-col md:flex-row justify-between items-start md:items-end border-b-[3px] border-fr-navy pb-3 mb-4 gap-3">
      <div>
        <h1 className="text-xl font-extrabold text-fr-navy uppercase tracking-tight flex items-center">
          GraphRAG &amp; Engineering Lakehouse
          <span className="ml-2 px-2 py-0.5 text-[11px] font-bold bg-fr-navy text-white tracking-wider">
            REACT SPA
          </span>
        </h1>
        <p className="text-xs text-fr-muted font-semibold mt-0.5">
          Long-Term Memory &amp; Audit Logs
        </p>
      </div>

      <div className="flex flex-col items-start md:items-end text-xs font-bold text-fr-navy gap-1.5 self-stretch md:self-auto">
        <div className="flex items-center gap-2">
          <span>
            LIVE STORE: <code className="mono font-bold text-fr-blue bg-blue-50 px-1 py-0.5 border border-blue-200">data/</code>
          </span>
          <span className="text-slate-300">|</span>
          <span className="inline-flex items-center gap-1.5">
            <span
              className={`w-2 h-2 inline-block ${isConnected ? 'bg-emerald-500 animate-pulse' : 'bg-slate-400'
                }`}
            />
            <span className={isConnected ? 'text-fr-blue font-extrabold' : 'text-fr-muted'}>
              {isConnected ? 'LIVE REFRESH (PORT 8765)' : 'OFFLINE / RECONNECTING'}
            </span>
          </span>
        </div>

        <div className="flex items-center gap-2 mt-1">
          <button
            onClick={onSync}
            disabled={isSyncing}
            className="flex items-center gap-1 px-3 py-1 text-[11px] font-extrabold bg-fr-navy text-white hover:bg-slate-800 disabled:opacity-60 transition-colors uppercase border border-fr-navy"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${isSyncing ? 'animate-spin' : ''}`} />
            {isSyncing ? 'Syncing...' : 'Sync DAG'}
          </button>

          <button
            onClick={onOpenSnapshots}
            className="flex items-center gap-1 px-3 py-1 text-[11px] font-extrabold bg-fr-blue text-white hover:bg-blue-700 transition-colors uppercase border border-fr-blue"
          >
            <Camera className="w-3.5 h-3.5" />
            View Snapshots ({snapshotCount})
          </button>
        </div>
      </div>
    </header>
  );
};

