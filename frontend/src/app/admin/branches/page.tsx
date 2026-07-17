'use client';
import React, { useState, useEffect } from 'react';

export default function ManageBranches() {
  const [branches, setBranches] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [newBranchName, setNewBranchName] = useState('');

  const fetchBranches = () => {
    fetch('https://nexgenu-career-guide.onrender.com/api/branches/')
      .then(res => res.json())
      .then(data => { setBranches(data); setLoading(false); })
      .catch(err => { console.error(err); setLoading(false); });
  };

  useEffect(() => {
    fetchBranches();
  }, []);

  const handleCreate = async () => {
    if (!newBranchName) return;
    try {
      const res = await fetch('https://nexgenu-career-guide.onrender.com/api/branches/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: newBranchName, slug: newBranchName.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '') })
      });
      if (res.ok) {
        setShowModal(false);
        setNewBranchName('');
        fetchBranches();
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleDelete = async (id: string) => {
    if (!confirm('Are you sure you want to delete this branch?')) return;
    try {
      await fetch(`https://nexgenu-career-guide.onrender.com/api/branches/${id}`, { method: 'DELETE' });
      fetchBranches();
    } catch (err) {
      console.error(err);
    }
  };

  if (loading) return <div>Loading branches...</div>;

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Manage Branches</h1>
        <button onClick={() => setShowModal(true)} className="bg-blue-500 text-white px-4 py-2 rounded-lg font-semibold hover:bg-blue-600 transition-colors">
          + Add Branch
        </button>
      </div>

      <div className="bg-foreground/5 rounded-xl border border-foreground/10 overflow-hidden">
        <table className="w-full text-left">
          <thead className="bg-foreground/10 border-b border-foreground/10">
            <tr>
              <th className="p-4 font-semibold">Name</th>
              <th className="p-4 font-semibold">Slug</th>
              <th className="p-4 font-semibold">Careers</th>
              <th className="p-4 font-semibold">Actions</th>
            </tr>
          </thead>
          <tbody>
            {branches.map((b) => (
              <tr key={b.id} className="border-b border-foreground/10 last:border-0 hover:bg-foreground/5">
                <td className="p-4 font-medium">{b.name}</td>
                <td className="p-4 text-foreground/70">{b.slug}</td>
                <td className="p-4 text-foreground/70">{b.careers?.length || 0}</td>
                <td className="p-4">
                  <button onClick={() => handleDelete(b.id)} className="text-red-500 hover:underline">Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {showModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-background p-6 rounded-xl border border-foreground/10 w-full max-w-md">
            <h2 className="text-xl font-bold mb-4">Add New Branch</h2>
            <input 
              className="w-full p-2 border border-foreground/20 rounded mb-4 bg-transparent"
              placeholder="Branch Name (e.g., Computer Science)"
              value={newBranchName}
              onChange={e => setNewBranchName(e.target.value)}
            />
            <div className="flex justify-end gap-2">
              <button onClick={() => setShowModal(false)} className="px-4 py-2 rounded hover:bg-foreground/10">Cancel</button>
              <button onClick={handleCreate} className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">Create</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
