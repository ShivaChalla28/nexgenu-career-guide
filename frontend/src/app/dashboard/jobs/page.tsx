'use client';
import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';

export default function JobsPortal() {
  const [jobs, setJobs] = useState<any[]>([]);
  const [internships, setInternships] = useState<any[]>([]);
  const [activeTab, setActiveTab] = useState<'jobs'|'internships'>('jobs');
  const [search, setSearch] = useState('');

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_URL || ''}/api/jobs/`)
      .then(res => res.json())
      .then(data => setJobs(Array.isArray(data) ? data : []))
      .catch(console.error);

    fetch(`${process.env.NEXT_PUBLIC_API_URL || ''}/api/jobs/internships/all`)
      .then(res => res.json())
      .then(data => setInternships(Array.isArray(data) ? data : []))
      .catch(console.error);
  }, []);

  const dataToDisplay = activeTab === 'jobs' ? jobs : internships;
  const filtered = dataToDisplay.filter(item => 
    (item.title || '').toLowerCase().includes(search.toLowerCase()) ||
    (item.company || '').toLowerCase().includes(search.toLowerCase())
  );

  const handleApply = (id: string) => {
    // Basic apply logic
    alert(`Applied successfully to ${id}!`);
  };

  return (
    <main className="flex min-h-screen flex-col pt-24 pb-20 px-6 max-w-7xl mx-auto w-full">
      <h1 className="text-4xl font-extrabold mb-6">Career Opportunities</h1>
      
      <div className="flex gap-4 mb-6">
        <button 
          className={`px-6 py-2 rounded-full font-bold transition-all ${activeTab === 'jobs' ? 'bg-blue-600 text-white' : 'bg-foreground/5 text-foreground/60'}`}
          onClick={() => setActiveTab('jobs')}
        >
          Jobs
        </button>
        <button 
          className={`px-6 py-2 rounded-full font-bold transition-all ${activeTab === 'internships' ? 'bg-purple-600 text-white' : 'bg-foreground/5 text-foreground/60'}`}
          onClick={() => setActiveTab('internships')}
        >
          Internships
        </button>
      </div>

      <div className="relative w-full md:w-96 mb-8">
        <span className="absolute left-4 top-1/2 -translate-y-1/2 text-foreground/40">🔍</span>
        <input
          type="text"
          placeholder="Search roles, companies..."
          value={search}
          onChange={e => setSearch(e.target.value)}
          className="w-full pl-10 pr-4 py-3 rounded-xl bg-foreground/5 border border-foreground/10 focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 transition text-sm"
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filtered.map(item => (
          <motion.div 
            key={item.job_id || item.internship_id}
            className="p-6 rounded-2xl border border-foreground/10 bg-foreground/3 hover:border-blue-500/30 transition-all flex flex-col justify-between"
            whileHover={{ y: -5 }}
          >
            <div>
              <div className="flex justify-between items-start mb-2">
                <h3 className="font-bold text-lg">{item.title}</h3>
                <span className="text-xs px-2 py-1 bg-foreground/10 rounded-full">{item.type || item.duration || 'Full-time'}</span>
              </div>
              <p className="text-blue-500 font-semibold mb-1">{item.company}</p>
              <p className="text-foreground/50 text-sm mb-4">📍 {item.location}</p>
              <p className="text-sm line-clamp-3 mb-4">{item.description}</p>
            </div>
            
            <button 
              onClick={() => handleApply(item.job_id || item.internship_id)}
              className="w-full py-2 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-xl font-bold transition hover:opacity-90"
            >
              Apply Now
            </button>
          </motion.div>
        ))}
        {filtered.length === 0 && (
          <p className="text-foreground/40">No {activeTab} found matching your search.</p>
        )}
      </div>
    </main>
  );
}
