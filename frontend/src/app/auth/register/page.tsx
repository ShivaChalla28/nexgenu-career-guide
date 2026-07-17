'use client';
import React, { useState } from 'react';
import { motion } from 'framer-motion';
import Link from 'next/link';
import { useRouter } from 'next/navigation';

const BRANCHES = [
  'Computer Science Engineering (CSE)',
  'Information Technology (IT)',
  'Artificial Intelligence & Data Science',
  'Electronics & Communication Engineering (ECE)',
  'Electrical & Electronics Engineering (EEE)',
  'Mechanical Engineering',
  'Civil Engineering',
  'Chemical Engineering',
  'Automobile Engineering',
  'Biomedical Engineering',
  'Mechatronics Engineering',
  'Instrumentation Engineering',
  'Aeronautical Engineering',
  'Agricultural Engineering',
  'Marine Engineering',
  'Mining Engineering',
  'Industrial Engineering',
  'Production Engineering',
  'Metallurgical Engineering',
  'Petroleum Engineering',
  'Textile Engineering',
  'Biotechnology Engineering',
  'Food Technology',
  'Environmental Engineering',
];

const STATES = [
  'Andhra Pradesh','Arunachal Pradesh','Assam','Bihar','Chhattisgarh',
  'Goa','Gujarat','Haryana','Himachal Pradesh','Jharkhand','Karnataka',
  'Kerala','Madhya Pradesh','Maharashtra','Manipur','Meghalaya','Mizoram',
  'Nagaland','Odisha','Punjab','Rajasthan','Sikkim','Tamil Nadu','Telangana',
  'Tripura','Uttar Pradesh','Uttarakhand','West Bengal',
  'Andaman & Nicobar Islands','Chandigarh','Dadra & Nagar Haveli',
  'Daman & Diu','Delhi','Jammu & Kashmir','Ladakh','Lakshadweep','Puducherry',
];

const YEARS = Array.from({ length: 8 }, (_, i) => String(2024 + i));

interface FormData {
  fullName: string;
  email: string;
  mobile: string;
  branch: string;
  college: string;
  year: string;
  state: string;
  password: string;
  confirmPassword: string;
}

function Field({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div className="space-y-1.5">
      <label className="text-sm font-semibold text-foreground/70">{label}</label>
      {children}
    </div>
  );
}

const inputCls =
  'w-full px-4 py-3 rounded-xl bg-foreground/5 border border-foreground/10 focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 transition text-sm placeholder:text-foreground/30';

