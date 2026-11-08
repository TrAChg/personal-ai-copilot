import React, { useState, useMemo } from 'react';
import { X, Folder, CheckCircle, Image as ImageIcon } from 'lucide-react';
import type { SnapshotMeta } from '../types/lakehouse';

interface SnapshotsModalProps {
  isOpen: boolean;
  snapshots: SnapshotMeta[];
  onClose: () => void;
}

export const SnapshotsModal: React.FC<SnapshotsModalProps> = ({
  isOpen,
  snapshots,
  onClose,
}) => {
  // Extract distinct project folders (e.g. personal_copilot, house_price_prediction, etc.)
  const folders = useMemo(() => {
    const set = new Set<string>();
    snapshots.forEach((s) => {
      if (s.folder && s.folder !== 'general') {
        set.add(s.folder);
      }
    });
    const list = Array.from(set).sort();
    if (list.length === 0 && snapshots.some((s) => s.folder === 'general')) {
      return ['general'];
    }
    return list;
  }, [snapshots]);

  // Default to the first actual project folder (NO redundant "all_snapshots")
  const [selectedFolder, setSelectedFolder] = useState<string>('');

  const activeFolder = selectedFolder && folders.includes(selectedFolder)
    ? selectedFolder
    : (folders[0] || '');

  const [selectedIdx, setSelectedIdx] = useState<number>(0);

  // Filter snapshots strictly by the selected project folder
  const projectSnapshots = useMemo(() => {
    return snapshots.filter((s) => (s.folder || 'general') === activeFolder);
  }, [snapshots, activeFolder]);

  const activeIdx = Math.min(selectedIdx, Math.max(0, projectSnapshots.length - 1));
  const current = projectSnapshots[activeIdx];

  const formatButtonLabel = (name: string) => {
    return name
      .replace('.png', '')
      .replace('functional_test_verified_', '')
      .replace('lakehouse_viewer_', '')
      .replace(/_/g, ' ')
      .toUpperCase();
  };

  const formatFolderLabel = (f: string) => {
    return f.replace(/_/g, ' ').toUpperCase();
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-[#002654]/70 z-50 flex items-center justify-center p-4">
      <div className="bg-white border-2 border-fr-navy w-11/12 max-w-5xl max-h-[92vh] flex flex-col overflow-hidden shadow-2xl">
        {/* Header */}
        <div className="flex justify-between items-center bg-fr-navy text-white px-4 py-2.5">
          <div className="flex items-center gap-2">
            <ImageIcon className="w-4 h-4 text-emerald-400" />
            <span className="font-extrabold text-xs uppercase tracking-wide">
              Project Snapshots Explorer (Divided by Project Folder)
            </span>
          </div>
          <button
            onClick={onClose}
            className="text-white hover:text-slate-300 font-bold p-1 text-sm"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {snapshots.length > 0 ? (
          <>
            {/* Project Folders Navigation (NO "all_snapshots" button) */}
            <div className="flex items-center gap-1.5 px-4 py-2.5 bg-slate-200 border-b border-fr-border overflow-x-auto text-xs">
              <span className="font-extrabold uppercase tracking-wider text-[10px] text-fr-navy mr-1 flex items-center gap-1 shrink-0">
                <Folder className="w-3.5 h-3.5 text-fr-navy" /> Project Folders:
              </span>
              {folders.map((f) => {
                const count = snapshots.filter((s) => (s.folder || 'general') === f).length;
                const isSelected = activeFolder === f;
                return (
                  <button
                    key={f}
                    onClick={() => {
                      setSelectedFolder(f);
                      setSelectedIdx(0);
                    }}
                    className={`px-3 py-1.5 text-[11px] font-extrabold uppercase transition-colors shrink-0 flex items-center gap-1.5 border ${
                      isSelected
                        ? 'bg-fr-navy text-white border-fr-navy shadow-xs'
                        : 'bg-white text-fr-navy border-fr-border hover:bg-slate-100'
                    }`}
                  >
                    <Folder className={`w-3.5 h-3.5 ${isSelected ? 'text-blue-300' : 'text-fr-blue'}`} />
                    📁 {formatFolderLabel(f)} ({count})
                  </button>
                );
              })}
            </div>

            {/* Individual Snapshot Selector for Active Project */}
            <div className="flex gap-1.5 px-4 py-2 border-b border-fr-border bg-slate-50 overflow-x-auto items-center">
              <span className="text-[10px] font-bold uppercase tracking-wider text-slate-500 mr-1 shrink-0">
                Verified Views:
              </span>
              {projectSnapshots.map((s, idx) => (
                <button
                  key={s.rel_path}
                  onClick={() => setSelectedIdx(idx)}
                  className={`px-3 py-1 text-[11px] font-bold uppercase transition-colors shrink-0 flex items-center gap-1.5 border ${
                    activeIdx === idx
                      ? 'bg-fr-blue text-white border-fr-blue'
                      : 'bg-white text-fr-navy border-fr-border hover:bg-slate-200'
                  }`}
                >
                  <CheckCircle className={`w-3 h-3 ${activeIdx === idx ? 'text-white' : 'text-emerald-600'}`} />
                  {formatButtonLabel(s.name)} ({s.size_kb} KB)
                </button>
              ))}
            </div>

            {/* Visual Preview */}
            <div className="p-4 overflow-y-auto flex-1 text-center bg-slate-100 flex flex-col items-center justify-center">
              {current && (
                <>
                  <img
                    src={`/${current.rel_path}`}
                    alt={current.name}
                    className="max-w-full max-h-[62vh] border border-fr-border shadow-sm object-contain bg-white"
                  />
                  <div className="mt-2.5 text-xs mono text-fr-muted font-semibold flex items-center gap-3 flex-wrap justify-center">
                    <span className="px-2 py-0.5 bg-blue-100 text-fr-navy border border-fr-blue uppercase text-[10px] font-extrabold flex items-center gap-1">
                      <Folder className="w-3 h-3" /> Folder: {current.folder || 'general'}
                    </span>
                    <span className="font-bold text-fr-navy">{current.name}</span>
                    <span>{current.size_kb} KB</span>
                    <span className="text-slate-400">({current.rel_path})</span>
                  </div>
                </>
              )}
            </div>
          </>
        ) : (
          <div className="p-8 text-center text-sm text-fr-muted">
            No snapshots found. Run <code className="mono font-bold">python run_copilot.py --audit-web</code> to capture visual UI snapshots.
          </div>
        )}
      </div>
    </div>
  );
};
