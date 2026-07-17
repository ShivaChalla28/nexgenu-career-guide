'use client';
import React, { useState, useEffect } from 'react';

export default function ManageRoadmaps() {
  const [roadmaps, setRoadmaps] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(0);

  const fetchRoadmaps = () => {
    setLoading(true);
    fetch(`${process.env.NEXT_PUBLIC_API_URL || ''}/api/roadmaps/?skip=${page * 50}&limit=50`)
      .then(res => res.json())
      .then(data => { setRoadmaps(data); setLoading(false); })
      .catch(err => { console.error(err); setLoading(false); });
  };

  useEffect(() => { fetchRoadmaps(); }, [page]);

  const handleDelete = async (id: string) => {
    if (!confirm('Delete this roadmap?')) return;
    try {
      await fetch(`${process.env.NEXT_PUBLIC_API_URL || ''}/api/roadmaps/${id}`, { method: 'DELETE' });
      fetchRoadmaps();
    } catch (err) { console.error(err); }
  };

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Manage Roadmaps</h1>
      <div className="bg-foreground/5 rounded-xl border border-foreground/10 overflow-hidden">
        <table className="w-full text-left">
          <thead className="bg-foreground/10 border-b border-foreground/10">
            <tr>
              <th className="p-4 font-semibold">Title</th>
              <th className="p-4 font-semibold">Actions</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr><td colSpan={2} className="p-8 text-center text-foreground/50">Loading roadmaps...</td></tr>
            ) : roadmaps.map((r: any) => (
              <tr key={r.id} className="border-b border-foreground/10 last:border-0 hover:bg-foreground/5">
                <td className="p-4 font-medium">{r.title}</td>
                <td className="p-4"><button onClick={() => handleDelete(r.id)} className="text-red-500 hover:underline">Delete</button></td>
              </tr>
            ))}
          </tbody>
        </table>
        <div className="p-4 border-t border-foreground/10 flex justify-between items-center bg-foreground/5">
          <button onClick={() => setPage(p => Math.max(0, p - 1))} disabled={page === 0} className="px-4 py-2 bg-foreground/10 rounded disabled:opacity-50">Previous</button>
          <span className="text-sm font-medium">Page {page + 1}</span>
          <button onClick={() => setPage(p => p + 1)} disabled={roadmaps.length < 50} className="px-4 py-2 bg-foreground/10 rounded disabled:opacity-50">Next</button>
        </div>
      </div>
    </div>
  );
}
