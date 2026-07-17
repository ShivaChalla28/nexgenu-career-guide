'use client';
import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { useRouter, usePathname } from 'next/navigation';

export default function Navbar() {
  const router = useRouter();
  const pathname = usePathname();
  const [scrolled, setScrolled] = useState(false);
  const [user, setUser] = useState<{ full_name?: string; role?: string } | null>(null);
  const [menuOpen, setMenuOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 50);
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  // Re-read user from localStorage on each route change
  useEffect(() => {
    const stored = localStorage.getItem('nexgenu_user');
    setUser(stored ? JSON.parse(stored) : null);
  }, [pathname]);

  const handleLogout = () => {
    localStorage.removeItem('nexgenu_user');
    localStorage.removeItem('nexgenu_role');
    setUser(null);
    router.push('/');
  };

  const firstName = user?.full_name?.split(' ')[0] || '';

  const isLoggedIn = !!user;
  const isDashboard = pathname?.startsWith('/dashboard') || pathname?.startsWith('/admin');

  return (
    <nav className={`sticky top-0 w-full z-50 transition-all duration-300 ${
      scrolled || isDashboard
        ? 'bg-background/90 backdrop-blur-md border-b border-foreground/10 py-3'
        : 'bg-transparent py-5'
    }`}>
      <div className="container mx-auto px-6 md:px-10 flex justify-between items-center">
        {/* Logo */}
        <Link href={isLoggedIn ? '/dashboard' : '/'} className="text-2xl font-extrabold tracking-tighter bg-clip-text text-transparent bg-gradient-to-r from-blue-500 to-purple-600">
          NexGenU
        </Link>

        {/* Desktop Nav */}
        <div className="hidden md:flex items-center gap-6">
          {isLoggedIn ? (
            <>
              <Link href="/dashboard" className={`text-sm font-semibold transition-colors hover:text-blue-400 ${pathname === '/dashboard' ? 'text-blue-400' : 'text-foreground/70'}`}>
                🏠 Dashboard
              </Link>
              {user?.role === 'admin' && (
                <Link href="/admin" className={`text-sm font-semibold transition-colors hover:text-purple-400 ${pathname?.startsWith('/admin') ? 'text-purple-400' : 'text-foreground/70'}`}>
                  ⚙️ Admin
                </Link>
              )}
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-white text-xs font-bold">
                  {firstName[0]?.toUpperCase() || 'U'}
                </div>
                <span className="text-sm font-semibold text-foreground/80">{firstName}</span>
                <button
                  onClick={handleLogout}
                  className="ml-1 px-4 py-2 text-sm font-semibold rounded-xl border border-foreground/15 hover:bg-foreground/10 hover:border-red-500/40 hover:text-red-400 transition-all"
                >
                  Logout
                </button>
              </div>
            </>
          ) : (
            <>
              <Link href="/" className="text-sm font-medium text-foreground/70 hover:text-foreground transition-colors">Home</Link>
              <Link href="/auth/login" className="text-sm font-semibold text-foreground/70 hover:text-blue-400 transition-colors">
                Login
              </Link>
              <Link href="/auth/register" className="px-5 py-2.5 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-full text-sm font-bold hover:opacity-90 transition shadow-lg shadow-blue-500/20">
                Get Started Free
              </Link>
            </>
          )}
        </div>

        {/* Mobile Hamburger */}
        <button
          onClick={() => setMenuOpen(!menuOpen)}
          className="md:hidden p-2 rounded-lg hover:bg-foreground/10 transition"
          aria-label="Toggle menu"
        >
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            {menuOpen
              ? <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              : <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
            }
          </svg>
        </button>
      </div>

      {/* Mobile Menu */}
      {menuOpen && (
        <div className="md:hidden bg-background/95 backdrop-blur-md border-t border-foreground/10 px-6 py-4 flex flex-col gap-4">
          {isLoggedIn ? (
            <>
              <Link href="/dashboard" onClick={() => setMenuOpen(false)} className="text-sm font-semibold py-2">🏠 Dashboard</Link>
              {user?.role === 'admin' && (
                <Link href="/admin" onClick={() => setMenuOpen(false)} className="text-sm font-semibold py-2">⚙️ Admin Panel</Link>
              )}
              <button onClick={() => { setMenuOpen(false); handleLogout(); }} className="text-left text-sm font-semibold py-2 text-red-400">
                Logout
              </button>
            </>
          ) : (
            <>
              <Link href="/auth/login" onClick={() => setMenuOpen(false)} className="text-sm font-semibold py-2">Login</Link>
              <Link href="/auth/register" onClick={() => setMenuOpen(false)} className="text-sm font-semibold py-2 text-blue-400">Register Free</Link>
            </>
          )}
        </div>
      )}
    </nav>
  );
}
