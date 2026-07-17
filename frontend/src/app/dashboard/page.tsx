'use client';
import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import Link from 'next/link';
import { useRouter } from 'next/navigation';

const BRANCHES = [
  { name: 'Computer Science Engineering (CSE)',         icon: '💻', slug: 'computer-science-engineering',          color: 'from-blue-500/20 to-blue-600/5',   border: 'border-blue-500/20',   tag: 'bg-blue-500/10 text-blue-400' },
  { name: 'Information Technology (IT)',                icon: '🌐', slug: 'information-technology',                color: 'from-cyan-500/20 to-cyan-600/5',    border: 'border-cyan-500/20',   tag: 'bg-cyan-500/10 text-cyan-400' },
  { name: 'Artificial Intelligence & Data Science',    icon: '🧠', slug: 'artificial-intelligence-and-data-science', color: 'from-purple-500/20 to-purple-600/5', border: 'border-purple-500/20', tag: 'bg-purple-500/10 text-purple-400' },
  { name: 'Electronics & Communication Engg (ECE)',    icon: '📡', slug: 'electronics-and-communication-engineering', color: 'from-yellow-500/20 to-yellow-600/5', border: 'border-yellow-500/20', tag: 'bg-yellow-500/10 text-yellow-400' },
  { name: 'Electrical & Electronics Engg (EEE)',       icon: '⚡', slug: 'electrical-and-electronics-engineering', color: 'from-orange-500/20 to-orange-600/5', border: 'border-orange-500/20', tag: 'bg-orange-500/10 text-orange-400' },
  { name: 'Mechanical Engineering',                    icon: '⚙️', slug: 'mechanical-engineering',                color: 'from-slate-500/20 to-slate-600/5',  border: 'border-slate-500/20',  tag: 'bg-slate-500/10 text-slate-400' },
  { name: 'Civil Engineering',                         icon: '🏗️', slug: 'civil-engineering',                    color: 'from-stone-500/20 to-stone-600/5',  border: 'border-stone-500/20',  tag: 'bg-stone-500/10 text-stone-400' },
  { name: 'Chemical Engineering',                      icon: '🧪', slug: 'chemical-engineering',                  color: 'from-green-500/20 to-green-600/5',  border: 'border-green-500/20',  tag: 'bg-green-500/10 text-green-400' },
  { name: 'Automobile Engineering',                    icon: '🚗', slug: 'automobile-engineering',                color: 'from-red-500/20 to-red-600/5',      border: 'border-red-500/20',    tag: 'bg-red-500/10 text-red-400' },
  { name: 'Biomedical Engineering',                    icon: '🩺', slug: 'biomedical-engineering',                color: 'from-pink-500/20 to-pink-600/5',    border: 'border-pink-500/20',   tag: 'bg-pink-500/10 text-pink-400' },
  { name: 'Mechatronics Engineering',                  icon: '🤖', slug: 'mechatronics-engineering',              color: 'from-violet-500/20 to-violet-600/5', border: 'border-violet-500/20', tag: 'bg-violet-500/10 text-violet-400' },
  { name: 'Instrumentation Engineering',               icon: '🎛️', slug: 'instrumentation-engineering',          color: 'from-indigo-500/20 to-indigo-600/5', border: 'border-indigo-500/20', tag: 'bg-indigo-500/10 text-indigo-400' },
  { name: 'Aeronautical Engineering',                  icon: '✈️', slug: 'aeronautical-engineering',              color: 'from-sky-500/20 to-sky-600/5',      border: 'border-sky-500/20',    tag: 'bg-sky-500/10 text-sky-400' },
  { name: 'Agricultural Engineering',                  icon: '🌾', slug: 'agricultural-engineering',              color: 'from-lime-500/20 to-lime-600/5',    border: 'border-lime-500/20',   tag: 'bg-lime-500/10 text-lime-400' },
  { name: 'Marine Engineering',                        icon: '⚓', slug: 'marine-engineering',                    color: 'from-teal-500/20 to-teal-600/5',    border: 'border-teal-500/20',   tag: 'bg-teal-500/10 text-teal-400' },
  { name: 'Mining Engineering',                        icon: '⛏️', slug: 'mining-engineering',                   color: 'from-amber-500/20 to-amber-600/5',  border: 'border-amber-500/20',  tag: 'bg-amber-500/10 text-amber-400' },
  { name: 'Industrial Engineering',                    icon: '🏭', slug: 'industrial-engineering',                color: 'from-zinc-500/20 to-zinc-600/5',    border: 'border-zinc-500/20',   tag: 'bg-zinc-500/10 text-zinc-400' },
  { name: 'Production Engineering',                    icon: '🛠️', slug: 'production-engineering',               color: 'from-neutral-500/20 to-neutral-600/5', border: 'border-neutral-500/20', tag: 'bg-neutral-500/10 text-neutral-400' },
  { name: 'Metallurgical Engineering',                 icon: '🔥', slug: 'metallurgical-engineering',             color: 'from-rose-500/20 to-rose-600/5',    border: 'border-rose-500/20',   tag: 'bg-rose-500/10 text-rose-400' },
  { name: 'Petroleum Engineering',                     icon: '🛢️', slug: 'petroleum-engineering',                color: 'from-orange-500/20 to-orange-600/5', border: 'border-orange-500/20', tag: 'bg-orange-500/10 text-orange-400' },
  { name: 'Textile Engineering',                       icon: '🧵', slug: 'textile-engineering',                  color: 'from-fuchsia-500/20 to-fuchsia-600/5', border: 'border-fuchsia-500/20', tag: 'bg-fuchsia-500/10 text-fuchsia-400' },
  { name: 'Biotechnology Engineering',                 icon: '🧬', slug: 'biotechnology-engineering',            color: 'from-emerald-500/20 to-emerald-600/5', border: 'border-emerald-500/20', tag: 'bg-emerald-500/10 text-emerald-400' },
  { name: 'Food Technology',                           icon: '🍎', slug: 'food-technology',                      color: 'from-green-500/20 to-green-600/5',  border: 'border-green-500/20',  tag: 'bg-green-500/10 text-green-400' },
  { name: 'Environmental Engineering',                 icon: '🌍', slug: 'environmental-engineering',            color: 'from-teal-500/20 to-teal-600/5',    border: 'border-teal-500/20',   tag: 'bg-teal-500/10 text-teal-400' },
];

