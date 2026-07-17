'use client';
import React, { useState } from 'react';

const BASE_URL = 'https://engineeeringroadmaps.nexgenu.dpdns.org';

const PAGES = [
  {
    page: 'Homepage',
    url: '/',
    title: 'NexGenU | Engineering Career Roadmaps Platform',
    description: "NexGenU is India's largest engineering career roadmap platform. Explore 300+ career paths across 24 engineering branches with AI-generated roadmaps.",
    canonical: BASE_URL,
    robots: 'index, follow',
    ogImage: `${BASE_URL}/og-image.png`,
  },
  {
    page: 'Dashboard',
    url: '/dashboard',
    title: 'My Dashboard | NexGenU',
    description: 'Your personalized NexGenU dashboard to explore engineering branch career paths.',
    canonical: `${BASE_URL}/dashboard`,
    robots: 'noindex, nofollow',
    ogImage: `${BASE_URL}/og-image.png`,
  },
  {
    page: 'Login',
    url: '/auth/login',
    title: 'Login | NexGenU',
    description: 'Login to NexGenU to access your personalized engineering career dashboard.',
    canonical: `${BASE_URL}/auth/login`,
    robots: 'noindex, nofollow',
    ogImage: `${BASE_URL}/og-image.png`,
  },
  {
    page: 'Register',
    url: '/auth/register',
    title: 'Create Account | NexGenU',
    description: 'Create a free NexGenU account and get access to 300+ engineering career roadmaps.',
    canonical: `${BASE_URL}/auth/register`,
    robots: 'noindex, nofollow',
    ogImage: `${BASE_URL}/og-image.png`,
  },
];

const BRANCH_PAGES = [
  { branch: 'Computer Science Engineering', slug: 'computer-science-engineering' },
  { branch: 'Information Technology', slug: 'information-technology' },
  { branch: 'AI & Data Science', slug: 'artificial-intelligence-and-data-science' },
  { branch: 'Electronics & Communication', slug: 'electronics-and-communication-engineering' },
  { branch: 'Electrical & Electronics', slug: 'electrical-and-electronics-engineering' },
  { branch: 'Mechanical Engineering', slug: 'mechanical-engineering' },
  { branch: 'Civil Engineering', slug: 'civil-engineering' },
  { branch: 'Chemical Engineering', slug: 'chemical-engineering' },
];

const ROBOTS_CONTENT = `User-agent: *
Allow: /
Allow: /branches/
Allow: /careers/
Disallow: /admin
Disallow: /dashboard
Disallow: /auth/login
Disallow: /auth/register
Sitemap: ${BASE_URL}/sitemap.xml`;

