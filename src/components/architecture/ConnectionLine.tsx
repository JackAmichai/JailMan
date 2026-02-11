import React from 'react';
import { motion } from 'framer-motion';

interface ConnectionLineProps {
  active: boolean;
  direction?: 'up' | 'down';
}

export const ConnectionLine: React.FC<ConnectionLineProps> = ({ active, direction = 'down' }) => {
  return (
    <div className="h-16 flex justify-center items-center w-full my-2">
        <svg width="40" height="100%" viewBox="0 0 40 100" preserveAspectRatio="none" className="overflow-visible">
            {/* Background Line */}
            <line x1="20" y1="0" x2="20" y2="100" stroke="#334155" strokeWidth="2" strokeDasharray="4 4" />

            {/* Animated Pulse */}
            <motion.circle
                cx="20"
                cy={direction === 'down' ? 0 : 100}
                r="4"
                fill="#3B82F6"
                filter="url(#glow)"
                initial={{ opacity: 0 }}
                animate={active ? {
                    cy: direction === 'down' ? [0, 100] : [100, 0],
                    opacity: [0, 1, 0]
                } : { opacity: 0 }}
                transition={{
                    duration: 1.5,
                    repeat: Infinity,
                    ease: "linear",
                    repeatDelay: 0.1
                }}
            />

            <defs>
                <filter id="glow">
                    <feGaussianBlur stdDeviation="2.5" result="coloredBlur"/>
                    <feMerge>
                        <feMergeNode in="coloredBlur"/>
                        <feMergeNode in="SourceGraphic"/>
                    </feMerge>
                </filter>
            </defs>
        </svg>
    </div>
  );
};