const QUICK_FEATURES = [
  { icon: '🗺️', label: 'Step-by-Step Roadmaps',    desc: 'Structured learning paths for any career' },
  { icon: '🏛️', label: 'Govt & PSU Careers',       desc: 'GATE, IES, ISRO, DRDO, BHEL & more'      },
  { icon: '💻', label: 'IT & Digital Transitions', desc: 'Switch into tech from any branch'         },
  { icon: '📋', label: 'Skill Checklists',          desc: 'Know exactly when you are job-ready'     },
];

export default function Dashboard() {
  const router = useRouter();
  const [user, setUser] = useState<{ full_name?: string; branch?: string; user_id?: string; role?: string } | null>(null);
  const [search, setSearch] = useState('');
  const [featureText, setFeatureText] = useState('');
  const [rating, setRating] = useState(5);
  const [featureSent, setFeatureSent] = useState(false);

  const [uiButtons, setUiButtons] = useState<any[]>([]);
  const [uiAlerts, setUiAlerts] = useState<any[]>([]);

  useEffect(() => {
    const stored = localStorage.getItem('nexgenu_user');
    if (!stored) {
      router.push('/auth/login');
      return;
    }
    setUser(JSON.parse(stored));

    fetch('http://localhost:8000/api/ui/buttons')
      .then(res => res.json())
      .then(data => {
        if (Array.isArray(data)) {
          setUiButtons(data.filter(b => b.is_active === 1 && b.placement === 'Dashboard'));
        }
      })
      .catch(err => console.error(err));

    fetch('http://localhost:8000/api/ui/alerts')
      .then(res => res.json())
      .then(data => {
        if (Array.isArray(data)) {
          setUiAlerts(data.filter(a => a.is_active === 1));
        }
      })
      .catch(err => console.error(err));
  }, [router]);

  const firstName = user?.full_name?.split(' ')[0] || 'Explorer';

  const filtered = BRANCHES.filter(b =>
    b.name.toLowerCase().includes(search.toLowerCase())
  );

  const handleFeatureSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!featureText.trim() || !user) return;
    
    try {
      const res = await fetch('http://localhost:8000/api/feedback/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: user.user_id,
          name: user.full_name,
          branch: user.branch,
          college: '',
          rating: rating,
          text: featureText
        })
      });
      if (res.ok) {
        setFeatureSent(true);
        setFeatureText('');
        setRating(5);
        setTimeout(() => setFeatureSent(false), 4000);
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('nexgenu_user');
    localStorage.removeItem('nexgenu_role');
    router.push('/');
  };

  if (!user) return null;

  return (
    <main className="flex min-h-screen flex-col pt-24 pb-20 px-6 max-w-7xl mx-auto w-full">
      <div className="absolute inset-0 -z-10 h-full w-full bg-background bg-[radial-gradient(#e5e7eb_1px,transparent_1px)] [background-size:16px_16px] dark:bg-[radial-gradient(#1f2937_1px,transparent_1px)] opacity-20" />


      {/* ── Welcome Banner ── */}
      <motion.div
        initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}
        className="relative rounded-3xl overflow-hidden bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 p-8 md:p-10 mb-10 text-white shadow-2xl"
      >
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_20%_50%,rgba(255,255,255,0.12),transparent)] pointer-events-none" />
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-6 relative z-10">
          <div>
            <span className="inline-block py-1 px-3 rounded-full bg-white/20 text-white text-xs font-bold tracking-widest uppercase mb-3 backdrop-blur-sm border border-white/20">
              Student Portal
            </span>
            <h1 className="text-4xl md:text-5xl font-extrabold mb-3">
              Welcome back, {firstName} 👋
            </h1>
            <p className="text-white/80 text-lg max-w-2xl font-medium">
              Ready to take the next step in your career? Explore branch-specific roadmaps, check your readiness, and prepare for interviews!
            </p>
            
            {uiButtons.length > 0 && (
              <div className="mt-6 flex flex-wrap gap-3">
                {uiButtons.map(btn => (
                  <a key={btn.id} href={btn.url} target={btn.target} rel="noopener noreferrer">
                    <button className={`px-5 py-2.5 ${btn.color} text-white font-bold rounded-xl shadow-lg transition-transform hover:scale-105 flex items-center gap-2 border border-white/20 backdrop-blur-md`}>
                      <span>{btn.icon}</span> {btn.name}
                    </button>
                  </a>
                ))}
              </div>
            )}
          </div>
          <div className="flex gap-3 flex-shrink-0">
            {user.role === 'admin' && (
              <Link href="/admin"
                className="px-5 py-2.5 bg-white/20 hover:bg-white/30 rounded-xl font-semibold text-sm transition border border-white/20">
                ⚙️ Admin Panel
              </Link>
            )}
            <button onClick={handleLogout}
              className="px-5 py-2.5 bg-white/10 hover:bg-white/20 rounded-xl font-semibold text-sm transition border border-white/20">
              Logout
            </button>
          </div>
        </div>

        {/* Quick Feature Pills */}
        <div className="flex flex-wrap gap-3 mt-8">
          {QUICK_FEATURES.map(f => (
            <div key={f.label} className="flex items-center gap-2 px-4 py-2 bg-white/10 rounded-full border border-white/15 text-sm">
              <span>{f.icon}</span>
              <span className="font-semibold">{f.label}</span>
            </div>
          ))}
        </div>
      </motion.div>

      {/* ── Branch Explorer ── */}
      <section className="mb-16">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-8">
          <div>
            <h2 className="text-3xl font-extrabold">All Engineering Branches</h2>
            <p className="text-foreground/55 mt-1">
              Select your branch to explore Core, IT & Digital, and Govt & PSU careers.
            </p>
          </div>
          {/* Search */}
          <div className="relative w-full md:w-72">
            <span className="absolute left-4 top-1/2 -translate-y-1/2 text-foreground/40">🔍</span>
            <input
              type="text"
              placeholder="Search branch..."
              value={search}
              onChange={e => setSearch(e.target.value)}
              className="w-full pl-10 pr-4 py-3 rounded-xl bg-foreground/5 border border-foreground/10 focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 transition text-sm"
            />
          </div>
        </div>

        {filtered.length === 0 ? (
          <div className="text-center py-20 text-foreground/40">
            <p className="text-4xl mb-3">🔍</p>
            <p className="font-semibold">No branch found for "{search}"</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5">
            {filtered.map((branch, i) => (
              <motion.div
                key={branch.slug}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.03 }}
                whileHover={{ y: -5, scale: 1.02 }}
              >
                <Link href={`/dashboard/branches/${branch.slug}`}>
                  <div className={`p-6 rounded-2xl border ${branch.border} bg-gradient-to-br ${branch.color} cursor-pointer transition-all h-full flex flex-col justify-between group min-h-[160px]`}>
                    <div>
                      <span className="text-4xl mb-3 block">{branch.icon}</span>
                      <h3 className="font-bold text-base leading-snug group-hover:text-blue-400 transition-colors mb-3">
                        {branch.name}
                      </h3>
                    </div>
                    <div className="flex items-center justify-between mt-2">
                      <span className={`text-xs font-semibold px-2 py-1 rounded-full ${branch.tag}`}>
                        View Roadmaps
                      </span>
                      <svg className="w-4 h-4 text-foreground/30 group-hover:text-blue-400 group-hover:translate-x-1 transition-all" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                      </svg>
                    </div>
                  </div>
                </Link>
              </motion.div>
            ))}
          </div>
        )}
      </section>

      {/* ── Share Feedback ── */}
      <motion.section
        initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }}
        className="rounded-3xl border border-foreground/10 bg-foreground/3 p-8 md:p-10"
      >
        <div className="max-w-2xl mx-auto text-center">
          <p className="text-3xl mb-3">⭐</p>
          <h2 className="text-2xl font-extrabold mb-2">Share Your Feedback</h2>
          <p className="text-foreground/55 mb-6 text-sm">
            How has NexGenU helped you? Make the platform available to all!
          </p>

          {featureSent ? (
            <motion.div initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }}
              className="p-4 rounded-xl bg-green-500/10 border border-green-500/30 text-green-400 font-semibold">
              ✅ Thank you! Your feedback has been sent to the admin for review.
            </motion.div>
          ) : (
            <form onSubmit={handleFeatureSubmit} className="flex flex-col gap-4">
              <div className="flex justify-center gap-2 mb-2">
                {[1, 2, 3, 4, 5].map(star => (
                  <button
                    key={star}
                    type="button"
                    onClick={() => setRating(star)}
                    className={`text-3xl transition-transform hover:scale-110 ${star <= rating ? 'text-yellow-500' : 'text-foreground/20'}`}
                  >
                    ★
                  </button>
                ))}
              </div>
              <textarea
                rows={4}
                placeholder="e.g. The EEE roadmap was exactly what I needed to prepare for my PSU exams! Highly recommended."
                value={featureText}
                onChange={e => setFeatureText(e.target.value)}
                className="w-full px-4 py-3 rounded-xl bg-foreground/5 border border-foreground/10 focus:outline-none focus:border-purple-500 focus:ring-2 focus:ring-purple-500/20 transition text-sm resize-none placeholder:text-foreground/30"
                required
              />
              <button
                type="submit"
                className="self-center px-8 py-3 bg-gradient-to-r from-purple-600 to-blue-600 text-white font-bold rounded-xl hover:opacity-90 transition shadow-lg shadow-purple-500/20"
              >
                Submit Feedback →
              </button>
            </form>
          )}
        </div>
      </motion.section>

      {/* Dynamic Alerts Section */}
      {uiAlerts.length > 0 && (
        <div className="w-full flex flex-col gap-3 mt-16 relative z-10">
          <h2 className="text-xl font-bold mb-2">Important Alerts</h2>
          {uiAlerts.map(alert => {
            const bgClass = alert.priority === 'High' ? 'bg-red-500/10 border-red-500/30 text-red-600' :
                            alert.priority === 'Medium' ? 'bg-yellow-500/10 border-yellow-500/30 text-yellow-600' :
                            'bg-blue-500/10 border-blue-500/30 text-blue-600';
            return (
              <motion.div 
                key={alert.id}
                initial={{ opacity: 0, y: -20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }}
                className={`w-full p-4 rounded-xl border flex flex-col md:flex-row md:items-center justify-between gap-4 backdrop-blur-md ${bgClass}`}
              >
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <span className="font-bold">{alert.title}</span>
                    <span className="text-xs px-2 py-0.5 rounded-full bg-background/50 border border-current/20">{alert.type}</span>
                  </div>
                  <p className="text-sm opacity-90">{alert.message}</p>
                </div>
              </motion.div>
            )
          })}
        </div>
      )}
    </main>
  );
}
