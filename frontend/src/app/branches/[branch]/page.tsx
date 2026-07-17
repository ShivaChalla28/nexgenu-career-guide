'use client';
import React, { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Link from 'next/link';

interface Career {
  id: string;
  name: string;
  slug: string;
  category?: string;
  overview?: string;
  india_salary?: string;
  industry_demand?: string;
}

const TABS = [
  { id: 'Core Careers',            label: 'Core Careers',          icon: '🏗️', color: 'blue'   },
  { id: 'IT & Digital Careers',    label: 'IT & Digital Careers',  icon: '💻', color: 'purple' },
  { id: 'Government & PSU Careers',label: 'Govt & PSU Careers',    icon: '🏛️', color: 'green'  },
];

const TAB_COLORS: Record<string, string> = {
  blue:   'border-blue-500 text-blue-500 bg-blue-500/10',
  purple: 'border-purple-500 text-purple-500 bg-purple-500/10',
  green:  'border-green-500 text-green-500 bg-green-500/10',
};

const CAREER_ICONS: Record<string, string> = {
  engineer: '⚙️', developer: '💻', designer: '🎨', analyst: '📊',
  manager: '📋', scientist: '🔬', architect: '🏗️', security: '🔒',
  cloud: '☁️', ai: '🤖', data: '📈', network: '🌐',
  embedded: '🖥️', robotics: '🦾', iot: '📡', solar: '☀️',
  wind: '💨', power: '⚡', plc: '🔧', scada: '🖥️',
  automation: '🔩', renewable: '🌱', cyber: '🛡️', vlsi: '🔬',
  telecom: '📶', control: '🎮', protection: '⚔️', substation: '🏭',
  transmission: '🗼', distribution: '💡',
};

function getIcon(name: string): string {
  const lower = name.toLowerCase();
  for (const [key, icon] of Object.entries(CAREER_ICONS)) {
    if (lower.includes(key)) return icon;
  }
  return '🎯';
}

function getCardAccent(category?: string): string {
  if (category === 'IT & Digital Careers')    return 'hover:border-purple-500/40 hover:bg-purple-500/5';
  if (category === 'Government & PSU Careers') return 'hover:border-green-500/40 hover:bg-green-500/5';
  return 'hover:border-blue-500/40 hover:bg-blue-500/5';
}

function getTagColor(category?: string): string {
  if (category === 'IT & Digital Careers')    return 'bg-purple-500/10 text-purple-400';
  if (category === 'Government & PSU Careers') return 'bg-green-500/10 text-green-400';
  return 'bg-blue-500/10 text-blue-400';
}

export default function BranchCareers({ params }: { params: { branch: string } }) {
  const [allCareers, setAllCareers] = useState<Career[]>([]);
  const [branchName, setBranchName] = useState('');
  const [activeTab, setActiveTab] = useState('Core Careers');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchCareers = async () => {
      try {
        const slug = params.branch;
        const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || ''}/api/branches/${slug}/careers`);
        if (!res.ok) {
          const errText = await res.text();
          throw new Error(`HTTP ${res.status}: ${errText}`);
        }
        const data = await res.json();
        setBranchName(data.branch?.name || slug.replace(/-/g, ' '));
        setAllCareers(data.careers || []);
      } catch (err: unknown) {
        const msg = err instanceof Error ? err.message : 'Unknown error';
        setError(`Could not load careers: ${msg}`);
      } finally {
        setLoading(false);
      }
    };
    fetchCareers();
  }, [params.branch]);

  // Group careers by category
  const grouped = TABS.reduce((acc, tab) => {
    acc[tab.id] = allCareers.filter(c => (c.category || 'Core Careers') === tab.id);
    return acc;
  }, {} as Record<string, Career[]>);

  const visibleCareers = grouped[activeTab] || [];

  return (
    <main className="flex min-h-screen flex-col items-center pt-28 pb-16 px-6">
      <div className="absolute inset-0 -z-10 h-full w-full bg-background bg-[radial-gradient(#e5e7eb_1px,transparent_1px)] [background-size:16px_16px] dark:bg-[radial-gradient(#1f2937_1px,transparent_1px)] opacity-30" />

      {/* Header */}
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="text-center max-w-4xl mb-10">
        <p className="text-sm text-foreground/50 uppercase tracking-widest mb-2 font-medium">Engineering Branch</p>
        <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight mb-4">
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500">
            {branchName || params.branch.replace(/-/g, ' ')}
          </span>
        </h1>
        <p className="text-lg text-foreground/60">
          Choose your career path below and get a complete step-by-step roadmap.
        </p>
      </motion.div>

      {/* Tabs */}
      {!loading && !error && (
        <div className="flex flex-wrap justify-center gap-3 mb-10">
          {TABS.map(tab => {
            const count = grouped[tab.id]?.length || 0;
            const isActive = activeTab === tab.id;
            const colorClass = TAB_COLORS[tab.color];
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-2 px-5 py-2.5 rounded-full border-2 font-semibold text-sm transition-all duration-200 ${
                  isActive
                    ? colorClass
                    : 'border-foreground/15 text-foreground/60 hover:border-foreground/30 hover:text-foreground'
                }`}
              >
                <span>{tab.icon}</span>
                <span>{tab.label}</span>
                {count > 0 && (
                  <span className={`px-2 py-0.5 rounded-full text-xs font-bold ${isActive ? 'bg-current/20' : 'bg-foreground/10'}`}>
                    {count}
                  </span>
                )}
              </button>
            );
          })}
        </div>
      )}

      {/* Loading */}
      {loading && (
        <div className="flex flex-col items-center gap-4 mt-16">
          <div className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin" />
          <p className="text-foreground/50">Loading careers...</p>
        </div>
      )}

      {/* Error */}
      {error && (
        <div className="mt-8 p-5 rounded-xl bg-red-500/10 border border-red-500/30 text-red-400 max-w-lg text-center">
          ⚠️ {error}
        </div>
      )}

      {/* Empty Tab */}
      {!loading && !error && visibleCareers.length === 0 && (
        <div className="mt-8 p-8 rounded-2xl bg-foreground/5 border border-foreground/10 text-center max-w-md">
          <p className="text-3xl mb-3">🔍</p>
          <p className="font-semibold mb-1">No careers in this category yet</p>
          <p className="text-sm text-foreground/50">Run <code className="bg-foreground/10 px-1 rounded">python fix_categories.py</code> to categorize careers.</p>
        </div>
      )}

      {/* Career Grid */}
      {!loading && !error && visibleCareers.length > 0 && (
        <AnimatePresence mode="wait">
          <motion.div
            key={activeTab}
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -8 }}
            transition={{ duration: 0.2 }}
            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 w-full max-w-6xl"
          >
            {visibleCareers.map((career, i) => (
              <Link href={`/careers/${career.slug}`} key={career.id}>
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: i * 0.04 }}
                  whileHover={{ y: -5, scale: 1.02 }}
                  className={`p-6 rounded-2xl border border-foreground/10 bg-foreground/3 backdrop-blur-sm transition-all cursor-pointer h-full flex flex-col justify-between group ${getCardAccent(career.category)}`}
                >
                  <div>
                    <div className="flex items-start justify-between mb-3">
                      <span className="text-3xl">{getIcon(career.name)}</span>
                      <span className={`text-xs font-semibold px-2 py-1 rounded-full ${getTagColor(career.category)}`}>
                        {career.category === 'IT & Digital Careers' ? 'IT & Digital' :
                         career.category === 'Government & PSU Careers' ? 'Govt & PSU' : 'Core'}
                      </span>
                    </div>
                    <h3 className="font-bold text-xl mb-2 group-hover:text-blue-400 transition-colors">
                      {career.name}
                    </h3>
                    {career.india_salary && (
                      <p className="text-xs font-semibold text-green-400 mb-2">
                        💰 {career.india_salary.split(',')[0]}
                      </p>
                    )}
                    <p className="text-sm text-foreground/55 line-clamp-2">
                      {career.overview || `Complete roadmap and skills guide for ${career.name}.`}
                    </p>
                  </div>
                  <div className="mt-4 text-sm font-semibold flex items-center gap-1 text-blue-400">
                    View Full Roadmap
                    <svg className="w-4 h-4 group-hover:translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                    </svg>
                  </div>
                </motion.div>
              </Link>
            ))}
          </motion.div>
        </AnimatePresence>
      )}
    </main>
  );
}