export default function SEOManager() {
  const [activeTab, setActiveTab] = useState<'pages' | 'branches' | 'robots' | 'preview'>('pages');
  const [previewUrl, setPreviewUrl] = useState(`${BASE_URL}`);
  const [copied, setCopied] = useState(false);

  const handleCopy = (text: string) => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const badgeCls = (robots: string) =>
    robots.includes('noindex')
      ? 'bg-red-500/10 text-red-400 border border-red-500/20'
      : 'bg-green-500/10 text-green-400 border border-green-500/20';

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-3xl font-bold">🔍 SEO Manager</h1>
          <p className="text-foreground/50 text-sm mt-1">Monitor and review SEO settings for all pages</p>
        </div>
        <div className="flex gap-2">
          <a
            href={`${BASE_URL}/sitemap.xml`}
            target="_blank"
            rel="noopener noreferrer"
            className="px-4 py-2 bg-blue-500/10 text-blue-400 border border-blue-500/20 rounded-lg text-sm font-semibold hover:bg-blue-500/20 transition"
          >
            🗺️ View Sitemap
          </a>
          <a
            href={`${BASE_URL}/robots.txt`}
            target="_blank"
            rel="noopener noreferrer"
            className="px-4 py-2 bg-purple-500/10 text-purple-400 border border-purple-500/20 rounded-lg text-sm font-semibold hover:bg-purple-500/20 transition"
          >
            🤖 View Robots.txt
          </a>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex gap-2 mb-6 border-b border-foreground/10 pb-3">
        {[
          { id: 'pages', label: '📄 Pages' },
          { id: 'branches', label: '🏢 Branches' },
          { id: 'robots', label: '🤖 Robots.txt' },
          { id: 'preview', label: '👁️ OG Preview' },
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id as typeof activeTab)}
            className={`px-4 py-2 rounded-lg text-sm font-semibold transition ${
              activeTab === tab.id
                ? 'bg-blue-600 text-white'
                : 'text-foreground/60 hover:bg-foreground/10'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Pages Tab */}
      {activeTab === 'pages' && (
        <div className="bg-foreground/5 rounded-xl border border-foreground/10 overflow-hidden">
          <table className="w-full text-left">
            <thead className="bg-foreground/10 border-b border-foreground/10">
              <tr>
                <th className="p-4 text-sm font-semibold">Page</th>
                <th className="p-4 text-sm font-semibold">Title</th>
                <th className="p-4 text-sm font-semibold">Description</th>
                <th className="p-4 text-sm font-semibold">Robots</th>
                <th className="p-4 text-sm font-semibold">Canonical</th>
              </tr>
            </thead>
            <tbody>
              {PAGES.map((p) => (
                <tr key={p.page} className="border-b border-foreground/10 last:border-0 hover:bg-foreground/5">
                  <td className="p-4 font-semibold text-sm">{p.page}<div className="text-xs text-foreground/40 font-normal">{p.url}</div></td>
                  <td className="p-4 text-sm max-w-[220px]"><div className="truncate" title={p.title}>{p.title}</div><div className="text-xs text-foreground/40 mt-0.5">{p.title.length} chars</div></td>
                  <td className="p-4 text-sm max-w-[260px]"><div className="line-clamp-2 text-foreground/70" title={p.description}>{p.description}</div><div className="text-xs text-foreground/40 mt-0.5">{p.description.length} chars</div></td>
                  <td className="p-4"><span className={`px-2 py-1 rounded text-xs font-bold ${badgeCls(p.robots)}`}>{p.robots}</span></td>
                  <td className="p-4 text-xs text-blue-400"><a href={p.canonical} target="_blank" rel="noopener noreferrer" className="hover:underline truncate block max-w-[180px]">{p.canonical}</a></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Branches Tab */}
      {activeTab === 'branches' && (
        <div className="bg-foreground/5 rounded-xl border border-foreground/10 overflow-hidden">
          <table className="w-full text-left">
            <thead className="bg-foreground/10 border-b border-foreground/10">
              <tr>
                <th className="p-4 text-sm font-semibold">Branch</th>
                <th className="p-4 text-sm font-semibold">Generated Title</th>
                <th className="p-4 text-sm font-semibold">URL</th>
                <th className="p-4 text-sm font-semibold">Indexed</th>
              </tr>
            </thead>
            <tbody>
              {BRANCH_PAGES.map((b) => (
                <tr key={b.slug} className="border-b border-foreground/10 last:border-0 hover:bg-foreground/5">
                  <td className="p-4 font-semibold text-sm">{b.branch}</td>
                  <td className="p-4 text-sm text-foreground/70">{b.branch} Career Roadmaps | NexGenU</td>
                  <td className="p-4"><a href={`${BASE_URL}/branches/${b.slug}`} target="_blank" rel="noopener noreferrer" className="text-xs text-blue-400 hover:underline">/branches/{b.slug}</a></td>
                  <td className="p-4"><span className="px-2 py-1 rounded text-xs font-bold bg-green-500/10 text-green-400 border border-green-500/20">index, follow</span></td>
                </tr>
              ))}
              <tr className="border-b border-foreground/10">
                <td colSpan={4} className="p-4 text-center text-sm text-foreground/40">
                  + 16 more branches — all auto-generated dynamically from their slugs
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      )}

      {/* Robots.txt Tab */}
      {activeTab === 'robots' && (
        <div>
          <div className="flex justify-between items-center mb-3">
            <h2 className="font-bold text-lg">robots.txt Content</h2>
            <button
              onClick={() => handleCopy(ROBOTS_CONTENT)}
              className="px-4 py-2 bg-foreground/10 hover:bg-foreground/20 rounded-lg text-sm font-semibold transition"
            >
              {copied ? '✅ Copied!' : '📋 Copy'}
            </button>
          </div>
          <pre className="p-6 bg-foreground/5 rounded-xl border border-foreground/10 text-sm font-mono text-foreground/80 whitespace-pre-wrap leading-relaxed">
            {ROBOTS_CONTENT}
          </pre>
          <div className="mt-4 p-4 bg-blue-500/5 border border-blue-500/20 rounded-xl text-sm text-blue-300">
            ℹ️ robots.txt is served at <a href={`${BASE_URL}/robots.txt`} target="_blank" rel="noopener noreferrer" className="underline">{BASE_URL}/robots.txt</a>. 
            Submit it to <a href="https://search.google.com/search-console" target="_blank" rel="noopener noreferrer" className="underline">Google Search Console</a> for faster indexing.
          </div>
        </div>
      )}

      {/* OG Preview Tab */}
      {activeTab === 'preview' && (
        <div>
          <h2 className="font-bold text-lg mb-4">Social Sharing Preview</h2>
          <div className="mb-4">
            <label className="block text-sm font-semibold mb-2">Preview URL</label>
            <div className="flex gap-2">
              <input
                value={previewUrl}
                onChange={(e) => setPreviewUrl(e.target.value)}
                className="flex-1 p-3 rounded-xl bg-foreground/5 border border-foreground/10 focus:outline-none focus:border-blue-500 text-sm"
                placeholder="Enter page URL to preview..."
              />
            </div>
          </div>

          {/* LinkedIn / Facebook Style Preview */}
          <div className="mb-6">
            <p className="text-xs font-bold uppercase tracking-widest text-foreground/40 mb-3">LinkedIn / Facebook</p>
            <div className="max-w-lg border border-foreground/20 rounded-xl overflow-hidden bg-foreground/5">
              <img src={`${BASE_URL}/og-image.png`} alt="OG Preview" className="w-full h-52 object-cover" />
              <div className="p-4">
                <div className="text-xs text-foreground/40 uppercase mb-1">{new URL(previewUrl).hostname}</div>
                <div className="font-bold text-base mb-1">NexGenU | Engineering Career Roadmaps Platform</div>
                <div className="text-sm text-foreground/60 line-clamp-2">Explore 300+ engineering career roadmaps with skills matrix, learning plans, projects, certifications, and interview prep — all free on NexGenU.</div>
              </div>
            </div>
          </div>

          {/* Twitter/X Style Preview */}
          <div>
            <p className="text-xs font-bold uppercase tracking-widest text-foreground/40 mb-3">Twitter / X</p>
            <div className="max-w-lg border border-foreground/20 rounded-xl overflow-hidden bg-foreground/5">
              <img src={`${BASE_URL}/og-image.png`} alt="Twitter OG Preview" className="w-full h-52 object-cover" />
              <div className="p-3">
                <div className="font-bold text-sm">NexGenU | Engineering Career Roadmaps Platform</div>
                <div className="text-xs text-foreground/50 mt-0.5">{new URL(previewUrl).hostname}</div>
              </div>
            </div>
          </div>

          <div className="mt-6 p-4 bg-green-500/5 border border-green-500/20 rounded-xl text-sm text-green-300">
            ✅ OG Image is live at: <a href={`${BASE_URL}/og-image.png`} target="_blank" rel="noopener noreferrer" className="underline">{BASE_URL}/og-image.png</a>
          </div>
        </div>
      )}

      {/* SEO Checklist */}
      <div className="mt-8 grid md:grid-cols-2 gap-4">
        <div className="p-5 bg-foreground/5 rounded-xl border border-foreground/10">
          <h3 className="font-bold mb-4 text-base">✅ SEO Checklist</h3>
          <div className="space-y-2 text-sm">
            {[
              'robots.txt configured',
              'sitemap.xml auto-generated',
              'Global meta title & description',
              'Open Graph tags on all pages',
              'Twitter Card tags on all pages',
              'Canonical URLs set',
              'Organization JSON-LD schema',
              'WebSite + SearchAction schema',
              'Course schema on career pages',
              'BreadcrumbList schema on career pages',
              '404 custom page created',
              'noindex on admin/auth/dashboard',
              'Security headers configured',
              'Image optimization enabled',
              'GZIP/Brotli compression enabled',
            ].map((item) => (
              <div key={item} className="flex items-center gap-2">
                <span className="text-green-400 font-bold">✓</span>
                <span>{item}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="p-5 bg-foreground/5 rounded-xl border border-foreground/10">
          <h3 className="font-bold mb-4 text-base">🔗 Search Console Links</h3>
          <div className="space-y-3 text-sm">
            {[
              { label: 'Google Search Console', url: 'https://search.google.com/search-console' },
              { label: 'Bing Webmaster Tools', url: 'https://www.bing.com/webmasters' },
              { label: 'Test OG Tags (Facebook)', url: 'https://developers.facebook.com/tools/debug/' },
              { label: 'Test Twitter Card', url: 'https://cards-dev.twitter.com/validator' },
              { label: 'Schema Validator', url: 'https://validator.schema.org' },
              { label: 'Google Rich Results Test', url: 'https://search.google.com/test/rich-results' },
              { label: 'PageSpeed Insights', url: `https://pagespeed.web.dev/report?url=${encodeURIComponent(BASE_URL)}` },
            ].map((link) => (
              <a key={link.label} href={link.url} target="_blank" rel="noopener noreferrer"
                className="flex items-center justify-between px-3 py-2 bg-foreground/5 border border-foreground/10 rounded-lg hover:bg-foreground/10 transition">
                <span>{link.label}</span>
                <span className="text-blue-400">→</span>
              </a>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
