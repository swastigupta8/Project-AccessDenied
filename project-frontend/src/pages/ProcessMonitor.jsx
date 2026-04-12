import React, { useState, useEffect } from 'react';
import { Droplets, Zap, Activity } from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import Navbar from '../components/Navbar.jsx';
import ThreatLevelBox from '../components/ThreatLevelBox.jsx';
import axios from 'axios';

const API_BASE = 'http://127.0.0.1:8000';

const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null;
  return (
    <div className="bg-[#0a0a0a] border border-white/10 rounded-lg p-3 font-mono text-xs z-50 shadow-xl">
      <p className="text-gray-500 mb-1.5">{label}</p>
      {payload.map((entry, i) => (
        <p key={i} style={{ color: entry.color }} className="font-bold">{entry.name}: {entry.value}%</p>
      ))}
    </div>
  );
};

const ProcessMonitor = () => {
  const [processData, setProcessData] = useState({ threat_confidence: 0, status: 'LOW' });
  const [chartData, setChartData] = useState([]);
  const [zeekLogs, setZeekLogs] = useState([]);
  const [isLive, setIsLive] = useState(true);

  useEffect(() => {
    const fetchZeek = async () => {
      try {
        const res = await axios.get(`${API_BASE}/api/zeek/logs`);
        setZeekLogs(res.data || []);
      } catch (err) {}
    };
    fetchZeek();
    const interval = setInterval(fetchZeek, 5000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await axios.get(`${API_BASE}/api/stream`);
        if (res?.data && !res.data.error) {
          setProcessData(res.data);
          setChartData(prev => [...prev.slice(-20), { time: new Date().toLocaleTimeString([], { hour12: false }), process: res.data.threat_confidence }]);
        }
      } catch (err) {}
    };
    fetchData();
    const interval = setInterval(() => { if (isLive) fetchData(); }, 3000);
    return () => clearInterval(interval);
  }, [isLive]);

  const lineColor = processData.status === 'HIGH' ? '#ef4444' : processData.status === 'MEDIUM' ? '#eab308' : '#3b82f6';

  return (
    <div className="h-screen w-full flex flex-col font-sans">
      <Navbar />

      <div className="flex-1 min-h-0 w-full max-w-[1600px] mx-auto p-4 md:p-6">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 md:gap-6 h-full min-h-0">
          
          <div className="lg:col-span-2 bg-neutral-900/30 border border-white/5 rounded-2xl p-5 md:p-6 flex flex-col min-h-[300px] lg:min-h-0">
            <div className="flex justify-between items-center mb-6 shrink-0">
              <h1 className="font-serif text-2xl md:text-3xl text-gray-100">Process Monitor</h1>
              <button onClick={() => setIsLive(!isLive)} className={`flex items-center gap-2 px-3 py-1.5 rounded-full border text-[10px] font-mono font-bold tracking-widest ${isLive ? 'border-green-500/30 bg-green-500/10 text-green-500' : 'border-red-500/30 bg-red-500/10 text-red-500'}`}>
                <div className={`w-1.5 h-1.5 rounded-full ${isLive ? 'bg-green-500 animate-pulse' : 'bg-red-500'}`} />
                {isLive ? 'LIVE' : 'PAUSED'}
              </button>
            </div>

            <div className="flex-1 w-full min-h-0 relative">
              <div className="absolute inset-0">
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={chartData}>
                    <defs>
                      <linearGradient id="procGrad" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="0%" stopColor={lineColor} stopOpacity={0.25} />
                        <stop offset="100%" stopColor={lineColor} stopOpacity={0} />
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
                    <XAxis dataKey="time" stroke="#555" tick={{ fill: '#888', fontSize: 10, fontFamily: 'monospace' }} axisLine={false} tickLine={false} tickMargin={10} />
                    <YAxis domain={[0, 100]} stroke="#555" tick={{ fill: '#888', fontSize: 10, fontFamily: 'monospace' }} axisLine={false} tickLine={false} tickMargin={10} />
                    <Tooltip content={<CustomTooltip />} />
                    <Area type="monotone" dataKey="process" stroke={lineColor} strokeWidth={2} fill="url(#procGrad)" isAnimationActive={false} />
                  </AreaChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>

          <div className="lg:col-span-1 flex flex-col gap-4 md:gap-6 min-h-0">
            <ThreatLevelBox label="Process Threat" percentage={processData.threat_confidence} status={processData.status} />

            <div className={`shrink-0 border rounded-2xl p-5 ${processData.status === 'HIGH' ? 'bg-red-950/20 border-red-500/20' : processData.status === 'MEDIUM' ? 'bg-yellow-950/20 border-yellow-500/20' : 'bg-neutral-900/30 border-white/5'}`}>
              <div className="flex items-center gap-2 mb-3">
                <Zap size={14} className={processData.status === 'HIGH' ? 'text-red-500' : 'text-blue-500'} />
                <span className="font-mono text-[10px] font-bold tracking-widest text-gray-400 uppercase">Autonomous Intel</span>
              </div>
              <p className={`text-xs leading-relaxed ${processData.status === 'HIGH' ? 'text-red-200' : processData.status === 'MEDIUM' ? 'text-yellow-200' : 'text-green-400'}`}>
                {processData.status === 'HIGH' ? "CRITICAL: SVM detected physical water pump anomaly. Override valves manually." : processData.status === 'MEDIUM' ? "WARNING: Irregular pressure detected in ICS. Monitor tanks." : "NOMINAL: SCADA telemetry within baselines."}
              </p>
            </div>

            <div className="flex-1 flex flex-col bg-neutral-900/30 border border-white/5 rounded-2xl overflow-hidden min-h-[200px]">
              <div className="p-4 border-b border-white/5 bg-black/20 flex items-center shrink-0">
                <div className="flex items-center gap-2 text-cyan-500 font-mono text-[10px] font-bold uppercase tracking-widest">
                  <Activity size={14} /> Zeek: weird.log
                </div>
              </div>
              <div className="flex-1 overflow-y-auto p-2">
                {zeekLogs.map((log, idx) => (
                  <div key={idx} className="flex gap-3 px-3 py-2 border-b border-white/5 font-mono text-[10px] hover:bg-white/5 transition-colors">
                    <span className="text-gray-500 shrink-0">[{log.ts}]</span>
                    <span className="text-cyan-500 font-bold truncate w-24 md:w-28 shrink-0">{log['id.orig_h']}</span>
                    <span className="text-yellow-500/80 truncate flex-1">{log.note}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
          
        </div>
      </div>
    </div>
  );
};

export default ProcessMonitor;