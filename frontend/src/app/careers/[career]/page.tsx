'use client';
import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Link from 'next/link';
import { useRouter } from 'next/navigation';

const API = '';

// ── Loading Skeleton ────────────────────────────────────────────────────────
function LoadingSkeleton({ career }: { career: string }) {
  const name = career.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
  const tips = [
    'Analyzing industry demand and salary data…',
    'Building your personalized skills matrix…',
    'Mapping learning phases and milestones…',
    'Curating project ideas for your portfolio…',
    'Preparing interview questions and checklists…',
  ];
  const [tip, setTip] = useState(0);
  useEffect(() => {
    const t = setInterval(() => setTip(p => (p + 1) % tips.length), 1800);
    return () => clearInterval(t);
  }, []);
  return (
    <div className="flex min-h-screen items-center justify-center bg-background pt-20">
      <div className="text-center max-w-lg px-6">
        <div className="w-20 h-20 mx-auto mb-6 relative">
          <div className="absolute inset-0 rounded-full border-4 border-blue-500/20 border-t-blue-500 animate-spin" />
          <div className="absolute inset-3 rounded-full border-4 border-purple-500/20 border-b-purple-500 animate-spin animate-reverse" />
          <span className="absolute inset-0 flex items-center justify-center text-2xl">🗺️</span>
        </div>
        <h1 className="text-3xl font-extrabold mb-2 bg-clip-text text-transparent bg-gradient-to-r from-blue-500 to-purple-600">
          Generating Roadmap
        </h1>
        <p className="text-xl font-bold text-foreground/80 mb-2">{name}</p>
        <AnimatePresence mode="wait">
          <motion.p key={tip} initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -8 }}
            className="text-foreground/55 text-sm mt-4 h-6">{tips[tip]}</motion.p>
        </AnimatePresence>
        <p className="text-xs text-foreground/30 mt-8">Powered by Gemini AI • Takes 5-15 seconds on first visit</p>
      </div>
    </div>
  );
}

