'use client';
import React, { useEffect, useState } from 'react';

export default function AdminHackathonsManager() {
  const [hackathons, setHackathons] = useState<any[]>([]);

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_URL || ''}/api/hackathons/`)
      .then(res => res.json())
      .then(data => setHackathons(Array.isArray(data) ? data : []))
      .catch(console.error);
  }, []);

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Hackathons Management</h1>
        <button className="px-5 py-2 bg-purple-600 text-white rounded-xl font-bold">+ New Hackathon</button>
      </div>
      
      <div className="grid grid-cols-1 gap-4">
        {hackathons.map(h => (
          <div key={h.hackathon_id} className="p-6 rounded-xl border border-foreground/10 bg-foreground/5 flex justify-between items-center">
            <div>
              <h3 className="font-bold text-lg">{h.title}</h3>
              <p className="text-sm text-foreground/50">{h.start_date} • Team Size: {h.team_size}</p>
            </div>
            <div className="flex gap-2">
              <button className="px-4 py-2 bg-blue-500/10 text-blue-600 rounded font-semibold text-sm hover:bg-blue-500/20">Edit</button>
              <button className="px-4 py-2 bg-red-500/10 text-red-600 rounded font-semibold text-sm hover:bg-red-500/20">Delete</button>
            </div>
          </div>
        ))}
        {hackathons.length === 0 && (
          <div className="p-8 text-center text-foreground/50 border border-foreground/10 rounded-xl bg-foreground/5">
            No hackathons created yet.
          </div>
        )}
      </div>
    </div>
  );
}
