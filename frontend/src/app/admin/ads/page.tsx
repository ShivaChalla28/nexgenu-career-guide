'use client';
import React, { useState, useEffect } from 'react';

export default function AdManager() {
  const [ads, setAds] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [newAd, setNewAd] = useState({ title: '', description: '', image_url: '', link_url: '', is_active: 1 });

  const fetchAds = () => {
    setLoading(true);
    fetch('/api/ui/ads')
      .then(res => res.json())
      .then(data => {
        setAds(Array.isArray(data) ? data : []);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchAds();
  }, []);

  const handleDelete = async (id: string) => {
    if (!confirm('Are you sure you want to delete this ad?')) return;
    try {
      await fetch(`/api/ui/ads/${id}`, { method: 'DELETE' });
      fetchAds();
    } catch (err) {
      console.error(err);
    }
  };

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await fetch('/api/ui/ads', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newAd)
      });
      if (res.ok) {
        setShowModal(false);
        setNewAd({ title: '', description: '', image_url: '', link_url: '', is_active: 1 });
        fetchAds();
      }
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Ad Manager</h1>
        <button 
          onClick={() => setShowModal(true)}
          className="bg-purple-500 text-white px-4 py-2 rounded-lg font-semibold hover:bg-purple-600 transition-colors"
        >
          + Publish Ad
        </button>
      </div>

      {loading ? (
        <div className="p-8 text-center text-foreground/50">Loading ads...</div>
      ) : (
        <div className="bg-foreground/5 rounded-xl border border-foreground/10 overflow-hidden">
          <table className="w-full text-left">
            <thead className="bg-foreground/10 border-b border-foreground/10">
              <tr>
                <th className="p-4 font-semibold">Title</th>
                <th className="p-4 font-semibold">Link / Image</th>
                <th className="p-4 font-semibold">Status</th>
                <th className="p-4 font-semibold">Actions</th>
              </tr>
            </thead>
            <tbody>
              {ads.length === 0 ? (
                <tr>
                  <td colSpan={4} className="p-8 text-center text-foreground/50">No ads found.</td>
                </tr>
              ) : ads.map((ad) => (
                <tr key={ad.id} className="border-b border-foreground/10 last:border-0 hover:bg-foreground/5">
                  <td className="p-4 font-medium max-w-[250px]">
                    <div className="truncate">{ad.title}</div>
                    <div className="text-xs text-foreground/60 font-normal mt-1 truncate">{ad.description}</div>
                  </td>
                  <td className="p-4 text-sm">
                    {ad.link_url && <a href={ad.link_url} target="_blank" className="text-blue-500 hover:underline block truncate max-w-[200px]">{ad.link_url}</a>}
                    {ad.image_url && <span className="text-foreground/50 block mt-1">Has Image</span>}
                  </td>
                  <td className="p-4">
                    <span className={`px-2 py-1 rounded text-xs font-bold ${ad.is_active ? 'bg-green-500/20 text-green-500' : 'bg-red-500/20 text-red-500'}`}>
                      {ad.is_active ? 'Active' : 'Disabled'}
                    </span>
                  </td>
                  <td className="p-4">
                    <button onClick={() => handleDelete(ad.id)} className="text-red-500 hover:underline font-semibold">Delete</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {showModal && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <div className="bg-background p-8 rounded-2xl border border-foreground/10 shadow-2xl w-full max-w-md max-h-[90vh] overflow-y-auto">
            <h2 className="text-2xl font-bold mb-6">Create New Ad</h2>
            <form onSubmit={handleCreate} className="flex flex-col gap-4">
              <div>
                <label className="block text-sm font-semibold mb-1">Ad Title</label>
                <input required value={newAd.title} onChange={e => setNewAd({...newAd, title: e.target.value})} className="w-full p-2 rounded-lg bg-foreground/5 border border-foreground/10" placeholder="e.g. Up to 50% off on premium courses!" />
              </div>
              <div>
                <label className="block text-sm font-semibold mb-1">Description (Optional)</label>
                <textarea value={newAd.description} onChange={e => setNewAd({...newAd, description: e.target.value})} className="w-full p-2 rounded-lg bg-foreground/5 border border-foreground/10" rows={2} placeholder="Brief details about the ad..." />
              </div>
              <div>
                <label className="block text-sm font-semibold mb-1">Image URL (Optional)</label>
                <input type="url" value={newAd.image_url} onChange={e => setNewAd({...newAd, image_url: e.target.value})} className="w-full p-2 rounded-lg bg-foreground/5 border border-foreground/10" placeholder="https://..." />
              </div>
              <div>
                <label className="block text-sm font-semibold mb-1">Target Link URL</label>
                <input required type="url" value={newAd.link_url} onChange={e => setNewAd({...newAd, link_url: e.target.value})} className="w-full p-2 rounded-lg bg-foreground/5 border border-foreground/10" placeholder="https://..." />
              </div>
              <div>
                <label className="flex items-center gap-2">
                  <input type="checkbox" checked={newAd.is_active === 1} onChange={e => setNewAd({...newAd, is_active: e.target.checked ? 1 : 0})} />
                  Is Active?
                </label>
              </div>
              <div className="flex justify-end gap-3 mt-4">
                <button type="button" onClick={() => setShowModal(false)} className="px-4 py-2 bg-foreground/10 rounded-lg hover:bg-foreground/20 font-semibold">Cancel</button>
                <button type="submit" className="px-4 py-2 bg-purple-500 text-white font-semibold rounded-lg hover:bg-purple-600">Publish Ad</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
