import React, { useState, useEffect } from 'react';
import { Lock, AlertTriangle, Crosshair } from 'lucide-react';
import Navbar from '../components/Navbar.jsx';
import axios from 'axios';

const API_BASE = 'http://127.0.0.1:8000';
const HONEYPOT_PORT = 8080;
const DOT_COLORS = ['#e8450e', '#a855f7', '#3b82f6', '#22c55e', '#f59e0b', '#06b6d4'];

const IPCard = ({ ip, index, total, radiusPercent, isCritical, globalRotation }) => {
  const angle = ((index / total) * 360 - 90 + globalRotation) * (Math.PI / 180);
  const xOffset = Math.cos(angle) * radiusPercent;
  const yOffset = Math.sin(angle) * radiusPercent;
  const dotColor = isCritical ? '#ef4444' : DOT_COLORS[index % DOT_COLORS.length];

  return (
    <div
      className={`absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 w-[85px] md:w-[95px] h-[85px] md:h-[95px] rounded-xl flex flex-col items-center justify-center gap-1.5 transition-all duration-300 backdrop-blur-md cursor-default
        ${isCritical ? 'bg-red-950/60 border border-red-500/50 shadow-[0_0_20px_rgba(239,68,68,0.2)] z-20' : 'bg-black/80 border border-white/5 z-10 hover:scale-105'}`}
      style={{ left: `calc(50% + ${xOffset}%)`, top: `calc(50% + ${yOffset}%)` }}
    >
      <div className={`w-1.5 h-1.5 md:w-2 md:h-2 rounded-full ${isCritical ? 'bg-red-500 animate-pulse shadow-[0_0_10px_#ef4444]' : ''}`} style={{ backgroundColor: !isCritical ? dotColor : undefined }} />
      <span className={`font-mono text-[8px] md:text-[9px] font-bold text-center leading-tight ${isCritical ? 'text-red-300' : 'text-gray-300'}`}>{ip}</span>
      <span className={`font-mono text-[7px] md:text-[8px] font-bold px-2 py-0.5 rounded-full uppercase tracking-wider ${isCritical ? 'bg-red-500/20 text-red-500' : 'bg-white/5 text-gray-400'}`}>
        {isCritical ? 'Critical' : 'Monitor'}
      </span>
    </div>
  );
};

