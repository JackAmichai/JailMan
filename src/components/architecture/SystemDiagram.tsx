import React from 'react';
import { motion } from 'framer-motion';
import { useSimulationStore } from '../../store/simulationStore';
import { Network, ShieldCheck, BrainCircuit, Database } from 'lucide-react';
import clsx from 'clsx';

const Node: React.FC<{
  id: string;
  label: string;
  icon: React.ReactNode;
  isActive: boolean;
  color: 'blue' | 'cyan' | 'indigo' | 'purple';
}> = ({ id, label, icon, isActive, color }) => {
  const glowColor = {
    blue: 'shadow-blue-500/50 border-blue-500',
    cyan: 'shadow-cyan-500/50 border-cyan-500',
    indigo: 'shadow-indigo-500/50 border-indigo-500',
    purple: 'shadow-purple-500/50 border-purple-500',
  }[color];

  const baseColor = {
    blue: 'bg-blue-950/50 text-blue-200 border-blue-900',
    cyan: 'bg-cyan-950/50 text-cyan-200 border-cyan-900',
    indigo: 'bg-indigo-950/50 text-indigo-200 border-indigo-900',
    purple: 'bg-purple-950/50 text-purple-200 border-purple-900',
  }[color];

  return (
    <motion.div
      layoutId={id}
      className={clsx(
        "relative flex flex-col items-center justify-center w-32 h-32 rounded-xl border-2 transition-all duration-500 backdrop-blur-md",
        isActive ? `${glowColor} shadow-[0_0_30px_-5px]` : baseColor
      )}
      animate={{
        scale: isActive ? 1.1 : 1,
        opacity: isActive ? 1 : 0.7,
      }}
    >
      <div className="mb-2 p-2 rounded-full bg-black/20">
        {icon}
      </div>
      <span className="text-xs font-bold uppercase tracking-wider">{label}</span>

      {isActive && (
        <motion.div
          layoutId="active-ring"
          className={clsx("absolute inset-0 rounded-xl border-2", {
            'border-blue-400': color === 'blue',
            'border-cyan-400': color === 'cyan',
            'border-indigo-400': color === 'indigo',
            'border-purple-400': color === 'purple',
          })}
          initial={{ opacity: 0, scale: 1.2 }}
          animate={{ opacity: [0, 1, 0], scale: [1.2, 1.5, 1.8] }}
          transition={{ duration: 1.5, repeat: Infinity }}
        />
      )}
    </motion.div>
  );
};

const Connection: React.FC<{ active: boolean }> = ({ active }) => {
    return (
        <div className="flex-1 h-0.5 bg-slate-800 relative mx-4 min-w-[50px]">
            {active && (
                <motion.div
                    className="absolute top-1/2 left-0 w-full h-1 bg-gradient-to-r from-transparent via-cyan-400 to-transparent -translate-y-1/2"
                    initial={{ x: '-100%' }}
                    animate={{ x: '100%' }}
                    transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                />
            )}
        </div>
    );
};

export const SystemDiagram: React.FC = () => {
  const { activeNode } = useSimulationStore();

  // Helper to check if flow is active between nodes
  // For simplicity, we just check if activeNode is one of the nodes in the chain
  // A better way would be to track 'flow' state in store, but this suffices for visual demo

  return (
    <div className="relative flex items-center justify-center h-full w-full p-8 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-slate-900 via-slate-950 to-slate-950 overflow-hidden rounded-lg border border-slate-800 shadow-inner">
        {/* Background Grid */}
        <div className="absolute inset-0 bg-[linear-gradient(rgba(30,41,59,0.1)_1px,transparent_1px),linear-gradient(90deg,rgba(30,41,59,0.1)_1px,transparent_1px)] bg-[size:40px_40px] [mask-image:radial-gradient(ellipse_60%_60%_at_50%_50%,black,transparent)] pointer-events-none" />

        <div className="relative z-10 flex items-center w-full max-w-6xl justify-between px-8">
            {/* Input Section (Body) */}
            <div className="flex flex-col items-center gap-4">
                <span className="text-cyan-500/50 text-xs font-mono uppercase tracking-[0.2em] mb-8">Somatic Input</span>
                <Node
                    id="gateway"
                    label="Gateway"
                    icon={<Network size={24} />}
                    isActive={activeNode === 'gateway'}
                    color="cyan"
                />
            </div>

            <Connection active={activeNode === 'gateway'} />

            {/* Mind Section */}
            <div className="flex flex-col items-center gap-4">
                <span className="text-purple-500/50 text-xs font-mono uppercase tracking-[0.2em] mb-8">Cognitive Core (Mind)</span>
                <div className="flex items-center gap-4 p-6 border border-purple-500/20 rounded-2xl bg-purple-900/10 backdrop-blur-sm">
                    <Node
                        id="firewall"
                        label="AI Firewall"
                        icon={<ShieldCheck size={24} />}
                        isActive={activeNode === 'firewall'}
                        color="indigo"
                    />
                    <Connection active={activeNode === 'firewall'} />
                    <Node
                        id="ai"
                        label="Reasoning Engine"
                        icon={<BrainCircuit size={24} />}
                        isActive={activeNode === 'ai'}
                        color="purple"
                    />
                </div>
            </div>

            <Connection active={activeNode === 'ai'} />

            {/* Output Section (Body) */}
            <div className="flex flex-col items-center gap-4">
                <span className="text-blue-500/50 text-xs font-mono uppercase tracking-[0.2em] mb-8">Somatic Action</span>
                <Node
                    id="tools"
                    label="Tools / DB"
                    icon={<Database size={24} />}
                    isActive={activeNode === 'tools'}
                    color="blue"
                />
            </div>
        </div>
    </div>
  );
};
