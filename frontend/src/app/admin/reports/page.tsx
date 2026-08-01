'use client';
import React from 'react';

export default function AdminReports() {
  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Platform Reports</h1>
        <button className="px-5 py-2 bg-foreground/10 text-foreground rounded-xl font-bold border border-foreground/20 hover:bg-foreground/20">
          ⬇️ Export CSV
        </button>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <div className="p-6 rounded-xl border border-foreground/10 bg-foreground/5">
          <h3 className="text-lg font-bold mb-2">Student Growth</h3>
          <div className="h-40 flex items-center justify-center bg-background rounded-lg border border-foreground/5">
            <span className="text-foreground/30 font-mono">[ Chart Placeholder ]</span>
          </div>
        </div>
        <div className="p-6 rounded-xl border border-foreground/10 bg-foreground/5">
          <h3 className="text-lg font-bold mb-2">Revenue</h3>
          <div className="h-40 flex items-center justify-center bg-background rounded-lg border border-foreground/5">
            <span className="text-foreground/30 font-mono">[ Chart Placeholder ]</span>
          </div>
        </div>
      </div>
    </div>
  );
}
