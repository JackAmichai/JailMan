import React, { useEffect, useRef } from 'react';
import { useSimulationStore, type LogEntry } from '../../store/simulationStore';
import { Terminal, Clock, Shield, AlertTriangle, CheckCircle, Info } from 'lucide-react';
import clsx from 'clsx';

const LogItem: React.FC<{ log: LogEntry }> = ({ log }) => {
  const getIcon = () => {
    switch (log.level) {
      case 'error': return <Shield size={14} className="text-red-500" />;
      case 'warning': return <AlertTriangle size={14} className="text-amber-500" />;
      case 'success': return <CheckCircle size={14} className="text-emerald-500" />;
      default: return <Info size={14} className="text-blue-500" />;
    }
  };

  const getColor = () => {
    switch (log.level) {
      case 'error': return 'text-red-400 border-red-900/30 bg-red-900/10';
      case 'warning': return 'text-amber-400 border-amber-900/30 bg-amber-900/10';
      case 'success': return 'text-emerald-400 border-emerald-900/30 bg-emerald-900/10';
      default: return 'text-blue-400 border-blue-900/30 bg-blue-900/10';
    }
  };

  return (
    <div className={clsx(
      "flex items-start gap-3 p-2 rounded border mb-2 font-mono text-sm animate-in fade-in slide-in-from-bottom-2 duration-300",
      getColor()
    )}>
      <span className="mt-0.5 opacity-70">{getIcon()}</span>
      <div className="flex flex-col flex-1">
        <div className="flex justify-between items-center opacity-70 text-xs mb-1">
            <span className="uppercase tracking-wider font-bold">{log.source}</span>
            <span className="flex items-center gap-1"><Clock size={10} /> {log.timestamp}</span>
        </div>
        <span>{log.message}</span>
      </div>
    </div>
  );
};

export const LogWindow: React.FC = () => {
  const { logs } = useSimulationStore();
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [logs]);

  return (
    <div className="flex flex-col h-full bg-slate-950 border border-slate-800 rounded-lg overflow-hidden shadow-2xl shadow-black/50">
      <div className="flex items-center gap-2 px-4 py-2 bg-slate-900 border-b border-slate-800">
        <Terminal size={16} className="text-slate-400" />
        <span className="text-sm font-medium text-slate-300 uppercase tracking-wider">System Logs</span>
        <div className="ml-auto flex gap-1.5">
            <div className="w-2.5 h-2.5 rounded-full bg-slate-700"></div>
            <div className="w-2.5 h-2.5 rounded-full bg-slate-700"></div>
            <div className="w-2.5 h-2.5 rounded-full bg-slate-700"></div>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-4 scrollbar-thin scrollbar-thumb-slate-700 scrollbar-track-transparent">
        {logs.length === 0 ? (
            <div className="h-full flex flex-col items-center justify-center text-slate-600 opacity-50">
                <Terminal size={48} className="mb-4" />
                <p>System Ready. Waiting for events...</p>
            </div>
        ) : (
            logs.map((log) => <LogItem key={log.id} log={log} />)
        )}
        <div ref={bottomRef} />
      </div>
    </div>
  );
};
