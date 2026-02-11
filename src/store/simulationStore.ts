import { create } from 'zustand';

export interface LogEntry {
  id: string;
  timestamp: string;
  source: string;
  message: string;
  level: 'info' | 'warning' | 'error' | 'success';
}

interface SimulationState {
  logs: LogEntry[];
  activeNode: string | null; // e.g., 'gateway', 'firewall', 'ai', 'tools'
  addLog: (log: Omit<LogEntry, 'id' | 'timestamp'>) => void;
  setActiveNode: (node: string | null) => void;
  clearLogs: () => void;
}

export const useSimulationStore = create<SimulationState>((set) => ({
  logs: [],
  activeNode: null,
  addLog: (log) => set((state) => ({
    logs: [
      {
        id: crypto.randomUUID(),
        timestamp: new Date().toLocaleTimeString(),
        ...log,
      },
      ...state.logs,
    ],
  })),
  setActiveNode: (node) => set({ activeNode: node }),
  clearLogs: () => set({ logs: [] }),
}));
