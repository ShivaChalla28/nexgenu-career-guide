'use client';
import React, { useState, useEffect } from 'react';

export default function AlertManager() {
  const [alerts, setAlerts] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [newAlert, setNewAlert] = useState({ title: '', type: 'Placement', message: '', priority: 'Medium', is_active: 1 });

  const fetchAlerts = () => {
    setLoading(true);
    fetch('/api/ui/alerts')
      .then(res => res.json())
      .then(data => {
        setAlerts(data);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchAlerts();
  }, []);

  const handleDelete = async (id: string) => {
    if (!confirm('Are you sure you want to delete this alert?')) return;
    try {
      await fetch(`/api/ui/alerts/${id}`, { method: 'DELETE' });
      fetchAlerts();
    } catch (err) {
      console.error(err);
    }
  };

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await fetch('/api/ui/alerts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newAlert)
      });
      if (res.ok) {
        setShowModal(false);
        setNewAlert({ title: '', type: 'Placement', message: '', priority: 'Medium', is_active: 1 });
        fetchAlerts();
      }
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Alert Manager</h1>
        <button 
          onClick={() => setShowModal(true)}
          className="bg-purple-500 text-white px-4 py-2 rounded-lg font-semibold hover:bg-purple-600 transition-colors"
        >
          + Publish Alert
        </button>
      </div>

      {loading ? (
        <div className="p-8 text-center text-foreground/50">Loading alerts...</div>
      ) : (
        <div className="bg-foreground/5 rounded-xl border border-foreground/10 overflow-hidden">
          <table className="w-full text-left">
            <thead className="bg-foreground/10 border-b border-foreground/10">
              <tr>
                <th className="p-4 font-semibold">Title</th>
                <th className="p-4 font-semibold">Type</th>
                <th className="p-4 font-semibold">Priority</th>
                <th className="p-4 font-semibold">Status</th>
                <th className="p-4 font-semibold">Actions</th>
              </tr>
            </thead>
            <tbody>
              {alerts.length === 0 ? (
                <tr>
                  <td colSpan={5} className="p-8 text-center text-foreground/50">No alerts found.</td>
                </tr>
              ) : alerts.map((a) => (
                <tr key={a.id} className="border-b border-foreground/10 last:border-0 hover:bg-foreground/5">
                  <td className="p-4 font-medium">{a.title}</td>
                  <td className="p-4 text-foreground/70">{a.type}</td>
                  <td className="p-4 text-foreground/70">{a.priority}</td>
                  <td className="p-4">
                    <span className={`px-2 py-1 rounded text-xs font-bold ${a.is_active ? 'bg-green-500/20 text-green-500' : 'bg-red-500/20 text-red-500'}`}>
                      {a.is_active ? 'Active' : 'Disabled'}
                    </span>
                  </td>
                  <td className="p-4">
                    <button onClick={() => handleDelete(a.id)} className="text-red-500 hover:underline">Delete</button>
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
            <h2 className="text-2xl font-bold mb-6">Create New Alert</h2>
            <form onSubmit={handleCreate} className="flex flex-col gap-4">
              <div>
                <label className="block text-sm font-semibold mb-1">Title</label>
                <input required value={newAlert.title} onChange={e => setNewAlert({...newAlert, title: e.target.value})} className="w-full p-2 rounded-lg bg-foreground/5 border border-foreground/10" placeholder="e.g. TCS Off-Campus Drive 2026" />
              </div>
              <div>
                <label className="block text-sm font-semibold mb-1">Type</label>
                <select value={newAlert.type} onChange={e => setNewAlert({...newAlert, type: e.target.value})} className="w-full p-2 rounded-lg bg-foreground/5 border border-foreground/10">
                  <option>Placement</option>
                  <option>Hackathon</option>
                  <option>Internship</option>
                  <option>Announcement</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-semibold mb-1">Priority</label>
                <select value={newAlert.priority} onChange={e => setNewAlert({...newAlert, priority: e.target.value})} className="w-full p-2 rounded-lg bg-foreground/5 border border-foreground/10">
                  <option>High</option>
                  <option>Medium</option>
                  <option>Low</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-semibold mb-1">Message</label>
                <textarea required value={newAlert.message} onChange={e => setNewAlert({...newAlert, message: e.target.value})} className="w-full p-2 rounded-lg bg-foreground/5 border border-foreground/10" rows={3} placeholder="Full details..." />
              </div>
              <div>
                <label className="flex items-center gap-2">
                  <input type="checkbox" checked={newAlert.is_active === 1} onChange={e => setNewAlert({...newAlert, is_active: e.target.checked ? 1 : 0})} />
                  Is Active?
                </label>
              </div>
              <div className="flex justify-end gap-3 mt-4">
                <button type="button" onClick={() => setShowModal(false)} className="px-4 py-2 bg-foreground/10 rounded-lg hover:bg-foreground/20">Cancel</button>
                <button type="submit" className="px-4 py-2 bg-purple-500 text-white font-semibold rounded-lg hover:bg-purple-600">Publish</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
