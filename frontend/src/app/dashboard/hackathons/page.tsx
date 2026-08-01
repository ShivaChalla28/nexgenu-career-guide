'use client';
import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';

export default function HackathonsPortal() {
  const [hackathons, setHackathons] = useState<any[]>([]);

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_URL || ''}/api/hackathons/`)
      .then(res => res.json())
      .then(data => setHackathons(Array.isArray(data) ? data : []))
      .catch(console.error);
  }, []);

  const handleRegister = (id: string) => {
    alert(`Registered for hackathon ${id}!`);
  };

  return (
    <main className="flex min-h-screen flex-col pt-24 pb-20 px-6 max-w-7xl mx-auto w-full">
      <h1 className="text-4xl font-extrabold mb-3">Hackathons & Events</h1>
      <p className="text-foreground/60 mb-8 max-w-2xl">
        Compete with the best minds, build innovative projects, and win exciting prizes.
      </p>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {hackathons.map(h => (
          <motion.div 
            key={h.hackathon_id}
            className="p-6 rounded-3xl border border-foreground/10 bg-gradient-to-br from-indigo-500/10 to-purple-500/5 hover:border-indigo-500/30 transition-all flex flex-col justify-between"
            whileHover={{ y: -5 }}
          >
            <div>
              <div className="flex justify-between items-start mb-4">
                <h3 className="font-bold text-2xl">{h.title}</h3>
                <span className={`text-xs px-3 py-1 rounded-full font-bold ${h.status === 'upcoming' ? 'bg-yellow-500/20 text-yellow-500' : 'bg-green-500/20 text-green-500'}`}>
                  {h.status?.toUpperCase() || 'LIVE'}
                </span>
              </div>
              <p className="text-foreground/70 mb-6">{h.description}</p>
              
              <div className="flex gap-4 text-sm text-foreground/50 mb-6 font-mono">
                <div>🗓️ {h.start_date || 'TBA'}</div>
                <div>👥 Team: {h.team_size || '1-4'}</div>
              </div>
            </div>
            
            <button 
              onClick={() => handleRegister(h.hackathon_id)}
              className="w-full py-3 bg-indigo-600 text-white rounded-xl font-bold transition hover:bg-indigo-700"
            >
              Register Team
            </button>
          </motion.div>
        ))}
        {hackathons.length === 0 && (
          <div className="p-8 rounded-3xl border border-dashed border-foreground/20 text-center col-span-full">
            <p className="text-foreground/50">No hackathons available at the moment. Stay tuned!</p>
          </div>
        )}
      </div>
    </main>
  );
}
