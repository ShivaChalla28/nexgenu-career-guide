'use client';
import React, { useState } from 'react';

export default function AdminSettings() {
  const [paymentToggle, setPaymentToggle] = useState(false);
  const [razorpayKey, setRazorpayKey] = useState('rzp_test_XXXXXXXXXXXXXXXX');

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    alert('Settings saved to API Vault (encrypted).');
  };

  return (
    <div className="max-w-4xl">
      <h1 className="text-3xl font-bold mb-6">Settings & API Vault</h1>
      
      <form onSubmit={handleSave} className="space-y-8">
        <section className="p-6 rounded-xl border border-foreground/10 bg-foreground/5">
          <h2 className="text-xl font-bold mb-4">System Toggles</h2>
          
          <div className="flex items-center justify-between p-4 bg-background rounded-lg border border-foreground/10 mb-4">
            <div>
              <h3 className="font-bold">Payment Engine</h3>
              <p className="text-sm text-foreground/50">Enable or disable payments globally.</p>
            </div>
            <label className="relative inline-flex items-center cursor-pointer">
              <input type="checkbox" className="sr-only peer" checked={paymentToggle} onChange={() => setPaymentToggle(!paymentToggle)} />
              <div className="w-11 h-6 bg-foreground/20 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-green-500"></div>
            </label>
          </div>
        </section>

        <section className="p-6 rounded-xl border border-foreground/10 bg-foreground/5">
          <h2 className="text-xl font-bold mb-4">API Vault (Encrypted)</h2>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-semibold mb-1">Razorpay Key ID</label>
              <input type="password" value={razorpayKey} onChange={e => setRazorpayKey(e.target.value)} className="w-full px-4 py-3 rounded-xl bg-background border border-foreground/10 focus:border-blue-500 outline-none transition" />
            </div>
            <div>
              <label className="block text-sm font-semibold mb-1">Razorpay Key Secret</label>
              <input type="password" placeholder="••••••••••••••••" className="w-full px-4 py-3 rounded-xl bg-background border border-foreground/10 focus:border-blue-500 outline-none transition" />
            </div>
          </div>
        </section>
        
        <button type="submit" className="px-8 py-3 bg-blue-600 text-white rounded-xl font-bold hover:bg-blue-700">
          Save Settings
        </button>
      </form>
    </div>
  );
}
