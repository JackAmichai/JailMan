import React from 'react';
import { useSimulationStore } from '../../store/simulationStore';
import { Play, ShieldAlert, Bug, Activity } from 'lucide-react';

export const ScenarioSelector: React.FC = () => {
  const { addLog, setActiveNode, clearLogs } = useSimulationStore();

  const runScenario = (type: string) => {
    clearLogs();
    addLog({
      source: 'System',
      message: `Initiating scenario: ${type}`,
      level: 'info',
    });

    if (type === 'Normal Request') {
      setActiveNode('gateway');
      addLog({ source: 'User', message: 'Sending legitimate request...', level: 'info' });

      setTimeout(() => {
        addLog({ source: 'Gateway', message: 'Request received. Validating headers...', level: 'info' });
        setActiveNode('firewall');
      }, 1000);

      setTimeout(() => {
        addLog({ source: 'Firewall', message: 'Security checks passed.', level: 'success' });
        setActiveNode('ai');
      }, 2500);

      setTimeout(() => {
        addLog({ source: 'Core AI', message: ' analyzing intent...', level: 'info' });
        setActiveNode('tools');
      }, 4500);

      setTimeout(() => {
        addLog({ source: 'Tool Exec', message: 'Fetching user data...', level: 'success' });
        setActiveNode(null);
      }, 6000);
    }

    else if (type === 'SQL Injection') {
      setActiveNode('gateway');
      addLog({ source: 'Attacker', message: 'Injecting payload: OR 1=1--', level: 'warning' });

      setTimeout(() => {
        addLog({ source: 'Gateway', message: 'Malicious pattern detected in payload.', level: 'warning' });
        setActiveNode('firewall');
      }, 1000);

      setTimeout(() => {
        addLog({ source: 'Firewall', message: 'THREAT BLOCKED: SQL Injection attempt.', level: 'error' });
        setActiveNode(null);
      }, 2000);
    }

    else if (type === 'Jailbreak Attempt') {
        setActiveNode('gateway');
        addLog({ source: 'Attacker', message: 'Prompt: "Ignore previous instructions..."', level: 'warning' });

        setTimeout(() => {
            addLog({ source: 'Gateway', message: 'Request passed initial structural checks.', level: 'info' });
            setActiveNode('firewall');
        }, 1000);

        setTimeout(() => {
            addLog({ source: 'Firewall', message: 'Traffic allowed (no signature match).', level: 'warning' });
            setActiveNode('ai');
        }, 2500);

        setTimeout(() => {
            addLog({ source: 'Guardrail AI', message: 'Semantic analysis: Jailbreak intent detected.', level: 'error' });
            setActiveNode(null);
        }, 4500);
    }
  };

  return (
    <div className="flex flex-col gap-4 p-6 bg-slate-900/50 backdrop-blur-sm border border-slate-800 rounded-lg">
      <h3 className="text-slate-400 text-sm font-medium uppercase tracking-wider">Simulation Scenarios</h3>
      <div className="grid grid-cols-2 gap-3">
        <button
          onClick={() => runScenario('Normal Request')}
          className="flex items-center gap-3 px-4 py-3 bg-blue-500/10 hover:bg-blue-500/20 border border-blue-500/30 text-blue-400 rounded-md transition-all text-sm font-medium"
        >
          <Play size={18} /> Normal Flow
        </button>
        <button
          onClick={() => runScenario('SQL Injection')}
          className="flex items-center gap-3 px-4 py-3 bg-red-500/10 hover:bg-red-500/20 border border-red-500/30 text-red-400 rounded-md transition-all text-sm font-medium"
        >
          <ShieldAlert size={18} /> SQL Injection
        </button>
        <button
          onClick={() => runScenario('Jailbreak Attempt')}
          className="flex items-center gap-3 px-4 py-3 bg-purple-500/10 hover:bg-purple-500/20 border border-purple-500/30 text-purple-400 rounded-md transition-all text-sm font-medium"
        >
          <Bug size={18} /> Jailbreak
        </button>
        <button
          onClick={() => runScenario('System Overload')} // Not implemented yet
          className="flex items-center gap-3 px-4 py-3 bg-amber-500/10 hover:bg-amber-500/20 border border-amber-500/30 text-amber-400 rounded-md transition-all text-sm font-medium opacity-50 cursor-not-allowed"
        >
          <Activity size={18} /> System Overload
        </button>
      </div>
    </div>
  );
};
