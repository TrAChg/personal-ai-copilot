import { useState, useEffect, useCallback, useRef } from 'react';
import type { LakehousePayload } from '../types/lakehouse';

export function useLakehouseData() {
  const [data, setData] = useState<LakehousePayload | null>(null);
  const [isConnected, setIsConnected] = useState<boolean>(false);
  const [isSyncing, setIsSyncing] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const lastVersionRef = useRef<string>('');

  const getEndpoint = useCallback((path: string) => {
    if (typeof window !== 'undefined' && (window.location.protocol === 'http:' || window.location.protocol === 'https:')) {
      return path;
    }
    return `http://localhost:8765${path}`;
  }, []);

  const fetchData = useCallback(async (force = false) => {
    try {
      const endpoint = getEndpoint('/api/data');
      const res = await fetch(endpoint, { cache: 'no-store' });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const json: LakehousePayload = await res.json();

      setIsConnected(true);
      setError(null);

      if (force || json.version !== lastVersionRef.current) {
        lastVersionRef.current = json.version;
        setData(json);
      }
    } catch (err: any) {
      setIsConnected(false);
      setError(err?.message || 'Server unreachable');
    }
  }, [getEndpoint]);

  const triggerSync = useCallback(async () => {
    setIsSyncing(true);
    try {
      const endpoint = getEndpoint('/api/sync');
      const res = await fetch(endpoint, { method: 'POST' });
      if (!res.ok) throw new Error(`Sync HTTP ${res.status}`);
      await fetchData(true);
    } catch (err: any) {
      alert(`Sync failed: ${err?.message || err}. Ensure live_server is running.`);
    } finally {
      setIsSyncing(false);
    }
  }, [getEndpoint, fetchData]);

  useEffect(() => {
    fetchData(true);
    const interval = setInterval(() => fetchData(false), 3500);

    const handleFocus = () => fetchData(false);
    window.addEventListener('focus', handleFocus);

    return () => {
      clearInterval(interval);
      window.removeEventListener('focus', handleFocus);
    };
  }, [fetchData]);

  return {
    data,
    isConnected,
    isSyncing,
    error,
    triggerSync,
    refetch: () => fetchData(true),
  };
}

