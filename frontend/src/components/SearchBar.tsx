import React from 'react';
import { Search } from 'lucide-react';

interface SearchBarProps {
  value: string;
  onChange: (value: string) => void;
}

export const SearchBar: React.FC<SearchBarProps> = ({ value, onChange }) => {
  return (
    <div className="relative mb-3.5">
      <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
        <Search className="h-4 w-4 text-fr-muted" />
      </div>
      <input
        type="text"
        id="globalSearch"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="Search events, commits, tasks, files, concepts, or subagents in real-time..."
        className="w-full bg-white border border-fr-border text-fr-navy pl-9 pr-3 py-2 text-xs font-semibold placeholder-slate-400 focus:outline-none focus:border-fr-blue"
      />
    </div>
  );
};