export default function Register() {
  const router = useRouter();
  const [formData, setFormData] = useState<FormData>({
    fullName: '', email: '', mobile: '', branch: '',
    college: '', year: '', state: '', password: '', confirmPassword: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false);

  const set = (field: keyof FormData) => (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    setFormData({ ...formData, [field]: e.target.value });
    setError('');
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match.');
      return;
    }
    if (formData.password.length < 6) {
      setError('Password must be at least 6 characters.');
      return;
    }
    if (!formData.branch) {
      setError('Please select your engineering branch.');
      return;
    }

    setLoading(true);
    try {
      const res = await fetch('http://localhost:8000/api/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          full_name: formData.fullName,
          email: formData.email,
          mobile_number: formData.mobile,
          branch: formData.branch,
          college_name: formData.college,
          graduation_year: formData.year,
          state: formData.state,
          password: formData.password,
        }),
      });

      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || 'Registration failed. Please try again.');
      }

      setSuccess(true);
      setTimeout(() => router.push('/auth/login'), 2500);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : 'Something went wrong. Please try again.';
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="flex min-h-screen items-center justify-center pt-28 pb-16 px-6">
      <div className="absolute inset-0 -z-10 h-full w-full bg-background bg-[radial-gradient(#e5e7eb_1px,transparent_1px)] dark:bg-[radial-gradient(#1f2937_1px,transparent_1px)] opacity-30" />
      <div className="absolute top-1/3 left-1/2 -translate-x-1/2 w-[700px] h-[500px] rounded-full bg-blue-600/8 blur-[130px] pointer-events-none" />

      <motion.div
        initial={{ opacity: 0, y: 24 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="w-full max-w-2xl"
      >
        <div className="bg-background/60 backdrop-blur-xl border border-foreground/10 rounded-3xl p-8 md:p-10 shadow-2xl">
          {/* Header */}
          <div className="text-center mb-8">
            <Link href="/" className="inline-block mb-4">
              <span className="text-2xl font-extrabold bg-clip-text text-transparent bg-gradient-to-r from-blue-500 to-purple-600">
                NexGenU
              </span>
            </Link>
            <h1 className="text-3xl font-extrabold mb-1">Create your account</h1>
            <p className="text-foreground/55 text-sm">Free forever • No credit card required</p>
          </div>

          {/* Alerts */}
          {error && (
            <motion.div initial={{ opacity: 0, y: -8 }} animate={{ opacity: 1, y: 0 }}
              className="mb-5 p-4 bg-red-500/10 border border-red-500/30 text-red-400 rounded-xl text-sm text-center">
              ⚠️ {error}
            </motion.div>
          )}
          {success && (
            <motion.div initial={{ opacity: 0, y: -8 }} animate={{ opacity: 1, y: 0 }}
              className="mb-5 p-4 bg-green-500/10 border border-green-500/30 text-green-400 rounded-xl text-sm text-center">
              🎉 Account created! Redirecting to login...
            </motion.div>
          )}

          <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-2 gap-5">
            {/* Full Name */}
            <Field label="Full Name">
              <input id="fullName" type="text" placeholder="Rahul Kumar" required
                value={formData.fullName} onChange={set('fullName')} className={inputCls} />
            </Field>

            {/* Email */}
            <Field label="Email Address">
              <input id="email" type="email" placeholder="rahul@example.com" required
                value={formData.email} onChange={set('email')} className={inputCls} />
            </Field>

            {/* Mobile */}
            <Field label="Mobile Number">
              <input id="mobile" type="tel" placeholder="+91 98765 43210" required
                value={formData.mobile} onChange={set('mobile')} className={inputCls}
                pattern="[0-9+\s\-()]{7,15}" />
            </Field>

            {/* Branch */}
            <Field label="Engineering Branch">
              <select id="branch" required value={formData.branch} onChange={set('branch')}
                className={inputCls + ' appearance-none cursor-pointer'}>
                <option value="" disabled>Select your branch</option>
                {BRANCHES.map((b) => (
                  <option key={b} value={b}>{b}</option>
                ))}
              </select>
            </Field>

            {/* College */}
            <Field label="College / University Name">
              <input id="college" type="text" placeholder="ABC Institute of Technology" required
                value={formData.college} onChange={set('college')} className={inputCls} />
            </Field>

            {/* Graduation Year */}
            <Field label="Expected Graduation Year">
              <input id="year" type="number" placeholder="e.g. 2026" required
                value={formData.year} onChange={set('year')} className={inputCls}
                min="2020" max="2035" />
            </Field>

            {/* State */}
            <Field label="State / UT">
              <select id="state" required value={formData.state} onChange={set('state')}
                className={inputCls + ' appearance-none cursor-pointer md:col-span-1'}>
                <option value="" disabled>Select your state</option>
                {STATES.map((s) => (
                  <option key={s} value={s}>{s}</option>
                ))}
              </select>
            </Field>

            {/* Password */}
            <Field label="Password">
              <div className="relative">
                <input id="password" name="password" type={showPassword ? 'text' : 'password'}
                  placeholder="Min. 6 characters" required
                  value={formData.password} onChange={set('password')}
                  className={inputCls + ' pr-12'} />
                <button type="button" onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-4 top-1/2 -translate-y-1/2 text-foreground/40 hover:text-foreground/70 transition">
                  {showPassword
                    ? <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" /></svg>
                    : <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" /></svg>
                  }
                </button>
              </div>
            </Field>

            {/* Confirm Password */}
            <Field label="Confirm Password">
              <div className="relative">
                <input id="confirmPassword" name="confirmPassword"
                  type={showConfirm ? 'text' : 'password'}
                  placeholder="Re-enter password" required
                  value={formData.confirmPassword} onChange={set('confirmPassword')}
                  className={inputCls + ' pr-12'} />
                <button type="button" onClick={() => setShowConfirm(!showConfirm)}
                  className="absolute right-4 top-1/2 -translate-y-1/2 text-foreground/40 hover:text-foreground/70 transition">
                  {showConfirm
                    ? <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" /></svg>
                    : <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" /></svg>
                  }
                </button>
              </div>
            </Field>

            {/* Submit */}
            <div className="md:col-span-2 pt-2">
              <button
                id="register-submit"
                type="submit"
                disabled={loading || success}
                className="w-full py-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white font-bold rounded-xl text-base hover:opacity-90 transition shadow-lg shadow-blue-500/25 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
              >
                {loading ? (
                  <>
                    <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                    Creating Account...
                  </>
                ) : success ? (
                  '✅ Account Created!'
                ) : (
                  'Create My Free Account →'
                )}
              </button>

              <p className="mt-4 text-center text-xs text-foreground/40">
                By registering, you agree to our{' '}
                <a href="/privacy" className="underline hover:text-foreground/70">Privacy Policy</a>.
                Your data is safe with us.
              </p>
            </div>
          </form>

          <p className="mt-6 text-center text-sm text-foreground/55">
            Already have an account?{' '}
            <Link href="/auth/login" className="text-blue-400 hover:text-blue-300 font-semibold transition">
              Sign in here
            </Link>
          </p>
        </div>
      </motion.div>
    </main>
  );
}
