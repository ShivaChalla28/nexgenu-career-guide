'use client';
import React from 'react';
import { motion } from 'framer-motion';
import Link from 'next/link';
import EngineeringBackground from '@/components/ui/EngineeringBackground';
import Testimonials from '@/components/ui/Testimonials';

const FEATURES = [
  {
    icon: '🗺️',
    title: 'Branch-Specific Roadmaps',
    desc: 'Get tailored career roadmaps built specifically for your engineering branch — not generic advice.',
    color: 'from-blue-500/20 to-blue-600/5',
    border: 'border-blue-500/30',
  },
  {
    icon: '🎯',
    title: 'Core + IT + Govt Careers',
    desc: 'Explore Core jobs, IT & Digital transitions, and Government & PSU opportunities — all in one place.',
    color: 'from-purple-500/20 to-purple-600/5',
    border: 'border-purple-500/30',
  },
  {
    icon: '📋',
    title: 'Step-by-Step Learning Plans',
    desc: 'Know exactly what to learn, in what order, with 30-day, 90-day and 365-day structured timelines.',
    color: 'from-pink-500/20 to-pink-600/5',
    border: 'border-pink-500/30',
  },
  {
    icon: '🏗️',
    title: 'Industry-Grade Projects',
    desc: 'Build capstone projects that actually impress recruiters and pass ATS systems effortlessly.',
    color: 'from-orange-500/20 to-orange-600/5',
    border: 'border-orange-500/30',
  },
  {
    icon: '📚',
    title: 'Curated Resources',
    desc: 'No more endless searching. Best official docs, YouTube channels, courses, and practice sites — curated.',
    color: 'from-green-500/20 to-green-600/5',
    border: 'border-green-500/30',
  },
  {
    icon: '🏛️',
    title: 'PSU & Govt Career Paths',
    desc: 'GATE, IES, ISRO, DRDO, BHEL, NTPC — complete roadmaps for every major government organization.',
    color: 'from-cyan-500/20 to-cyan-600/5',
    border: 'border-cyan-500/30',
  },
  {
    icon: '🤖',
    title: 'AI-Powered Roadmaps',
    desc: 'Each career roadmap is generated with AI and reviewed for accuracy, depth and industry relevance.',
    color: 'from-violet-500/20 to-violet-600/5',
    border: 'border-violet-500/30',
  },
  {
    icon: '✅',
    title: 'Readiness Checklists',
    desc: 'Know when you are truly job-ready with role-specific interview prep checklists and skill matrices.',
    color: 'from-teal-500/20 to-teal-600/5',
    border: 'border-teal-500/30',
  },
  {
    icon: '🎓',
    title: 'Higher Study Guidance',
    desc: 'Planning for M.Tech, MS abroad, or research? Get detailed guidance on entrance exams and pathways.',
    color: 'from-rose-500/20 to-rose-600/5',
    border: 'border-rose-500/30',
  },
];

const STEPS = [
  { num: '01', title: 'Register Free', desc: 'Create your account with your engineering branch details.' },
  { num: '02', title: 'Choose Your Branch', desc: 'Select from 24 engineering disciplines on your dashboard.' },
  { num: '03', title: 'Explore Careers', desc: 'Browse Core, IT & Digital, and Govt & PSU career paths.' },
  { num: '04', title: 'Follow the Roadmap', desc: 'Get step-by-step guidance and become industry-ready.' },
];

const STATS = [
  { value: '24+', label: 'Engineering Branches' },
  { value: '300+', label: 'Career Roadmaps' },
  { value: '3', label: 'Career Categories' },
  { value: 'Free', label: 'to use' },
];

