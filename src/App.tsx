import { SystemDiagram } from './components/architecture/SystemDiagram';
import { ScenarioSelector } from './components/controls/ScenarioSelector';
import { LogWindow } from './components/console/LogWindow';
import { Activity } from 'lucide-react';

function App() {
  return (
    <div className="flex flex-col h-screen bg-slate-950 text-slate-100 overflow-hidden font-sans selection:bg-cyan-500/30">

      {/* Header */}
      <header className="flex items-center justify-between px-6 py-4 border-b border-slate-800 bg-slate-900/50 backdrop-blur-md">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg shadow-lg shadow-purple-500/20">
            <Activity className="text-white" size={24} />
          </div>
          <div>
            <h1 className="text-xl font-bold tracking-tight bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
              NEURO-SYMBOLIC GUARDRAIL
            </h1>
            <p className="text-xs text-slate-400 font-mono tracking-wider">SYSTEM STATUS: ONLINE</p>
          </div>
        </div>
        <div className="flex items-center gap-4">
             <div className="flex items-center gap-2 px-3 py-1 rounded-full bg-slate-800 border border-slate-700 text-xs text-slate-400 font-mono">
                <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                LIVE SIMULATION
             </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="flex flex-1 overflow-hidden p-4 gap-4">

        {/* Left Panel: Diagram & Controls */}
        <main className="flex-[3] flex flex-col gap-4 relative">
            <div className="flex-1 rounded-2xl border border-slate-800 overflow-hidden shadow-2xl bg-slate-900/30 backdrop-blur-sm relative group">
                <div className="absolute top-4 left-4 z-20 text-xs font-mono text-slate-500 uppercase tracking-widest pointer-events-none">
                    Architecture Visualization
                </div>
                <SystemDiagram />
            </div>

            <div className="h-auto">
                <ScenarioSelector />
            </div>
        </main>

        {/* Right Panel: Console */}
        <aside className="flex-[1] min-w-[320px] flex flex-col">
           <LogWindow />
        </aside>

      </div>
    </div>
  );
}

export default App;
