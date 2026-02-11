import React from 'react';
import { motion } from 'framer-motion';
import type { LucideIcon } from 'lucide-react';

export type NodeStatus = 'idle' | 'processing' | 'alert' | 'safe';

interface ComponentNodeProps {
  title: string;
  icon: LucideIcon;
  status: NodeStatus;
  details?: string;
  children?: React.ReactNode;
}

export const ComponentNode: React.FC<ComponentNodeProps> = ({
  title,
  icon: Icon,
  status,
  details,
  children
}) => {
  const getGlowColor = (status: NodeStatus) => {
    switch (status) {
      case 'alert':
        return 'rgba(239, 68, 68, 0.5)'; // red-500
      case 'processing':
        return 'rgba(59, 130, 246, 0.5)'; // blue-500
      case 'safe':
        return 'rgba(34, 197, 94, 0.5)'; // green-500
      case 'idle':
      default:
        return 'rgba(148, 163, 184, 0.1)'; // slate-400
    }
  };

  const getBorderColor = (status: NodeStatus) => {
    switch (status) {
      case 'alert':
        return '#EF4444';
      case 'processing':
        return '#3B82F6';
      case 'safe':
        return '#22C55E';
      case 'idle':
      default:
        return '#334155'; // slate-700
    }
  };

  return (
    <motion.div
      animate={{
        borderColor: getBorderColor(status),
        boxShadow: `0 0 20px ${getGlowColor(status)}`
      }}
      className="p-4 rounded-xl border-2 bg-slate-900 transition-colors w-64 flex flex-col items-center gap-2 relative z-10"
    >
      <div className={`p-2 rounded-full bg-slate-800 ${status === 'processing' ? 'animate-pulse' : ''}`}>
        <Icon className="w-8 h-8 text-slate-200" />
      </div>
      <h3 className="text-slate-200 font-bold text-lg">{title}</h3>
      {details && (
        <p className="text-slate-400 text-sm text-center">{details}</p>
      )}
      {children}
    </motion.div>
  );
};
