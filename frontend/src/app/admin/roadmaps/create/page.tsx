'use client';
import React, { useState } from 'react';

export default function CreateRoadmap() {
  const [activeTab, setActiveTab] = useState("overview");

  return (
    <div className="max-w-5xl">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Create Dynamic Roadmap</h1>
        <button className="bg-green-600 text-white px-6 py-2 rounded-lg font-bold shadow-lg hover:bg-green-700">Save Roadmap</button>
      </div>
      
      <p className="text-foreground/70 mb-8">This advanced editor allows you to construct massive career knowledge bases using JSON-structured modular data.</p>

      {/* Tabs */}
      <div className="flex gap-2 border-b border-foreground/10 mb-8 overflow-x-auto pb-2">
        {["Overview", "Skills Matrix", "Learning Plans", "Steps Timeline", "Projects", "Practice", "Interview Prep"].map(tab => {
          const key = tab.toLowerCase().replace(/ /g, '-');
          return (
            <button 
              key={key} onClick={() => setActiveTab(key)}
              className={`px-4 py-2 rounded-t-lg font-semibold whitespace-nowrap ${activeTab === key ? 'bg-foreground/10 border-b-2 border-blue-500' : 'hover:bg-foreground/5'}`}
            >
              {tab}
            </button>
          )
        })}
      </div>

      {/* Form Content */}
      <div className="bg-foreground/5 p-8 rounded-xl border border-foreground/10 min-h-[400px]">
        {activeTab === "overview" && (
          <div className="space-y-4">
            <h2 className="text-xl font-bold mb-4">Basic Information</h2>
            <input type="text" placeholder="Career Name (e.g., Full Stack Developer)" className="w-full p-3 rounded-lg bg-background border border-foreground/10" />
            <textarea placeholder="Career Overview..." rows={4} className="w-full p-3 rounded-lg bg-background border border-foreground/10"></textarea>
            <div className="grid grid-cols-2 gap-4">
              <input type="text" placeholder="India Salary (e.g. ₹6L - ₹25L)" className="w-full p-3 rounded-lg bg-background border border-foreground/10" />
              <input type="text" placeholder="Global Salary (e.g. $90k - $160k)" className="w-full p-3 rounded-lg bg-background border border-foreground/10" />
            </div>
          </div>
        )}
        
        {activeTab === "skills-matrix" && (
          <div className="space-y-4">
            <h2 className="text-xl font-bold mb-4">JSON Skills Matrix Editor</h2>
            <p className="text-sm text-foreground/70 mb-2">Use comma separated values.</p>
            <input type="text" placeholder="Programming Languages (e.g. Python, Java, JS)" className="w-full p-3 rounded-lg bg-background border border-foreground/10" />
            <input type="text" placeholder="Core Engineering Subjects" className="w-full p-3 rounded-lg bg-background border border-foreground/10" />
            <input type="text" placeholder="Soft Skills" className="w-full p-3 rounded-lg bg-background border border-foreground/10" />
            <input type="text" placeholder="Frameworks & Libraries" className="w-full p-3 rounded-lg bg-background border border-foreground/10" />
          </div>
        )}

        {activeTab === "learning-plans" && (
          <div className="space-y-4">
            <h2 className="text-xl font-bold mb-4">Define 4 Learning Plans</h2>
            {['Fast Track', 'Standard', 'Balanced', 'Flexible'].map(plan => (
              <div key={plan} className="flex gap-4 items-center bg-background p-4 rounded-lg border border-foreground/10">
                <span className="font-bold w-32">{plan}</span>
                <input type="number" placeholder="Daily Hours" className="p-2 rounded border border-foreground/10 bg-transparent w-32" />
                <input type="text" placeholder="Duration (e.g. 6 Months)" className="p-2 rounded border border-foreground/10 bg-transparent flex-1" />
              </div>
            ))}
          </div>
        )}
        
        {/* Placeholder for others */}
        {["steps-timeline", "projects", "practice", "interview-prep"].includes(activeTab) && (
          <div className="flex flex-col items-center justify-center h-64 opacity-50">
            <span className="text-4xl mb-4">🛠️</span>
            <p>Advanced JSON Builder for {activeTab.replace(/-/g, ' ')} loads here.</p>
          </div>
        )}
      </div>
    </div>
  );
}
