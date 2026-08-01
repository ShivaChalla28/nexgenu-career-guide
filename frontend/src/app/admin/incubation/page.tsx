'use client';
import React, { useEffect, useState } from 'react';

export default function AdminIncubationManager() {
  const [ideas, setIdeas] = useState<any[]>([]);

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_URL || ''}/api/incubation/ideas`)
      .then(res => res.json())
      .then(data => setIdeas(Array.isArray(data) ? data : []))
      .catch(console.error);
  }, []);

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Startup Incubation</h1>
      <p className="text-foreground/60 mb-8">Review startup ideas, assign mentors, and schedule pitches.</p>
      
      <div className="grid grid-cols-1 gap-4">
        {ideas.map(idea => (
          <div key={idea.idea_id} className="p-6 rounded-xl border border-foreground/10 bg-foreground/5 flex justify-between items-center">
            <div>
              <h3 className="font-bold text-lg">{idea.title}</h3>
              <p className="text-sm text-foreground/50">{idea.description}</p>
            </div>
            <div className="flex gap-2">
              <button className="px-4 py-2 bg-green-500/10 text-green-600 rounded font-semibold text-sm hover:bg-green-500/20">Assign Mentor</button>
            </div>
          </div>
        ))}
        {ideas.length === 0 && (
          <div className="p-8 text-center text-foreground/50 border border-foreground/10 rounded-xl bg-foreground/5">
            No startup ideas submitted.
          </div>
        )}
      </div>
    </div>
  );
}
