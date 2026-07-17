'use client';
import React, { useState, useEffect } from 'react';

export default function AdminDashboard() {
  const [stats, setStats] = useState({ 
    users: 0, branches: 0, careers: 0, roadmaps: 0, 
    core_careers: 0, it_careers: 0, govt_careers: 0, visible_careers: 0,
    pending_feedback: 0, approved_feedback: 0
  });
  const [pendingFeedback, setPendingFeedback] = useState<any[]>([]);
  const [approvedFeedback, setApprovedFeedback] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/admin/stats')
      .then(res => res.json())
      .then(data => setStats(data))
      .catch(err => console.error("Failed to fetch stats", err));

    Promise.all([
      fetch('/api/feedback/pending').then(res => res.json()),
      fetch('/api/feedback/approved').then(res => res.json())
    ])
    .then(([pending, approved]) => {
      setPendingFeedback(Array.isArray(pending) ? pending : []);
      setApprovedFeedback(Array.isArray(approved) ? approved : []);
      setLoading(false);
    })
    .catch(err => {
      console.error("Failed to fetch feedback", err);
      setLoading(false);
    });
  }, []);

  const handleApprove = async (id: string) => {
    try {
      const res = await fetch(`/api/feedback/${id}/approve`, { method: 'PUT' });
      if (res.ok) {
        const approvedItem = pendingFeedback.find(f => f.id === id);
        setPendingFeedback(prev => prev.filter(f => f.id !== id));
        if (approvedItem) {
          setApprovedFeedback(prev => [approvedItem, ...prev]);
        }
        setStats(prev => ({ ...prev, pending_feedback: prev.pending_feedback - 1, approved_feedback: prev.approved_feedback + 1 }));
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleReject = async (id: string) => {
    try {
      const res = await fetch(`/api/feedback/${id}`, { method: 'DELETE' });
      if (res.ok) {
        setPendingFeedback(prev => prev.filter(f => f.id !== id));
        setStats(prev => ({ ...prev, pending_feedback: prev.pending_feedback - 1 }));
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleRejectApproved = async (id: string) => {
    try {
      const res = await fetch(`/api/feedback/${id}`, { method: 'DELETE' });
      if (res.ok) {
        setApprovedFeedback(prev => prev.filter(f => f.id !== id));
        setStats(prev => ({ ...prev, approved_feedback: prev.approved_feedback - 1 }));
      }
    } catch (err) {
      console.error(err);
    }
  };

  if (loading) {
    return <div className="p-8 text-center text-foreground/50">Loading live statistics...</div>;
  }

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Dashboard Analytics</h1>
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="p-6 rounded-xl border border-foreground/10 bg-foreground/5 shadow-sm">
          <h3 className="text-lg font-medium text-foreground/70">Total Branches</h3>
          <p className="text-4xl font-extrabold mt-2 text-blue-500">{stats.branches}</p>
        </div>
        <div className="p-6 rounded-xl border border-foreground/10 bg-foreground/5 shadow-sm">
          <h3 className="text-lg font-medium text-foreground/70">Total Careers</h3>
          <p className="text-4xl font-extrabold mt-2 text-purple-500">
            {stats.careers} 
            <span className="text-sm font-medium text-foreground/50 ml-2">({stats.visible_careers} visible)</span>
          </p>
        </div>
        <div className="p-6 rounded-xl border border-foreground/10 bg-foreground/5 shadow-sm">
          <h3 className="text-lg font-medium text-foreground/70">Total Users</h3>
          <p className="text-4xl font-extrabold mt-2 text-pink-500">{stats.users}</p>
        </div>
        <div className="p-6 rounded-xl border border-foreground/10 bg-foreground/5 shadow-sm">
          <h3 className="text-lg font-medium text-foreground/70">Roadmaps</h3>
          <p className="text-4xl font-extrabold mt-2 text-green-500">{stats.roadmaps}</p>
        </div>
      </div>

      <h2 className="text-xl font-bold mb-4">Career Breakdown</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="p-6 rounded-xl border border-foreground/10 bg-gradient-to-br from-indigo-500/10 to-transparent">
          <h3 className="text-lg font-medium text-foreground/70">Core Careers</h3>
          <p className="text-3xl font-bold mt-2 text-indigo-500">{stats.core_careers}</p>
        </div>
        <div className="p-6 rounded-xl border border-foreground/10 bg-gradient-to-br from-cyan-500/10 to-transparent">
          <h3 className="text-lg font-medium text-foreground/70">IT & Digital Careers</h3>
          <p className="text-3xl font-bold mt-2 text-cyan-500">{stats.it_careers}</p>
        </div>
        <div className="p-6 rounded-xl border border-foreground/10 bg-gradient-to-br from-amber-500/10 to-transparent">
          <h3 className="text-lg font-medium text-foreground/70">Government & PSU</h3>
          <p className="text-3xl font-bold mt-2 text-amber-500">{stats.govt_careers}</p>
        </div>
      </div>

      <h2 className="text-xl font-bold mt-12 mb-4">Manage Feedback</h2>
      {pendingFeedback.length === 0 ? (
        <div className="p-8 text-center text-foreground/50 border border-foreground/10 rounded-xl bg-foreground/5">
          No pending feedback to review.
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {pendingFeedback.map(fb => (
            <div key={fb.id} className="p-6 rounded-xl border border-foreground/10 bg-foreground/5 flex flex-col justify-between">
              <div>
                <div className="flex justify-between items-start mb-2">
                  <div>
                    <h4 className="font-bold">{fb.name}</h4>
                    <p className="text-sm text-foreground/60">{fb.branch}</p>
                  </div>
                  <div className="text-yellow-500 text-sm">
                    {'★'.repeat(fb.rating)}{'☆'.repeat(5-fb.rating)}
                  </div>
                </div>
                <p className="italic text-foreground/80 mb-4">"{fb.text}"</p>
              </div>
              <div className="flex gap-3">
                <button 
                  onClick={() => handleApprove(fb.id)}
                  className="px-4 py-2 bg-green-500/10 text-green-600 border border-green-500/20 rounded-lg hover:bg-green-500/20 transition-colors font-medium text-sm flex-1"
                >
                  Approve
                </button>
                <button 
                  onClick={() => handleReject(fb.id)}
                  className="px-4 py-2 bg-red-500/10 text-red-600 border border-red-500/20 rounded-lg hover:bg-red-500/20 transition-colors font-medium text-sm flex-1"
                >
                  Reject & Delete
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      <h2 className="text-xl font-bold mt-12 mb-4">Approved Feedback (Live on Site)</h2>
      {approvedFeedback.length === 0 ? (
        <div className="p-8 text-center text-foreground/50 border border-foreground/10 rounded-xl bg-foreground/5 mb-20">
          No approved feedback to show.
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-20">
          {approvedFeedback.map(fb => (
            <div key={fb.id} className="p-6 rounded-xl border border-green-500/20 bg-green-500/5 flex flex-col justify-between">
              <div>
                <div className="flex justify-between items-start mb-2">
                  <div>
                    <h4 className="font-bold">{fb.name}</h4>
                    <p className="text-sm text-foreground/60">{fb.branch}</p>
                  </div>
                  <div className="text-yellow-500 text-sm">
                    {'★'.repeat(fb.rating)}{'☆'.repeat(5-fb.rating)}
                  </div>
                </div>
                <p className="italic text-foreground/80 mb-4">"{fb.text}"</p>
              </div>
              <div className="flex gap-3 mt-4 pt-4 border-t border-green-500/20">
                <button 
                  onClick={() => handleRejectApproved(fb.id)}
                  className="px-4 py-2 bg-red-500/10 text-red-600 border border-red-500/20 rounded-lg hover:bg-red-500/20 transition-colors font-medium text-sm flex-1"
                >
                  Delete Live Feedback
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