export default function Home() {
  const [userCount, setUserCount] = React.useState<number | null>(null);
  const [feedbackCount, setFeedbackCount] = React.useState<number>(0);
  const [uiButtons, setUiButtons] = React.useState<any[]>([]);
  const [uiAlerts, setUiAlerts] = React.useState<any[]>([]);

  React.useEffect(() => {
    fetch('https://nexgenu-career-guide.onrender.com/api/admin/stats')
      .then(res => res.json())
      .then(data => {
        if (data && data.users !== undefined) {
          setUserCount(data.users);
        }
        if (data && data.approved_feedback !== undefined) {
          setFeedbackCount(data.approved_feedback);
        }
      })
      .catch(err => console.error("Failed to fetch user count:", err));

    fetch('https://nexgenu-career-guide.onrender.com/api/ui/buttons')
      .then(res => res.json())
      .then(data => {
        if (Array.isArray(data)) {
          setUiButtons(data.filter(b => b.is_active === 1 && b.placement === 'Homepage'));
        }
      })
      .catch(err => console.error(err));

    fetch('https://nexgenu-career-guide.onrender.com/api/ui/alerts')
      .then(res => res.json())
      .then(data => {
        if (Array.isArray(data)) {
          setUiAlerts(data.filter(a => a.is_active === 1));
        }
      })
      .catch(err => console.error(err));
  }, []);

  let displayStats = [...STATS];
  if (feedbackCount > 0) {
    displayStats = [{ value: `${feedbackCount}+`, label: 'Verified Reviews' }, ...displayStats];
  }
  if (userCount !== null) {
    displayStats = [{ value: `${userCount}+`, label: 'Registered Students' }, ...displayStats];
  }

  return (
    <main className="flex min-h-screen flex-col items-center pb-0 w-full overflow-x-hidden relative">
      <div className="absolute inset-0 -z-20 h-full w-full bg-background bg-[radial-gradient(#e5e7eb_1px,transparent_1px)] [background-size:16px_16px] dark:bg-[radial-gradient(#1f2937_1px,transparent_1px)] opacity-30" />
      <EngineeringBackground />


      {/* ── HERO ── */}
      <section className="w-full flex flex-col items-center justify-center text-center px-6 pt-32 pb-24 min-h-[90vh]">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="max-w-5xl"
        >
          <motion.span
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.2 }}
            className="inline-block mb-6 px-5 py-2 rounded-full bg-blue-500/10 border border-blue-500/30 text-blue-400 text-sm font-semibold tracking-wide"
          >
            {userCount !== null ? `🚀 Join ${userCount}+ Students on India's #1 Engineering Career Platform` : `🚀 India's #1 Engineering Career Platform`}
          </motion.span>

          <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight mb-6 leading-tight">
            Your Complete{' '}
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500">
              Career Vision
            </span>
            <br />Roadmap
          </h1>

          <p className="text-lg md:text-xl text-foreground/65 mb-12 max-w-2xl mx-auto leading-relaxed">
            Stop guessing your future. NexGenU guides engineering students step-by-step
            from beginner to industry-ready professional — with branch-specific roadmaps,
            curated resources, and government career paths.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-16">
            <Link href="/auth/login">
              <motion.button 
                whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}
                className="px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 hover:opacity-90 text-white font-bold rounded-2xl shadow-[0_0_40px_rgba(59,130,246,0.3)] transition-all flex items-center gap-2"
              >
                Start Your Journey <span className="text-xl">→</span>
              </motion.button>
            </Link>
            <Link href="/dashboard">
              <motion.button 
                whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}
                className="px-8 py-4 bg-foreground/5 hover:bg-foreground/10 text-foreground font-bold rounded-2xl border border-foreground/10 transition-all backdrop-blur-md"
              >
                Explore Roadmap Demo
              </motion.button>
            </Link>
            
            {uiButtons.map(btn => (
              <a key={btn.id} href={btn.url} target={btn.target} rel="noopener noreferrer">
                <motion.button
                  whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}
                  className={`px-8 py-4 ${btn.color} text-white font-bold rounded-2xl shadow-lg transition-all flex items-center gap-2`}
                >
                  <span>{btn.icon}</span> {btn.name}
                </motion.button>
              </a>
            ))}
          </div>

          {/* Stats Bar */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 }}
            className="flex flex-wrap justify-center gap-8 md:gap-16"
          >
            {displayStats.map((s) => (
              <div key={s.label} className="text-center">
                <p className="text-3xl md:text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-500">
                  {s.value}
                </p>
                <p className="text-sm text-foreground/55 mt-1 font-medium">{s.label}</p>
              </div>
            ))}
          </motion.div>
        </motion.div>
      </section>

      {/* ── HOW IT WORKS ── */}
      <section className="w-full max-w-6xl px-6 py-24 border-t border-foreground/10">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <p className="text-sm text-foreground/50 uppercase tracking-widest mb-3 font-semibold">Simple Process</p>
          <h2 className="text-4xl md:text-5xl font-extrabold">How It Works</h2>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {STEPS.map((step, i) => (
            <motion.div
              key={step.num}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.1 }}
              className="relative p-7 rounded-2xl border border-foreground/10 bg-foreground/3 hover:border-blue-500/30 hover:bg-blue-500/5 transition-all group"
            >
              <span className="text-5xl font-black text-foreground/8 group-hover:text-blue-500/15 transition-colors select-none block mb-4">
                {step.num}
              </span>
              <h3 className="text-lg font-bold mb-2 group-hover:text-blue-400 transition-colors">{step.title}</h3>
              <p className="text-sm text-foreground/60 leading-relaxed">{step.desc}</p>
            </motion.div>
          ))}
        </div>
      </section>

      {/* ── FEATURES GRID ── */}
      <section className="w-full max-w-7xl px-6 py-24 border-t border-foreground/10">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <p className="text-sm text-foreground/50 uppercase tracking-widest mb-3 font-semibold">Everything You Need</p>
          <h2 className="text-4xl md:text-5xl font-extrabold mb-4">Platform Features</h2>
          <p className="text-foreground/60 max-w-xl mx-auto text-lg">
            A complete ecosystem designed exclusively for engineering students in India.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {FEATURES.map((feat, i) => (
            <motion.div
              key={feat.title}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.07 }}
              whileHover={{ y: -6, scale: 1.02 }}
              className={`p-7 rounded-2xl border ${feat.border} bg-gradient-to-br ${feat.color} backdrop-blur-sm transition-all cursor-default`}
            >
              <span className="text-4xl mb-5 block">{feat.icon}</span>
              <h3 className="text-xl font-bold mb-3">{feat.title}</h3>
              <p className="text-sm text-foreground/65 leading-relaxed">{feat.desc}</p>
            </motion.div>
          ))}
        </div>
      </section>

      <Testimonials />

      {/* ── CTA BANNER ── */}
      <section className="w-full max-w-5xl px-6 py-24">
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          whileInView={{ opacity: 1, scale: 1 }}
          viewport={{ once: true }}
          className="relative rounded-3xl overflow-hidden bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 p-12 text-center text-white shadow-2xl"
        >
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_30%_50%,rgba(255,255,255,0.1),transparent)] pointer-events-none" />
          <h2 className="text-4xl md:text-5xl font-extrabold mb-4 relative">
            Ready to build your future?
          </h2>
          <p className="text-white/80 text-lg mb-8 max-w-xl mx-auto relative">
            Join thousands of engineering students who have found their career direction with NexGenU.
          </p>
          <Link
            href="/auth/register"
            className="inline-block px-12 py-4 bg-white text-blue-700 font-extrabold rounded-full text-lg hover:scale-105 transition-transform shadow-lg"
          >
            Register Now — It's Free
          </Link>
        </motion.div>
      </section>

      {/* ── FOOTER ── */}
      <footer className="w-full bg-foreground/5 border-t border-foreground/10 py-14 px-6">
        <div className="max-w-6xl mx-auto flex flex-col md:flex-row justify-between items-center gap-6">
          <div className="text-center md:text-left">
            <h3 className="text-2xl font-extrabold tracking-tighter bg-clip-text text-transparent bg-gradient-to-r from-blue-500 to-purple-600 mb-1">
              NexGenU
            </h3>
            <p className="text-sm text-foreground/50">Career Vision Roadmaps — India's Engineering Career Platform.</p>
          </div>
          <div className="flex flex-wrap justify-center gap-8 text-sm font-medium text-foreground/60">
            <Link href="/auth/register" className="hover:text-blue-500 transition-colors">Register</Link>
            <Link href="/auth/login" className="hover:text-blue-500 transition-colors">Login</Link>
            <Link href="/dashboard" className="hover:text-blue-500 transition-colors">Dashboard</Link>
            <Link href="/faq" className="hover:text-blue-500 transition-colors">FAQ</Link>
            <Link href="/contact" className="hover:text-blue-500 transition-colors">Contact</Link>
          </div>
        </div>
        <p className="text-center text-xs text-foreground/30 mt-8">© 2025 NexGenU. All rights reserved.</p>
      </footer>
    </main>
  );
}
