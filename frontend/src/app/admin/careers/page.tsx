'use client';
import React, { useState, useEffect } from 'react';

export default function ManageCareers() {
  const [careers, setCareers] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(0);

  const fetchCareers = () => {
    setLoading(true);
    fetch(`http://localhost:8000/api/careers/?skip=${page * 50}&limit=50`)
      .then(res => res.json())
      .then(data => { setCareers(data); setLoading(false); })
      .catch(err => { console.error(err); setLoading(false); });
  };

  useEffect(() => { fetchCareers(); }, [page]);

  const handleDelete = async (id: string) => {
    if (!confirm('Delete this career? This also deletes its roadmaps/mappings.')) return;
    try {
      await fetch(`http://localhost:8000/api/careers/${id}`, { method: 'DELETE' });
      fetchCareers();
    } catch (err) { console.error(err); }
  };

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Manage Careers</h1>
      <div className="bg-foreground/5 rounded-xl border border-foreground/10 overflow-hidden">
        <table className="w-full text-left">
          <thead className="bg-foreground/10 border-b border-foreground/10">
            <tr>
              <th className="p-4 font-semibold">Name</th>
              <th className="p-4 font-semibold">Category</th>
              <th className="p-4 font-semibold">Salary (India)</th>
              <th className="p-4 font-semibold">Actions</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr><td colSpan={4} className="p-8 text-center text-foreground/50">Loading careers...</td></tr>
            ) : careers.map((c: any) => (
              <tr key={c.id} className="border-b border-foreground/10 last:border-0 hover:bg-foreground/5">
                <td className="p-4 font-medium">{c.name}</td>
                <td className="p-4 text-foreground/70">{c.category || 'Uncategorized'}</td>
                <td className="p-4 text-foreground/70">{c.india_salary || 'N/A'}</td>
                <td className="p-4"><button onClick={() => handleDelete(c.id)} className="text-red-500 hover:underline">Delete</button></td>
              </tr>
            ))}
          </tbody>
        </table>
        <div className="p-4 border-t border-foreground/10 flex justify-between items-center bg-foreground/5">
          <button onClick={() => setPage(p => Math.max(0, p - 1))} disabled={page === 0} className="px-4 py-2 bg-foreground/10 rounded disabled:opacity-50">Previous</button>
          <span className="text-sm font-medium">Page {page + 1}</span>
          <button onClick={() => setPage(p => p + 1)} disabled={careers.length < 50} className="px-4 py-2 bg-foreground/10 rounded disabled:opacity-50">Next</button>
        </div>
      </div>
    </div>
  );
}
