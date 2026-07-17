import type { Metadata } from 'next';
import Link from 'next/link';

export const metadata: Metadata = {
  title: '404 — Page Not Found',
  description: 'The page you are looking for could not be found. Go back to NexGenU to explore engineering career roadmaps.',
  robots: { index: false, follow: false },
};

export default function NotFound() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-background px-6 py-24 text-center">
      <div className="absolute inset-0 -z-10 bg-background bg-[radial-gradient(#e5e7eb_1px,transparent_1px)] dark:bg-[radial-gradient(#1f2937_1px,transparent_1px)] [background-size:16px_16px] opacity-20" />

      <h1 className="text-9xl font-black bg-clip-text text-transparent bg-gradient-to-r from-blue-500 to-purple-600 select-none">
        404
      </h1>
      <h2 className="text-3xl font-extrabold mt-4 mb-3">Page Not Found</h2>
      <p className="text-foreground/60 text-lg max-w-md mb-10">
        The page you&#39;re looking for doesn&#39;t exist or has been moved. Let&#39;s get you back on track!
      </p>

      <div className="flex flex-wrap gap-4 justify-center">
        <Link
          href="/"
          className="px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-full font-bold text-sm hover:opacity-90 transition shadow-lg"
        >
          🏠 Go to Homepage
        </Link>
        <Link
          href="/dashboard"
          className="px-6 py-3 bg-foreground/10 text-foreground rounded-full font-bold text-sm hover:bg-foreground/20 transition border border-foreground/10"
        >
          📊 Go to Dashboard
        </Link>
        <Link
          href="/auth/login"
          className="px-6 py-3 bg-foreground/10 text-foreground rounded-full font-bold text-sm hover:bg-foreground/20 transition border border-foreground/10"
        >
          🔐 Login
        </Link>
      </div>

      {/* Popular Branches */}
      <div className="mt-16 max-w-2xl w-full">
        <h3 className="text-sm font-bold uppercase tracking-widest text-foreground/40 mb-5">
          Popular Engineering Branches
        </h3>
        <div className="flex flex-wrap gap-2 justify-center">
          {[
            { label: 'Computer Science', slug: 'computer-science-engineering' },
            { label: 'Information Technology', slug: 'information-technology' },
            { label: 'AI & Data Science', slug: 'artificial-intelligence-and-data-science' },
            { label: 'ECE', slug: 'electronics-and-communication-engineering' },
            { label: 'Mechanical', slug: 'mechanical-engineering' },
            { label: 'Civil', slug: 'civil-engineering' },
            { label: 'EEE', slug: 'electrical-and-electronics-engineering' },
          ].map((b) => (
            <Link
              key={b.slug}
              href={`/branches/${b.slug}`}
              className="px-4 py-2 text-xs font-semibold bg-blue-500/10 text-blue-400 border border-blue-500/20 rounded-full hover:bg-blue-500/20 transition"
            >
              {b.label}
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}
