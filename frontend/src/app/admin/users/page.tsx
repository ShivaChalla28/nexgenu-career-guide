'use client';
import React, { useState, useEffect } from 'react';

export default function ManageUsers() {
  const [users, setUsers] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(0);

  const fetchUsers = () => {
    setLoading(true);
    fetch(`${process.env.NEXT_PUBLIC_API_URL || ''}/api/admin/users?skip=${page * 50}&limit=50`)
      .then(res => res.json())
      .then(data => { setUsers(data); setLoading(false); })
      .catch(err => { console.error(err); setLoading(false); });
  };

  useEffect(() => { fetchUsers(); }, [page]);

  const handleDelete = async (id: string) => {
    if (!confirm('Are you sure you want to delete this user?')) return;
    try {
      await fetch(`${process.env.NEXT_PUBLIC_API_URL || ''}/api/admin/users/${id}`, { method: 'DELETE' });
      fetchUsers();
    } catch (err) { console.error(err); }
  };

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Manage Users</h1>
      <div className="bg-foreground/5 rounded-xl border border-foreground/10 overflow-hidden">
        <table className="w-full text-left">
          <thead className="bg-foreground/10 border-b border-foreground/10">
            <tr>
              <th className="p-4 font-semibold">Name</th>
              <th className="p-4 font-semibold">Email</th>
              <th className="p-4 font-semibold">Branch</th>
              <th className="p-4 font-semibold">Role</th>
              <th className="p-4 font-semibold">Actions</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr><td colSpan={5} className="p-8 text-center text-foreground/50">Loading users...</td></tr>
            ) : users.map((u: any) => (
              <tr key={u.id} className="border-b border-foreground/10 last:border-0 hover:bg-foreground/5">
                <td className="p-4 font-medium">{u.full_name}</td>
                <td className="p-4 text-foreground/70">{u.email}</td>
                <td className="p-4 text-foreground/70">{u.branch || 'N/A'}</td>
                <td className="p-4">
                  <span className={`px-2 py-1 rounded text-xs font-semibold ${u.role === 'admin' ? 'bg-purple-500/20 text-purple-500' : 'bg-blue-500/20 text-blue-500'}`}>
                    {u.role}
                  </span>
                </td>
                <td className="p-4"><button onClick={() => handleDelete(u.id)} className="text-red-500 hover:underline">Delete</button></td>
              </tr>
            ))}
          </tbody>
        </table>
        <div className="p-4 border-t border-foreground/10 flex justify-between items-center bg-foreground/5">
          <button onClick={() => setPage(p => Math.max(0, p - 1))} disabled={page === 0} className="px-4 py-2 bg-foreground/10 rounded disabled:opacity-50">Previous</button>
          <span className="text-sm font-medium">Page {page + 1}</span>
          <button onClick={() => setPage(p => p + 1)} disabled={users.length < 50} className="px-4 py-2 bg-foreground/10 rounded disabled:opacity-50">Next</button>
        </div>
      </div>
    </div>
  );
}
