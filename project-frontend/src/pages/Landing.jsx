import React from 'react';
import { Link } from 'react-router-dom';
import { Activity, Lock, Cpu, Shield } from 'lucide-react';
import Navbar from '../components/Navbar.jsx';

const Landing = () => {
  return (
    <div className="h-screen w-full bg-[#050505] flex flex-col relative overflow-hidden font-sans text-gray-100">
      {/* Background Gradients */}
      <div className="absolute bottom-0 left-1/2 -translate-x-1/2 w-full max-w-5xl h-[60%] bg-[radial-gradient(ellipse_at_center_bottom,rgba(232,69,14,0.20)_0%,transparent_60%)] pointer-events-none" />
      
      <Navbar />

      {/* Hero Section */}
      <div className="flex-1 flex flex-col items-center justify-center text-center px-6 relative z-10 min-h-0">
        
        {/* AlphaQ Team Badge */}
        <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full border border-white/10 bg-white/5 mb-6 md:mb-8 shadow-[0_0_15px_rgba(232,69,14,0.1)]">
          <Shield size={12} className="text-orange-500" />
          <span className="font-mono text-[10px] tracking-widest text-gray-400 uppercase">
            AccessDenied <span className="text-orange-500 font-bold">by AlphaQ</span>
          </span>
        </div>

        <h1 className="font-serif text-5xl md:text-6xl lg:text-7xl text-gray-100 mb-1 md:mb-2 leading-tight">
          Defending the Future
        </h1>
        <h1 className="font-serif text-5xl md:text-6xl lg:text-7xl italic text-orange-600 mb-4 md:mb-6 leading-tight">
          One Threat at a Time.
        </h1>
        <p className="text-gray-400 max-w-lg mx-auto text-xs md:text-sm leading-relaxed">
          Real-time AI-powered intrusion detection across network, process, and honeypot vectors. Stay ahead of every zero-day attack.
        </p>

      </div>

      {/* Fixed Grid Footer */}
      <div className="w-full max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-4 md:gap-6 px-6 pb-8 md:pb-12 shrink-0 relative z-10">
        {[
          { icon: Activity, title: 'Network Monitor', desc: 'Isolation Forest AI detects anomalous IT traffic.', to: '/network', color: 'text-purple-500' },
          { icon: Cpu, title: 'Process Monitor', desc: 'SVM-powered ICS/SCADA telemetry analysis.', to: '/process', color: 'text-blue-500' },
          { icon: Lock, title: 'Honeypot Trap', desc: 'Deception-based detection capturing live IPs.', to: '/honeypot', color: 'text-orange-500' },
        ].map((card) => (
          <Link key={card.to} to={card.to} className="group bg-neutral-900/30 border border-white/5 hover:border-white/10 rounded-2xl p-5 md:p-6 transition-all duration-300 hover:-translate-y-1 flex flex-col justify-center">
            <card.icon size={20} className={`${card.color} mb-3 md:mb-4`} />
            <h3 className="text-gray-100 text-sm md:text-base font-bold mb-1 md:mb-2">{card.title}</h3>
            <p className="text-gray-500 text-[10px] md:text-xs leading-relaxed">{card.desc}</p>
          </Link>
        ))}
      </div>
      
    </div>
  );
};

export default Landing;