import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Shield } from 'lucide-react';

const Navbar = () => {
  const location = useLocation();
  const links = [
    { to: '/network', label: 'Network Monitor' },
    { to: '/process', label: 'Process Monitor' },
    { to: '/honeypot', label: 'Honeypot Decoy' },
  ];

  return (
    <nav className="h-16 shrink-0 w-full flex items-center justify-between px-6 md:px-8 border-b border-white/5 bg-black/40 backdrop-blur-md z-50">
      <Link to="/" className="flex items-center gap-2.5 text-gray-100 hover:text-white transition-colors">
        <Shield size={20} className="text-orange-600" />
        <span className="font-serif text-lg tracking-tight">AccessDenied</span>
      </Link>

      <div className="hidden md:flex items-center gap-8">
        {links.map((link) => {
          const active = location.pathname === link.to;
          return (
            <Link key={link.to} to={link.to} className={`font-sans text-[13px] tracking-wide transition-colors ${active ? 'text-gray-100 font-bold' : 'text-gray-500 hover:text-gray-300'}`}>
              {link.label}
            </Link>
          );
        })}
      </div>
    </nav>
  );
};

export default Navbar;