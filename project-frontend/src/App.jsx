import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Landing from './pages/Landing.jsx';
import NetworkSecurity from './pages/NetworkSecurity.jsx';
import ProcessMonitor from './pages/ProcessMonitor.jsx';
import Honeypot from './pages/Honeypot.jsx';

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/network" element={<NetworkSecurity />} />
        <Route path="/process" element={<ProcessMonitor />} />
        <Route path="/honeypot" element={<Honeypot />} />
      </Routes>
    </Router>
  );
};

export default App;