// ── Main Component ──────────────────────────────────────────────────────────
export default function CareerRoadmapPage({ params }: { params: { career: string } }) {
  const router = useRouter();
  const slug = params.career;
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [activePlan, setActivePlan] = useState(0);
  const [activeSection, setActiveSection] = useState('overview');

  useEffect(() => {
    async function load() {
      try {
        const res = await fetch(`${API}/api/careers/${slug}`);
        if (!res.ok) throw new Error(`API error ${res.status}`);
        const json = await res.json();
        setData(json);
      } catch (e: any) {
        setError(e.message || 'Failed to load roadmap');
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [slug]);

  const scrollTo = (id: string) => {
    setActiveSection(id);
    document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' });
  };

  const SECTIONS = [
    { id: 'overview',    label: '📋 Career Overview'   },
    { id: 'skills',      label: '🧠 Skills Matrix'     },
    { id: 'roadmap',     label: '🗺️ Learning Roadmap'  },
    { id: 'projects',    label: '💼 Projects'          },
    { id: 'certs',       label: '🏅 Certifications'    },
    { id: 'interview',   label: '🎯 Interview Prep'    },
    { id: 'checklist',   label: '✅ Readiness Check'   },
  ];

  if (loading) return <LoadingSkeleton career={slug} />;

  if (error) return (
    <div className="flex min-h-screen items-center justify-center flex-col gap-4 pt-20">
      <p className="text-4xl">⚠️</p>
      <p className="text-xl font-bold text-red-400">Failed to load roadmap</p>
      <p className="text-foreground/50 text-sm">{error}</p>
      <p className="text-foreground/40 text-xs">Make sure the backend is running at localhost:8000</p>
      <Link href="/dashboard" className="mt-4 px-6 py-2 bg-blue-600 text-white rounded-xl font-semibold">← Back to Dashboard</Link>
    </div>
  );

  const career  = data?.career  || {};
  const roadmap = data?.roadmap || {};

  // Parse JSON strings from DB if needed
  const parse = (val: any) => {
    if (!val) return null;
    if (typeof val === 'string') { try { return JSON.parse(val); } catch { return val; } }
    return val;
  };

  const responsibilities  = parse(career.responsibilities)  || [];
  const growthPath        = parse(career.growth_path)        || [];
  const skillsMatrix      = parse(roadmap.skills_matrix)     || {};
  const learningPlans     = parse(roadmap.learning_plans)    || [];
  const learningSteps     = parse(roadmap.learning_steps)    || [];
  const projects          = parse(roadmap.projects)          || {};
  const certifications    = parse(roadmap.certifications)    || [];
  const interviewPrep     = parse(roadmap.interview_prep)    || {};
  const readinessChecklist = parse(roadmap.readiness_checklist) || [];
  const practiceQs        = parse(roadmap.practice_questions) || {};

  const planList = Array.isArray(learningPlans) ? learningPlans : Object.values(learningPlans);
  const selectedPlan = planList[activePlan] || {};

  function getScaledStep(step: any, index: number, targetMonths: number) {
    // Strip any hardcoded month prefixes from the LLM title
    const cleanTitle = (step.title || '').replace(/^(Months? \d+(?:-\d+)?:?\s*|\d+(?:st|nd|rd|th) Month:?\s*|M\d+(?:-M\d+)?:?\s*)/i, '');
    
    // Calculate new start and end months based on 6 phases total
    const monthsPerPhase = targetMonths / 6;
    const startMonth = Math.floor(index * monthsPerPhase) + 1;
    const endMonth = Math.floor((index + 1) * monthsPerPhase);
    
    // Format nicely
    const isSingleMonth = startMonth >= endMonth;
    const phaseLabel = isSingleMonth ? `Month ${startMonth}` : `Months ${startMonth}-${endMonth}`;
    const phaseShort = isSingleMonth ? `M${startMonth}` : `M${startMonth}-M${endMonth}`;
    const duration = Math.round(monthsPerPhase * 4) + ' Weeks';

    return {
      phase: phaseShort,
      title: `${phaseLabel}: ${cleanTitle}`,
      duration: duration,
      learn: step.learn
    };
  }

  const totalTargetMonths = parseInt(selectedPlan?.duration) || 12;

  return (
    <div className="flex min-h-screen bg-background pt-20 relative">
      {/* Background */}
      <div className="fixed inset-0 -z-10 bg-background bg-[radial-gradient(#e5e7eb_1px,transparent_1px)] dark:bg-[radial-gradient(#1f2937_1px,transparent_1px)] [background-size:20px_20px] opacity-20" />

      {/* ── Sidebar ── */}
      <aside className="w-64 fixed h-[calc(100vh-80px)] overflow-y-auto border-r border-foreground/10 p-6 hidden lg:flex flex-col bg-foreground/3 backdrop-blur-md z-20">
        <button onClick={() => router.back()} className="text-blue-400 hover:text-blue-300 mb-8 inline-flex items-center gap-1 text-sm font-semibold self-start">
          ← Back
        </button>
        <h3 className="font-bold mb-4 uppercase text-foreground/40 text-xs tracking-widest">Roadmap Sections</h3>
        <nav className="flex flex-col gap-1">
          {SECTIONS.map(sec => (
            <button key={sec.id} onClick={() => scrollTo(sec.id)}
              className={`text-left text-sm font-semibold px-3 py-2 rounded-lg transition-all ${
                activeSection === sec.id
                  ? 'bg-blue-600 text-white shadow'
                  : 'text-foreground/60 hover:bg-foreground/10 hover:text-foreground'
              }`}>
              {sec.label}
            </button>
          ))}
        </nav>
      </aside>

      {/* ── Main Content ── */}
      <main className="flex-1 lg:ml-64 p-6 lg:p-12 max-w-5xl">

        {/* Mobile Back Button */}
        <button onClick={() => router.back()} className="lg:hidden text-blue-400 hover:text-blue-300 mb-6 inline-flex items-center gap-1 text-sm font-semibold self-start">
          ← Back
        </button>

        {/* HERO */}
        <div className="mb-12">
          <motion.h1 initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}
            className="text-5xl md:text-6xl font-extrabold tracking-tight mb-4 text-transparent bg-clip-text bg-gradient-to-r from-blue-500 to-purple-600">
            {career.name || slug.split('-').map((w: string) => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')}
          </motion.h1>
          <p className="text-lg text-foreground/70 max-w-3xl leading-relaxed">{career.overview}</p>
        </div>

        {/* ── 1. OVERVIEW ── */}
        <section id="overview" className="mb-20 scroll-mt-24">
          <h2 className="text-3xl font-extrabold mb-8 pb-3 border-b border-foreground/10">📋 Career Overview</h2>
          <div className="grid md:grid-cols-2 gap-8">
            <div className="space-y-6">
              {responsibilities.length > 0 && (
                <div className="p-6 bg-foreground/5 rounded-2xl border border-foreground/10">
                  <h3 className="font-bold text-sm uppercase tracking-widest text-foreground/50 mb-3">Key Responsibilities</h3>
                  <ul className="space-y-2">
                    {responsibilities.map((r: string, i: number) => (
                      <li key={i} className="flex items-start gap-2 text-sm">
                        <span className="text-blue-400 mt-0.5">▸</span> {r}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
              {career.who_can_apply && (
                <div className="p-5 bg-blue-500/5 rounded-xl border border-blue-500/20">
                  <h3 className="font-bold text-sm text-blue-400 mb-2">Who Can Apply</h3>
                  <p className="text-sm text-foreground/70">{career.who_can_apply}</p>
                </div>
              )}
              {career.future_scope && (
                <div className="p-5 bg-purple-500/5 rounded-xl border border-purple-500/20">
                  <h3 className="font-bold text-sm text-purple-400 mb-2">Future Scope</h3>
                  <p className="text-sm text-foreground/70">{career.future_scope}</p>
                </div>
              )}
              {growthPath.length > 0 && (
                <div>
                  <h3 className="font-bold text-sm uppercase tracking-widest text-foreground/50 mb-3">Growth Path</h3>
                  <div className="flex flex-wrap gap-2">
                    {growthPath.map((g: string, i: number) => (
                      <React.Fragment key={g}>
                        <span className="px-3 py-1 bg-blue-500/10 text-blue-400 text-sm font-semibold rounded-full border border-blue-500/20">{g}</span>
                        {i < growthPath.length - 1 && <span className="text-foreground/30 self-center">→</span>}
                      </React.Fragment>
                    ))}
                  </div>
                </div>
              )}
            </div>

            <div className="grid grid-cols-2 gap-4">
              {[
                { label: 'Industry Demand',    val: career.industry_demand,      color: 'text-green-400',  bg: 'bg-green-500/5',  border: 'border-green-500/20', icon: '📈' },
                { label: 'Remote Work',        val: career.remote_opportunities,  color: 'text-sky-400',    bg: 'bg-sky-500/5',    border: 'border-sky-500/20',   icon: '🏠' },
                { label: 'India Salary',       val: career.india_salary,          color: 'text-emerald-400',bg: 'bg-emerald-500/5',border: 'border-emerald-500/20',icon: '💰' },
                { label: 'International',      val: career.international_salary,  color: 'text-yellow-400', bg: 'bg-yellow-500/5', border: 'border-yellow-500/20', icon: '🌍' },
              ].map(card => card.val ? (
                <div key={card.label} className={`p-5 ${card.bg} rounded-2xl border ${card.border}`}>
                  <div className="text-xl mb-1">{card.icon}</div>
                  <h4 className="text-xs font-bold text-foreground/50 uppercase tracking-wider mb-1">{card.label}</h4>
                  <p className={`font-bold text-sm ${card.color}`}>{card.val}</p>
                </div>
              ) : null)}
            </div>
          </div>
        </section>

        {/* ── 2. SKILLS MATRIX ── */}
        {Object.keys(skillsMatrix).length > 0 && (
          <section id="skills" className="mb-20 scroll-mt-24">
            <h2 className="text-3xl font-extrabold mb-8 pb-3 border-b border-foreground/10">🧠 Complete Skills Matrix</h2>
            <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
              {Object.entries(skillsMatrix).map(([cat, skills]: [string, any]) => (
                <motion.div key={cat} whileHover={{ y: -3 }}
                  className="p-6 bg-foreground/5 rounded-2xl border border-foreground/10">
                  <h3 className="font-bold text-purple-400 mb-4 text-sm uppercase tracking-wider">{cat}</h3>
                  <ul className="space-y-1.5">
                    {(Array.isArray(skills) ? skills : [skills]).map((s: string, i: number) => (
                      <li key={i} className="flex items-center gap-2 text-sm">
                        <span className="w-1.5 h-1.5 rounded-full bg-purple-500 flex-shrink-0" />
                        {s}
                      </li>
                    ))}
                  </ul>
                </motion.div>
              ))}
            </div>
          </section>
        )}

        {/* ── 3. LEARNING ROADMAP ── */}
        <section id="roadmap" className="mb-20 scroll-mt-24">
          <h2 className="text-3xl font-extrabold mb-8 pb-3 border-b border-foreground/10">🗺️ Learning Roadmap</h2>

          {/* Learning Plans */}
          {planList.length > 0 && (
            <div className="mb-10">
              <h3 className="text-xl font-bold mb-4">Choose Your Learning Pace</h3>
              <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
                {planList.map((plan: any, i: number) => (
                  <button key={i} onClick={() => setActivePlan(i)}
                    className={`p-5 rounded-2xl text-left transition-all border ${
                      activePlan === i
                        ? 'bg-blue-600 border-blue-500 text-white shadow-xl shadow-blue-500/20 scale-105'
                        : 'bg-foreground/5 border-foreground/10 hover:bg-foreground/10'
                    }`}>
                    <h4 className="font-bold mb-1">{plan.name}</h4>
                    <p className="text-sm opacity-80">{plan.duration}</p>
                    <p className="text-xs opacity-60">{plan.daily_hours}/day</p>
                  </button>
                ))}
              </div>
              {selectedPlan.name && (
                <div className="p-6 bg-blue-500/5 border border-blue-500/20 rounded-2xl">
                  <h4 className="font-bold text-blue-400 mb-1">{selectedPlan.name}</h4>
                  <p className="text-sm text-foreground/60">{selectedPlan.duration} • {selectedPlan.daily_hours} per day</p>
                </div>
              )}
            </div>
          )}

          {/* Learning Steps / Phases */}
          {learningSteps.length > 0 && (
            <div>
              <h3 className="text-xl font-bold mb-6">Phase-by-Phase Roadmap</h3>
              <div className="relative border-l-4 border-purple-500/30 ml-4 pl-8 space-y-8">
                {learningSteps.map((rawStep: any, i: number) => {
                  const step = getScaledStep(rawStep, i, totalTargetMonths);
                  return (
                  <motion.div key={i} initial={{ opacity: 0, x: -20 }} whileInView={{ opacity: 1, x: 0 }}
                    viewport={{ once: true }} transition={{ delay: i * 0.05 }} className="relative">
                    <div className="absolute -left-[49px] top-1 w-8 h-8 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-white text-[10px] leading-tight font-bold shadow-lg">
                      {step.phase}
                    </div>
                    <div className="p-6 bg-foreground/5 rounded-2xl border border-foreground/10 hover:border-purple-500/30 transition-colors">
                      <div className="flex items-center justify-between mb-3">
                        <h4 className="text-lg font-bold">{step.title}</h4>
                        <span className="px-3 py-1 bg-purple-500/10 text-purple-400 text-xs font-bold rounded-full border border-purple-500/20">
                          {step.duration}
                        </span>
                      </div>
                      {step.learn && (
                        <div className="flex flex-wrap gap-2">
                          {(Array.isArray(step.learn) ? step.learn : [step.learn]).map((topic: string, j: number) => (
                            <span key={j} className="px-3 py-1 bg-background rounded-lg text-xs font-semibold border border-foreground/10">
                              {topic}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>
                  </motion.div>
                ); })}
              </div>
            </div>
          )}
        </section>

        {/* ── 4. PROJECTS ── */}
        {Object.keys(projects).length > 0 && (
          <section id="projects" className="mb-20 scroll-mt-24">
            <h2 className="text-3xl font-extrabold mb-8 pb-3 border-b border-foreground/10">💼 Project Portfolio</h2>
            <div className="space-y-8">
              {Object.entries(projects).map(([level, list]: [string, any]) => {
                const items = Array.isArray(list) ? list : [list];
                if (!items.length) return null;
                const colors: Record<string, string> = {
                  Beginner: 'text-green-400 border-green-500/20 bg-green-500/5',
                  Intermediate: 'text-blue-400 border-blue-500/20 bg-blue-500/5',
                  Advanced: 'text-purple-400 border-purple-500/20 bg-purple-500/5',
                  'Industry-Level': 'text-orange-400 border-orange-500/20 bg-orange-500/5',
                };
                const cls = colors[level] || 'text-foreground/70 border-foreground/10 bg-foreground/5';
                return (
                  <div key={level}>
                    <h3 className={`inline-block text-sm font-bold uppercase tracking-widest px-4 py-1.5 rounded-full border mb-4 ${cls}`}>
                      {level} Projects
                    </h3>
                    <div className="grid md:grid-cols-2 gap-4">
                      {items.map((p: any, i: number) => (
                        <motion.div key={i} whileHover={{ y: -3 }}
                          className="p-6 bg-foreground/5 rounded-2xl border border-foreground/10 hover:border-blue-500/30 transition-all">
                          {typeof p === 'string' ? (
                            <p className="font-semibold">{p}</p>
                          ) : (
                            <>
                              <h4 className="text-lg font-bold mb-2">{p.name}</h4>
                              {p.objective && <p className="text-sm text-foreground/60 mb-3">{p.objective}</p>}
                              {p.skills && (
                                <div className="flex flex-wrap gap-1.5 mb-2">
                                  {(Array.isArray(p.skills) ? p.skills : [p.skills]).map((s: string, j: number) => (
                                    <span key={j} className="px-2 py-0.5 bg-background text-xs rounded border border-foreground/10">{s}</span>
                                  ))}
                                </div>
                              )}
                              {(p.duration || p.tech) && (
                                <p className="text-xs font-semibold text-blue-400">
                                  {p.duration && `⏱ ${p.duration}`}{p.duration && p.tech && ' • '}{p.tech && `🛠 ${p.tech}`}
                                </p>
                              )}
                            </>
                          )}
                        </motion.div>
                      ))}
                    </div>
                  </div>
                );
              })}
            </div>
          </section>
        )}

        {/* ── 5. CERTIFICATIONS ── */}
        {certifications.length > 0 && (
          <section id="certs" className="mb-20 scroll-mt-24">
            <h2 className="text-3xl font-extrabold mb-8 pb-3 border-b border-foreground/10">🏅 Recommended Certifications</h2>
            <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {certifications.map((cert: string, i: number) => (
                <motion.div key={i} whileHover={{ scale: 1.02 }}
                  className="p-5 bg-gradient-to-br from-yellow-500/10 to-orange-500/5 border border-yellow-500/20 rounded-xl flex items-start gap-3">
                  <span className="text-2xl">🎓</span>
                  <p className="font-semibold text-sm leading-snug">{cert}</p>
                </motion.div>
              ))}
            </div>
          </section>
        )}

        {/* ── 6. INTERVIEW PREP ── */}
        {Object.keys(interviewPrep).length > 0 && (
          <section id="interview" className="mb-20 scroll-mt-24">
            <h2 className="text-3xl font-extrabold mb-8 pb-3 border-b border-foreground/10">🎯 Interview Preparation</h2>
            <div className="grid md:grid-cols-2 gap-6">
              {Object.entries(interviewPrep).map(([cat, qs]: [string, any]) => {
                const items = Array.isArray(qs) ? qs : [qs];
                return (
                  <div key={cat} className="p-6 bg-foreground/5 rounded-2xl border border-foreground/10">
                    <h3 className="font-bold text-lg mb-4 capitalize text-blue-400">{cat}</h3>
                    <ul className="space-y-3">
                      {items.map((q: string, i: number) => (
                        <li key={i} className="flex items-start gap-2 text-sm">
                          <span className="text-blue-400 font-bold mt-0.5">Q{i + 1}.</span>
                          <span className="text-foreground/80">{q}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                );
              })}
            </div>

            {/* Practice Questions */}
            {Object.keys(practiceQs).length > 0 && (
              <div className="mt-8">
                <h3 className="text-xl font-bold mb-4">Practice Problems by Topic</h3>
                <div className="grid sm:grid-cols-2 gap-4">
                  {Object.entries(practiceQs).map(([topic, qs]: [string, any]) => {
                    const items = Array.isArray(qs) ? qs : [qs];
                    return (
                      <div key={topic} className="p-5 bg-foreground/5 rounded-xl border border-foreground/10">
                        <h4 className="font-bold text-sm text-purple-400 mb-2">{topic}</h4>
                        <ul className="space-y-1">
                          {items.map((q: string, i: number) => <li key={i} className="text-xs text-foreground/70">• {q}</li>)}
                        </ul>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}
          </section>
        )}

        {/* ── 7. READINESS CHECKLIST ── */}
        {readinessChecklist.length > 0 && (
          <section id="checklist" className="mb-20 scroll-mt-24">
            <h2 className="text-3xl font-extrabold mb-8 pb-3 border-b border-foreground/10">✅ Job Readiness Checklist</h2>
            <div className="bg-foreground/5 rounded-2xl border border-foreground/10 p-8">
              <div className="grid sm:grid-cols-2 gap-3">
                {readinessChecklist.map((item: string, i: number) => (
                  <div key={i} className="flex items-start gap-3 p-3 bg-background rounded-xl border border-foreground/8 hover:border-green-500/30 transition-colors">
                    <span className="text-green-400 text-lg flex-shrink-0">☐</span>
                    <span className="text-sm font-medium">{item}</span>
                  </div>
                ))}
              </div>
              <div className="mt-8 p-5 bg-gradient-to-r from-green-600/20 to-emerald-600/20 rounded-xl border border-green-500/30 text-center">
                <p className="text-green-400 font-bold text-lg">🚀 Complete all items above to be job-ready!</p>
                <p className="text-foreground/60 text-sm mt-1">Save this checklist and track your progress daily.</p>
              </div>
            </div>
          </section>
        )}

      </main>
    </div>
  );
}
