'use client';
import React, { useState, useEffect } from 'react';

export default function ButtonManager() {
  const [buttons, setButtons] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [newButton, setNewButton] = useState({ name: '', icon: '🌟', color: 'bg-blue-500', url: '', placement: 'Homepage', is_active: 1 });

  const fetchButtons = () => {
    setLoading(true);
    fetch(`${process.env.NEXT_PUBLIC_API_URL || ''}/api/ui/buttons`)
      .then(res => res.json())
      .then(data => {
        setButtons(data);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchButtons();
  }, []);

  const handleDelete = async (id: string) => {
    if (!confirm('Are you sure you want to delete this button?')) return;
    try {
      await fetch(`${process.env.NEXT_PUBLIC_API_URL || ''}/api/ui/buttons/${id}`, { method: 'DELETE' });
      fetchButtons();
    } catch (err) {
      console.error(err);
    }
  };

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || ''}/api/ui/buttons`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newButton)
      });
      if (res.ok) {
        setShowModal(false);
        setNewButton({ name: '', icon: '🌟', color: 'bg-blue-500', url: '', placement: 'Homepage', is_active: 1 });
        fetchButtons();
      }
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Button Manager</h1>
        <button 
          onClick={() => setShowModal(true)}
          className="bg-purple-500 text-white px-4 py-2 rounded-lg font-semibold hover:bg-purple-600 transition-colors"
        >
          + Create Button
        </button>
      </div>

      {loading ? (
        <div className="p-8 text-center text-foreground/50">Loading buttons...</div>
      ) : (
        <div className="bg-foreground/5 rounded-xl border border-foreground/10 overflow-hidden">
          <table className="w-full text-left">
            <thead className="bg-foreground/10 border-b border-foreground/10">
              <tr>
                <th className="p-4 font-semibold">Name</th>
                <th className="p-4 font-semibold">Placement</th>
                <th className="p-4 font-semibold">Status</th>
                <th className="p-4 font-semibold">Actions</th>
              </tr>
            </thead>
            <tbody>
              {buttons.length === 0 ? (
                <tr>
                  <td colSpan={4} className="p-8 text-center text-foreground/50">No buttons found.</td>
                </tr>
              ) : buttons.map((b) => (
                <tr key={b.id} className="border-b border-foreground/10 last:border-0 hover:bg-foreground/5">
                  <td className="p-4 font-medium flex items-center gap-2">
                    <span className="text-xl">{b.icon}</span> {b.name}
                  </td>
                  <td className="p-4 text-foreground/70">{b.placement}</td>
                  <td className="p-4">
                    <span className={`px-2 py-1 rounded text-xs font-bold ${b.is_active ? 'bg-green-500/20 text-green-500' : 'bg-red-500/20 text-red-500'}`}>
                      {b.is_active ? 'Active' : 'Disabled'}
                    </span>
                  </td>
                  <td className="p-4">
                    <button onClick={() => handleDelete(b.id)} className="text-red-500 hover:underline">Delete</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {showModal && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <div className="bg-background p-8 rounded-2xl border border-foreground/10 shadow-2xl w-full max-w-md">
            <h2 className="text-2xl font-bold mb-6">Create New Button</h2>
            <form onSubmit={handleCreate} className="flex flex-col gap-4">
              <div>
                <label className="block text-sm font-semibold mb-1">Button Text</label>
                <input required value={newButton.name} onChange={e => setNewButton({...newButton, name: e.target.value})} className="w-full p-2 rounded-lg bg-foreground/5 border border-foreground/10" placeholder="e.g. Join WhatsApp" />
              </div>
              <div className="flex gap-4">
                <div className="flex-1">
                  <label className="block text-sm font-semibold mb-1">Emoji Icon</label>
                  <input required value={newButton.icon} onChange={e => setNewButton({...newButton, icon: e.target.value})} className="w-full p-2 rounded-lg bg-foreground/5 border border-foreground/10" placeholder="📱" />
                </div>
                <div className="flex-1">
                  <label className="block text-sm font-semibold mb-1">Color Class</label>
                  <select value={newButton.color} onChange={e => setNewButton({...newButton, color: e.target.value})} className="w-full p-2 rounded-lg bg-foreground/5 border border-foreground/10">
                    <option value="bg-blue-500">Blue</option>
                    <option value="bg-green-500">Green</option>
                    <option value="bg-purple-500">Purple</option>
                    <option value="bg-red-500">Red</option>
                    <option value="bg-amber-500">Orange</option>
                  </select>
                </div>
              </div>
              <div>
                <label className="block text-sm font-semibold mb-1">Target URL</label>
                <input required type="url" value={newButton.url} onChange={e => setNewButton({...newButton, url: e.target.value})} className="w-full p-2 rounded-lg bg-foreground/5 border border-foreground/10" placeholder="https://..." />
              </div>
              <div>
                <label className="block text-sm font-semibold mb-1">Placement</label>
                <select value={newButton.placement} onChange={e => setNewButton({...newButton, placement: e.target.value})} className="w-full p-2 rounded-lg bg-foreground/5 border border-foreground/10">
                  <option>Homepage</option>
                  <option>Dashboard</option>
                  <option>Footer</option>
                </select>
              </div>
              <div>
                <label className="flex items-center gap-2">
                  <input type="checkbox" checked={newButton.is_active === 1} onChange={e => setNewButton({...newButton, is_active: e.target.checked ? 1 : 0})} />
                  Is Active?
                </label>
              </div>
              <div className="flex justify-end gap-3 mt-4">
                <button type="button" onClick={() => setShowModal(false)} className="px-4 py-2 bg-foreground/10 rounded-lg hover:bg-foreground/20">Cancel</button>
                <button type="submit" className="px-4 py-2 bg-purple-500 text-white font-semibold rounded-lg hover:bg-purple-600">Create</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
