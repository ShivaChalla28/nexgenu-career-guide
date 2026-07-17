import type { MetadataRoute } from 'next';

const BASE_URL = 'https://engineeeringroadmaps.nexgenu.dpdns.org';

const BRANCH_SLUGS = [
  { slug: 'computer-science-engineering', name: 'Computer Science Engineering' },
  { slug: 'information-technology', name: 'Information Technology' },
  { slug: 'artificial-intelligence-and-data-science', name: 'Artificial Intelligence & Data Science' },
  { slug: 'electronics-and-communication-engineering', name: 'Electronics & Communication Engineering' },
  { slug: 'electrical-and-electronics-engineering', name: 'Electrical & Electronics Engineering' },
  { slug: 'mechanical-engineering', name: 'Mechanical Engineering' },
  { slug: 'civil-engineering', name: 'Civil Engineering' },
  { slug: 'chemical-engineering', name: 'Chemical Engineering' },
  { slug: 'automobile-engineering', name: 'Automobile Engineering' },
  { slug: 'biomedical-engineering', name: 'Biomedical Engineering' },
  { slug: 'mechatronics-engineering', name: 'Mechatronics Engineering' },
  { slug: 'instrumentation-engineering', name: 'Instrumentation Engineering' },
  { slug: 'aeronautical-engineering', name: 'Aeronautical Engineering' },
  { slug: 'agricultural-engineering', name: 'Agricultural Engineering' },
  { slug: 'marine-engineering', name: 'Marine Engineering' },
  { slug: 'mining-engineering', name: 'Mining Engineering' },
  { slug: 'industrial-engineering', name: 'Industrial Engineering' },
  { slug: 'production-engineering', name: 'Production Engineering' },
  { slug: 'metallurgical-engineering', name: 'Metallurgical Engineering' },
  { slug: 'petroleum-engineering', name: 'Petroleum Engineering' },
  { slug: 'textile-engineering', name: 'Textile Engineering' },
  { slug: 'biotechnology-engineering', name: 'Biotechnology Engineering' },
  { slug: 'food-technology', name: 'Food Technology' },
  { slug: 'environmental-engineering', name: 'Environmental Engineering' },
];

async function getCareerSlugs(): Promise<string[]> {
  try {
    const res = await fetch('/api/careers', {
      next: { revalidate: 3600 },
    });
    if (!res.ok) return [];
    const data = await res.json();
    return (data || []).map((c: { slug: string }) => c.slug).filter(Boolean);
  } catch {
    return [];
  }
}

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const careerSlugs = await getCareerSlugs();

  const staticRoutes: MetadataRoute.Sitemap = [
    {
      url: BASE_URL,
      lastModified: new Date(),
      changeFrequency: 'weekly',
      priority: 1.0,
    },
  ];

  const branchRoutes: MetadataRoute.Sitemap = BRANCH_SLUGS.map(({ slug }) => ({
    url: `${BASE_URL}/branches/${slug}`,
    lastModified: new Date(),
    changeFrequency: 'monthly',
    priority: 0.8,
  }));

  const careerRoutes: MetadataRoute.Sitemap = careerSlugs.map((slug) => ({
    url: `${BASE_URL}/careers/${slug}`,
    lastModified: new Date(),
    changeFrequency: 'monthly',
    priority: 0.7,
  }));

  return [...staticRoutes, ...branchRoutes, ...careerRoutes];
}
