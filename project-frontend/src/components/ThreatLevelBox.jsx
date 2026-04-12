import React from 'react';

const ThreatLevelBox = ({ label, percentage, status }) => {
  const colors = {
    HIGH: { text: 'text-red-500', bg: 'bg-red-500/10', border: 'border-red-500/30', bar: 'bg-red-500' },
    MEDIUM: { text: 'text-yellow-500', bg: 'bg-yellow-500/10', border: 'border-yellow-500/30', bar: 'bg-yellow-500' },
    LOW: { text: 'text-green-500', bg: 'bg-green-500/10', border: 'border-green-500/30', bar: 'bg-green-500' }
  }[status] || colors.LOW;

  return (
    <div className="bg-neutral-900/30 border border-white/5 rounded-2xl p-5 md:p-6 relative overflow-hidden shrink-0">
      <div className={`absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-current to-transparent ${colors.text} opacity-40`} />

      <div className="flex justify-between items-center mb-4 md:mb-6">
        <span className="font-sans text-[10px] md:text-xs font-bold tracking-widest uppercase text-gray-500">{label}</span>
        <span className={`font-mono text-[9px] md:text-[10px] font-bold px-2.5 py-0.5 rounded-full border ${colors.bg} ${colors.text} ${colors.border} tracking-widest`}>{status}</span>
      </div>

      <div className="font-serif text-4xl md:text-5xl text-gray-100 mb-1">{percentage}<span className="text-xl md:text-2xl text-gray-600">%</span></div>
      <p className="font-sans text-[10px] md:text-xs text-gray-500 mb-4 md:mb-6">Threat Confidence Score</p>

      <div className="h-1.5 w-full bg-white/5 rounded-full overflow-hidden">
        <div className={`h-full ${colors.bar} transition-all duration-1000 ease-out rounded-full`} style={{ width: `${percentage}%` }} />
      </div>
    </div>
  );
};

export default ThreatLevelBox;