const Honeypot = () => {
  const [backendLogs, setBackendLogs] = useState([]);
  const [rotation, setRotation] = useState(0);

  useEffect(() => {
    const fetchLogs = async () => {
      try {
        const res = await axios.get(`${API_BASE}/api/honeypot/logs`);
        setBackendLogs(res.data || []);
      } catch (err) {}
    };
    fetchLogs();
    const interval = setInterval(fetchLogs, 4000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    const anim = setInterval(() => setRotation((prev) => prev + 0.3), 50);
    return () => clearInterval(anim);
  }, []);

  const hasAlerts = backendLogs.length > 0;
  const displayItems = backendLogs.slice(-8).map(log => ({ ip: log.attacker_ip, isCritical: true }));
  
  const placeholders = ['192.168.1.45', '10.0.0.112', '172.16.0.88', '203.0.113.7', '198.51.100.3', '45.33.32.156', '8.8.8.8'];
  let pIdx = 0;
  while (displayItems.length < 8) {
    displayItems.push({ ip: placeholders[pIdx % placeholders.length], isCritical: false });
    pIdx++;
  }

  return (
    <div className="h-screen w-full flex flex-col font-sans">
      <Navbar />

      <div className="flex-1 min-h-0 w-full max-w-[1600px] mx-auto p-4 md:p-6">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 md:gap-6 h-full min-h-0">
          
          {/* Radar Arena (Bounded to an Aspect Square) */}
          <div className="bg-neutral-900/30 border border-white/5 rounded-2xl flex items-center justify-center p-6 relative min-h-[400px] lg:min-h-0 overflow-hidden">
            <div className="relative w-full h-full max-w-[550px] max-h-[550px] aspect-square flex items-center justify-center">
              
              {/* Radar Rings */}
              {[0.4, 0.7, 1].map((scale, i) => (
                <div key={i} className="absolute rounded-full border border-white/5 pointer-events-none" style={{ width: `${100 * scale}%`, height: `${100 * scale}%` }} />
              ))}

              {/* Sweeper Line */}
              <div className="absolute w-[50%] h-[2px] bg-gradient-to-r from-transparent via-orange-600/40 to-transparent origin-left pointer-events-none" style={{ transform: `rotate(${rotation * 2}deg)` }} />

              {/* Orbiting IPs */}
              <div className="absolute inset-0">
                 {displayItems.map((item, i) => (
                  <IPCard key={i} ip={item.ip} index={i} total={displayItems.length} radiusPercent={38} isCritical={item.isCritical} globalRotation={rotation} />
                ))}
              </div>

              {/* Center Hub */}
              <div className="absolute flex flex-col items-center z-30 pointer-events-none">
                <div className={`absolute w-32 h-32 md:w-40 md:h-40 rounded-full ${hasAlerts ? 'bg-[radial-gradient(circle,rgba(239,68,68,0.2)_0%,transparent_70%)]' : 'bg-[radial-gradient(circle,rgba(232,69,14,0.15)_0%,transparent_70%)]'}`} />
                <Lock size={28} className={`mb-3 relative ${hasAlerts ? 'text-red-500' : 'text-orange-500'}`} />
                <h2 className="font-serif text-xl md:text-2xl text-gray-100 mb-1 relative">{hasAlerts ? 'Under Attack' : 'Trap Active'}</h2>
                <p className="text-gray-500 text-[9px] md:text-[10px] text-center max-w-[120px] relative">{hasAlerts ? `${backendLogs.length} attempts captured.` : `Port ${HONEYPOT_PORT} active.`}</p>
              </div>
            </div>
          </div>

          {/* Right Column: Intel & Logs */}
          <div className="flex flex-col gap-4 md:gap-6 min-h-0">
            <div className={`shrink-0 border rounded-2xl p-5 md:p-6 ${hasAlerts ? 'bg-red-950/20 border-red-500/30' : 'bg-neutral-900/30 border-orange-500/30'}`}>
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-2">
                  <Crosshair size={16} className={hasAlerts ? 'text-red-500' : 'text-orange-500'} />
                  <span className={`font-mono text-xs md:text-[13px] font-bold uppercase tracking-widest ${hasAlerts ? 'text-red-500' : 'text-orange-500'}`}>Honeypot Intel</span>
                </div>
                <span className="font-mono text-[9px] md:text-[10px] text-gray-500">DECOY: 0.0.0.0:{HONEYPOT_PORT}</span>
              </div>
              <p className={`text-xs md:text-sm leading-relaxed ${hasAlerts ? 'text-red-300' : 'text-gray-400'}`}>
                {hasAlerts ? `SUSTAINED ATTACK: Decoy port ${HONEYPOT_PORT} absorbing heavy fire (${backendLogs.length} hits). Perimeter breached. ACTION: Null-route attacking IPs at Edge Firewall.` : "PERIMETER SECURE: The deception trap reports zero unauthorized intrusions. Monitoring active."}
              </p>
            </div>

            <div className="flex-1 flex flex-col bg-neutral-900/30 border border-white/5 rounded-2xl overflow-hidden min-h-[250px]">
              <div className="p-4 border-b border-white/5 bg-black/20 flex items-center shrink-0">
                <div className="flex items-center gap-2 text-orange-500 font-mono text-[10px] md:text-xs font-bold uppercase tracking-widest">
                  <AlertTriangle size={14} /> Deception Triggers
                </div>
              </div>
              
              <div className="flex-1 overflow-y-auto">
                <table className="w-full text-left font-sans text-xs">
                  <thead className="sticky top-0 bg-[#0a0a0a]">
                    <tr>
                      <th className="p-3 md:p-4 font-mono text-[9px] md:text-[10px] text-gray-500 uppercase tracking-widest border-b border-white/5">Time</th>
                      <th className="p-3 md:p-4 font-mono text-[9px] md:text-[10px] text-gray-500 uppercase tracking-widest border-b border-white/5">Source IP</th>
                      <th className="p-3 md:p-4 font-mono text-[9px] md:text-[10px] text-gray-500 uppercase tracking-widest border-b border-white/5 text-right">Severity</th>
                    </tr>
                  </thead>
                  <tbody>
                    {backendLogs.length > 0 ? backendLogs.slice().reverse().map((log, idx) => (
                      <tr key={idx} className="border-b border-white/5 hover:bg-white/5 transition-colors">
                        <td className="p-3 md:p-4 text-gray-500">{new Date().toLocaleTimeString()}</td>
                        <td className="p-3 md:p-4 font-mono font-bold text-orange-500">{log.attacker_ip}</td>
                        <td className="p-3 md:p-4 text-right">
                          <span className="font-mono text-[9px] md:text-[10px] font-bold px-2.5 py-1 rounded-full bg-red-500/10 text-red-500 border border-red-500/20">CRITICAL</span>
                        </td>
                      </tr>
                    )) : (
                      <tr><td colSpan="3" className="p-8 text-center text-gray-500 italic">No unauthorized probes detected.</td></tr>
                    )}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
          
        </div>
      </div>
    </div>
  );
};

export default Honeypot;