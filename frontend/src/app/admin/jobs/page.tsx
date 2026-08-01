'use client';
import React, { useEffect, useState } from 'react';

export default function AdminJobsManager() {
  const [jobs, setJobs] = useState<any[]>([]);

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_URL || ''}/api/jobs/`)
      .then(res => res.json())
      .then(data => setJobs(Array.isArray(data) ? data : []))
      .catch(console.error);
  }, []);

  const handleApprove = (id: string) => {
    alert(`Approved job ${id}`);
  };

  const handleReject = (id: string) => {
    alert(`Rejected job ${id}`);
  };

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Jobs & Internships Management</h1>
      <p className="text-foreground/60 mb-8">Review, approve, or reject job postings submitted by recruiters.</p>
      
      <div className="grid grid-cols-1 gap-4">
        {jobs.map(job => (
          <div key={job.job_id} className="p-6 rounded-xl border border-foreground/10 bg-foreground/5 flex justify-between items-center">
            <div>
              <h3 className="font-bold text-lg">{job.title}</h3>
              <p className="text-sm text-foreground/50">{job.company} • {job.location}</p>
            </div>
            <div className="flex gap-2">
              <button onClick={() => handleApprove(job.job_id)} className="px-4 py-2 bg-green-500/10 text-green-600 rounded font-semibold text-sm hover:bg-green-500/20">Approve</button>
              <button onClick={() => handleReject(job.job_id)} className="px-4 py-2 bg-red-500/10 text-red-600 rounded font-semibold text-sm hover:bg-red-500/20">Reject</button>
            </div>
          </div>
        ))}
        {jobs.length === 0 && (
          <div className="p-8 text-center text-foreground/50 border border-foreground/10 rounded-xl bg-foreground/5">
            No job postings available.
          </div>
        )}
      </div>
    </div>
  );
}
