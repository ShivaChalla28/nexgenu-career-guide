'use client';
import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';

export default function IncubationPortal() {
  const [ideas, setIdeas] = useState<any[]>([]);

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_URL || ''}/api/incubation/ideas`)
      .then(res => res.json())
      .then(data => setIdeas(Array.isArray(data) ? data : []))
      .catch(console.error);
  }, []);

  const handleSubmitIdea = (e: React.FormEvent) => {
    e.preventDefault();
    alert('Idea submitted successfully for review!');
  };

  return (
    <main className="flex min-h-screen flex-col pt-24 pb-20 px-6 max-w-7xl mx-auto w-full">
      <h1 className="text-4xl font-extrabold mb-3">Startup Incubation</h1>
      <p className="text-foreground/60 mb-10 max-w-2xl">
        Got a billion-dollar idea? Pitch it to our mentors, get feedback, and incubate your startup with NexGenU.
      </p>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-10">
        <motion.div 
          className="p-8 rounded-3xl border border-foreground/10 bg-foreground/3 shadow-xl"
          initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }}
        >
          <h2 className="text-2xl font-bold mb-6">Submit Your Pitch</h2>
          <form onSubmit={handleSubmitIdea} className="flex flex-col gap-4">
            <div>
              <label className="block text-sm font-semibold mb-1">Startup Name</label>
              <input required type="text" className="w-full px-4 py-3 rounded-xl bg-background border border-foreground/10 focus:border-orange-500 outline-none transition" placeholder="e.g. Acme Corp" />
            </div>
            <div>
              <label className="block text-sm font-semibold mb-1">Elevator Pitch</label>
              <textarea required rows={4} className="w-full px-4 py-3 rounded-xl bg-background border border-foreground/10 focus:border-orange-500 outline-none transition" placeholder="Describe your idea in 3 sentences..."></textarea>
            </div>
            <div>
              <label className="block text-sm font-semibold mb-1">Pitch Deck Link</label>
              <input required type="url" className="w-full px-4 py-3 rounded-xl bg-background border border-foreground/10 focus:border-orange-500 outline-none transition" placeholder="https://drive.google.com/..." />
            </div>
            <button type="submit" className="mt-2 py-3 bg-gradient-to-r from-orange-500 to-red-500 text-white rounded-xl font-bold shadow-lg shadow-orange-500/20 hover:scale-[1.02] transition">
              Submit Idea →
            </button>
          </form>
        </motion.div>

        <div>
          <h2 className="text-2xl font-bold mb-6">Your Submissions</h2>
          <div className="flex flex-col gap-4">
            {ideas.map(idea => (
              <div key={idea.idea_id} className="p-6 rounded-2xl border border-foreground/10 bg-background flex flex-col gap-3">
                <div className="flex justify-between">
                  <h3 className="font-bold text-lg">{idea.title}</h3>
                  <span className="text-xs px-2 py-1 bg-yellow-500/20 text-yellow-600 rounded-full font-bold uppercase">{idea.status || 'Pending Review'}</span>
                </div>
                <p className="text-sm text-foreground/60">{idea.description}</p>
                {idea.feedback && (
                  <div className="mt-2 p-3 rounded-lg bg-blue-500/10 border border-blue-500/20 text-sm text-blue-400">
                    <strong>Mentor Feedback:</strong> {idea.feedback}
                  </div>
                )}
              </div>
            ))}
            {ideas.length === 0 && (
              <p className="text-foreground/40 italic">You haven't submitted any ideas yet.</p>
            )}
          </div>
        </div>
      </div>
    </main>
  );
}
