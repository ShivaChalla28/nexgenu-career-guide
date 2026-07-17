'use client';
import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';

export default function AdminLayout({ children }: { children: React.ReactNode }) {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [userId, setUserId] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    if (sessionStorage.getItem('nexgenu_admin_auth') === 'true') {
      setIsAuthenticated(true);
    }
  }, []);

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    if (userId === '22191A0228@Archana' && password === '23JR1A595@ShivaChalla') {
      sessionStorage.setItem('nexgenu_admin_auth', 'true');
      setIsAuthenticated(true);
      setError('');
    } else {
      setError('Invalid Admin Credentials!');
    }
  };

  const handleLogout = () => {
    sessionStorage.removeItem('nexgenu_admin_auth');
    setIsAuthenticated(false);
  };

  if (!mounted) return null;

  if (!isAuthenticated) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-background pt-20">
        <div className="w-full max-w-md p-8 bg-foreground/5 rounded-2xl border border-foreground/10 shadow-2xl">
          <div className="text-center mb-8">
            <h2 className="text-3xl font-extrabold tracking-tighter bg-clip-text text-transparent bg-gradient-to-r from-blue-500 to-purple-600 mb-2">NexGenU Admin</h2>
            <p className="text-foreground/60 text-sm">Authorized Personnel Only</p>
          </div>
          
          {error && (
            <div className="mb-4 p-3 bg-red-500/10 border border-red-500/30 rounded-lg text-red-500 text-sm text-center font-medium">
              {error}
            </div>
          )}

          <form onSubmit={handleLogin} className="space-y-5">
            <div>
              <label className="block text-sm font-semibold mb-1.5 text-foreground/80">Admin User ID</label>
              <input 
                type="text" 
                value={userId} 
                onChange={(e) => setUserId(e.target.value)} 
                className="w-full p-3 bg-background border border-foreground/10 rounded-xl focus:outline-none focus:border-blue-500 transition-colors" 
                placeholder="Enter User ID"
                required 
              />
            </div>
            <div>
              <label className="block text-sm font-semibold mb-1.5 text-foreground/80">Password</label>
              <input 
                type="password" 
                value={password} 
                onChange={(e) => setPassword(e.target.value)} 
                className="w-full p-3 bg-background border border-foreground/10 rounded-xl focus:outline-none focus:border-purple-500 transition-colors" 
                placeholder="Enter Password"
                required 
              />
            </div>
            <button 
              type="submit" 
              className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:opacity-90 text-white font-bold py-3 rounded-xl shadow-lg shadow-blue-500/20 transition-all mt-2"
            >
              Access Dashboard
            </button>
          </form>
          
          <div className="mt-6 text-center">
            <Link href="/" className="text-sm text-foreground/50 hover:text-foreground/80 transition-colors">
              &larr; Back to Main Site
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen bg-background pt-20">
      <aside className="w-64 border-r border-foreground/10 bg-foreground/5 p-6 flex flex-col fixed h-full z-10 overflow-y-auto pb-24">
        <h2 className="text-xl font-extrabold tracking-tighter bg-clip-text text-transparent bg-gradient-to-r from-blue-500 to-purple-600 mb-8">NexGenU Admin</h2>
        <nav className="flex flex-col space-y-4 flex-1">
          <Link href="/admin" className="text-sm font-semibold text-foreground/70 hover:text-blue-500 transition-colors">📊 Dashboard</Link>
          <Link href="/admin/users" className="text-sm font-semibold text-foreground/70 hover:text-blue-500 transition-colors">👥 Manage Users</Link>
          <Link href="/admin/branches" className="text-sm font-semibold text-foreground/70 hover:text-blue-500 transition-colors">🏢 Manage Branches</Link>
          <Link href="/admin/careers" className="text-sm font-semibold text-foreground/70 hover:text-blue-500 transition-colors">💼 Manage Careers</Link>
          <Link href="/admin/roadmaps" className="text-sm font-semibold text-foreground/70 hover:text-blue-500 transition-colors">🗺️ Manage Roadmaps</Link>
          
          <div className="border-t border-foreground/10 my-4"></div>
          
          <Link href="/admin/buttons" className="text-sm font-semibold text-foreground/70 hover:text-purple-500 transition-colors">🔘 Button Manager</Link>
          <Link href="/admin/alerts" className="text-sm font-semibold text-foreground/70 hover:text-purple-500 transition-colors">🔔 Alert Manager</Link>
          <Link href="/admin/ads" className="text-sm font-semibold text-foreground/70 hover:text-purple-500 transition-colors">📢 Ad Manager</Link>
          
          <div className="border-t border-foreground/10 my-4"></div>
          
          <Link href="/admin/seo" className="text-sm font-semibold text-foreground/70 hover:text-green-500 transition-colors">🔍 SEO Manager</Link>
        </nav>
        
        <div className="mt-8 pt-4 border-t border-foreground/10">
          <button 
            onClick={handleLogout}
            className="w-full py-2 px-4 bg-red-500/10 text-red-500 hover:bg-red-500/20 text-sm font-semibold rounded-lg transition-colors text-left flex items-center gap-2"
          >
            <span>🚪</span> Logout Admin
          </button>
        </div>
      </aside>
      <main className="flex-1 p-8 ml-64 overflow-y-auto">
        {children}
      </main>
    </div>
  );
}
