'use client';
import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';

export default function RecruiterDashboard() {
  const [activeTab, setActiveTab] = useState<'jobs' | 'internships' | 'applicants' | 'analytics'>('jobs');
  const [jobs, setJobs] = useState<any[]>([]);
  const [internships, setInternships] = useState<any[]>([]);

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_URL || ''}/api/jobs/`)
      .then(res => res.json())
      .then(data => setJobs(Array.isArray(data) ? data : []))
      .catch(console.error);

    fetch(`${process.env.NEXT_PUBLIC_API_URL || ''}/api/jobs/internships/all`)
      .then(res => res.json())
      .then(data => setInternships(Array.isArray(data) ? data : []))
      .catch(console.error);
  }, []);

  const handlePostJob = (e: React.FormEvent) => {
    e.preventDefault();
    alert("Job submitted for admin approval!");
  };

  return (
    <main className="flex min-h-screen flex-col pt-24 pb-20 px-6 max-w-7xl mx-auto w-full">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-4xl font-extrabold mb-2">Recruiter Dashboard</h1>
          <p className="text-foreground/60">Manage your job postings and applicants.</p>
        </div>
        <div className="flex gap-4">
          <button className="px-5 py-2 bg-blue-600 text-white font-bold rounded-xl shadow-lg shadow-blue-500/20">
            + Post Job
          </button>
          <button className="px-5 py-2 bg-purple-600 text-white font-bold rounded-xl shadow-lg shadow-purple-500/20">
            + Post Internship
          </button>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex gap-4 border-b border-foreground/10 mb-8 pb-4 overflow-x-auto">
        {['jobs', 'internships', 'applicants', 'analytics'].map(tab => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab as any)}
            className={`px-4 py-2 font-bold capitalize whitespace-nowrap transition-colors ${activeTab === tab ? 'text-blue-500 border-b-2 border-blue-500' : 'text-foreground/50 hover:text-foreground'}`}
          >
            {tab}
          </button>
        ))}
      </div>

      {activeTab === 'jobs' && (
        <section>
          <h2 className="text-2xl font-bold mb-4">Your Job Postings</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {jobs.map(job => (
              <div key={job.job_id} className="p-6 rounded-2xl bg-foreground/5 border border-foreground/10">
                <div className="flex justify-between">
                  <h3 className="font-bold">{job.title}</h3>
                  <span className="text-xs px-2 py-1 bg-blue-500/10 text-blue-500 rounded">{job.status || 'Active'}</span>
                </div>
                <p className="text-sm text-foreground/50 mt-2">Location: {job.location}</p>
                <div className="flex gap-2 mt-4">
                  <button className="flex-1 py-1.5 bg-foreground/10 hover:bg-foreground/20 rounded font-semibold text-sm transition">Edit</button>
                  <button className="flex-1 py-1.5 bg-red-500/10 text-red-500 hover:bg-red-500/20 rounded font-semibold text-sm transition">Delete</button>
                </div>
              </div>
            ))}
            {jobs.length === 0 && <p className="text-foreground/40">You have no active job postings.</p>}
          </div>
        </section>
      )}

      {activeTab === 'internships' && (
        <section>
          <h2 className="text-2xl font-bold mb-4">Your Internship Postings</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {internships.map(intern => (
              <div key={intern.internship_id} className="p-6 rounded-2xl bg-foreground/5 border border-foreground/10">
                <div className="flex justify-between">
                  <h3 className="font-bold">{intern.title}</h3>
                  <span className="text-xs px-2 py-1 bg-purple-500/10 text-purple-500 rounded">{intern.status || 'Active'}</span>
                </div>
                <p className="text-sm text-foreground/50 mt-2">Duration: {intern.duration}</p>
                <div className="flex gap-2 mt-4">
                  <button className="flex-1 py-1.5 bg-foreground/10 hover:bg-foreground/20 rounded font-semibold text-sm transition">Edit</button>
                  <button className="flex-1 py-1.5 bg-red-500/10 text-red-500 hover:bg-red-500/20 rounded font-semibold text-sm transition">Delete</button>
                </div>
              </div>
            ))}
            {internships.length === 0 && <p className="text-foreground/40">You have no active internship postings.</p>}
          </div>
        </section>
      )}

      {activeTab === 'applicants' && (
        <section>
          <h2 className="text-2xl font-bold mb-4">Recent Applicants</h2>
          <div className="p-8 rounded-2xl border border-dashed border-foreground/20 text-center">
            <p className="text-foreground/50">No applicants to review yet.</p>
          </div>
        </section>
      )}

      {activeTab === 'analytics' && (
        <section>
          <h2 className="text-2xl font-bold mb-4">Dashboard Analytics</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="p-6 rounded-2xl bg-blue-500/10 border border-blue-500/20">
              <h3 className="text-sm font-bold text-blue-500 mb-1">Total Views</h3>
              <p className="text-4xl font-extrabold text-blue-600 dark:text-blue-400">1,204</p>
            </div>
            <div className="p-6 rounded-2xl bg-green-500/10 border border-green-500/20">
              <h3 className="text-sm font-bold text-green-500 mb-1">Total Applicants</h3>
              <p className="text-4xl font-extrabold text-green-600 dark:text-green-400">86</p>
            </div>
            <div className="p-6 rounded-2xl bg-purple-500/10 border border-purple-500/20">
              <h3 className="text-sm font-bold text-purple-500 mb-1">Shortlisted</h3>
              <p className="text-4xl font-extrabold text-purple-600 dark:text-purple-400">12</p>
            </div>
          </div>
        </section>
      )}
    </main>
  );
}
