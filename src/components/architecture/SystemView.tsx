import React, { useState } from 'react';
import { Shield, Brain, Lock } from 'lucide-react';
import { ComponentNode, type NodeStatus } from './ComponentNode';
import { ConnectionLine } from './ConnectionLine';

export const SystemView: React.FC = () => {
  const [firewallStatus, setFirewallStatus] = useState<NodeStatus>('idle');
  const [graphStatus, setGraphStatus] = useState<NodeStatus>('idle');
  const [gatewayStatus, setGatewayStatus] = useState<NodeStatus>('idle');

  const [connection1Active, setConnection1Active] = useState(false); // Gateway <-> Graph
  const [connection2Active, setConnection2Active] = useState(false); // Graph <-> Firewall

  const [flowDirection, setFlowDirection] = useState<'up' | 'down'>('up');

  const [simulationState, setSimulationState] = useState<'idle' | 'requesting' | 'processing' | 'responding'>('idle');

  const simulateRequest = async () => {
    if (simulationState !== 'idle') return;

    setSimulationState('requesting');
    setFlowDirection('up');

    // Step 1: Gateway activates
    setGatewayStatus('processing');
    await new Promise(r => setTimeout(r, 800));

    // Step 2: Pulse Up to Graph
    setConnection1Active(true);
    await new Promise(r => setTimeout(r, 800));
    setGatewayStatus('idle');
    setConnection1Active(false);

    // Step 3: Graph activates
    setGraphStatus('processing');
    await new Promise(r => setTimeout(r, 1200));

    // Step 4: Pulse Up to Firewall
    setConnection2Active(true);
    await new Promise(r => setTimeout(r, 800));
    setGraphStatus('idle');
    setConnection2Active(false);

    // Step 5: Firewall activates (Processing)
    setFirewallStatus('processing');
    setSimulationState('processing');
    await new Promise(r => setTimeout(r, 1500));

    // Step 6: Decision (Random Safe or Alert)
    const isSafe = Math.random() > 0.5;
    setFirewallStatus(isSafe ? 'safe' : 'alert');
    setSimulationState('responding');
    setFlowDirection('down');

    await new Promise(r => setTimeout(r, 1000));

    // Step 7: Pulse Down
    setConnection2Active(true); // Firewall -> Graph
    await new Promise(r => setTimeout(r, 800));
    setConnection2Active(false);

    setGraphStatus(isSafe ? 'safe' : 'alert'); // Highlight graph briefly with the result
    await new Promise(r => setTimeout(r, 500));

    setConnection1Active(true); // Graph -> Gateway
    await new Promise(r => setTimeout(r, 800));
    setConnection1Active(false);
    setGraphStatus('idle');

    // Step 8: Gateway result
    setGatewayStatus(isSafe ? 'safe' : 'alert');

    await new Promise(r => setTimeout(r, 2000));

    // Reset
    setFirewallStatus('idle');
    setGraphStatus('idle');
    setGatewayStatus('idle');
    setSimulationState('idle');
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-slate-950 p-8 text-white">
      <h1 className="text-3xl font-bold mb-8 bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
        Neuro-Symbolic Architecture
      </h1>

      <div className="flex flex-col items-center max-w-md w-full">

        {/* Top: Cognitive Firewall (Mind) */}
        <ComponentNode
          title="Cognitive Firewall"
          icon={Shield}
          status={firewallStatus}
          details="Mind Layer - Decision Engine"
        />

        {/* Connection 2 */}
        <ConnectionLine active={connection2Active} direction={flowDirection} />

        {/* Middle: Operation Graph (Memory) */}
        <ComponentNode
          title="Operation Graph"
          icon={Brain}
          status={graphStatus}
          details="Memory Layer - Context & Knowledge"
        />

        {/* Connection 1 */}
        <ConnectionLine active={connection1Active} direction={flowDirection} />

        {/* Bottom: Guardrail Gateway (Body) */}
        <ComponentNode
          title="Guardrail Gateway"
          icon={Lock}
          status={gatewayStatus}
          details="Body Layer - Input/Output"
        />

        <button
          onClick={simulateRequest}
          disabled={simulationState !== 'idle'}
          className={`mt-12 px-8 py-3 rounded-full font-bold transition-all transform hover:scale-105 ${
            simulationState === 'idle'
              ? 'bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white shadow-lg shadow-blue-500/25'
              : 'bg-slate-800 text-slate-500 cursor-not-allowed border border-slate-700'
          }`}
        >
          {simulationState === 'idle' ? 'Simulate Request' : 'Processing...'}
        </button>

        <p className="mt-4 text-slate-500 text-sm">
          Click the button to visualize the data flow.
        </p>

      </div>
    </div>
  );
};
