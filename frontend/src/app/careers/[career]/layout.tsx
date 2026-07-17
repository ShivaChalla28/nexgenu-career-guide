import type { Metadata } from 'next';

const BASE_URL = 'https://engineeeringroadmaps.nexgenu.dpdns.org';

function slugToTitle(slug: string): string {
  return slug
    .split('-')
    .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
    .join(' ');
}

async function getCareerData(slug: string): Promise<{ name?: string; overview?: string; branch?: string } | null> {
  try {
    const res = await fetch(`https://nexgenu-career-guide.onrender.com/api/careers/${slug}`, {
      next: { revalidate: 3600 },
    });
    if (!res.ok) return null;
    const data = await res.json();
    return data?.career || null;
  } catch {
    return null;
  }
}

export async function generateMetadata({
  params,
}: {
  params: { career: string };
}): Promise<Metadata> {
  const { career: slug } = params;
  const careerData = await getCareerData(slug);

  const name = careerData?.name || slugToTitle(slug);
  const branch = careerData?.branch || 'Engineering';
  const overview = careerData?.overview;

  const title = `${name} Career Roadmap`;
  const description = overview
    ? `${overview.slice(0, 155)}...`
    : `Complete ${name} career roadmap for ${branch} graduates. Learn required skills, projects, certifications, and interview preparation. Free step-by-step guide on NexGenU.`;

  const keywords = [
    `${name} career roadmap`,
    `${name} jobs India`,
    `how to become ${name}`,
    `${name} skills required`,
    `${name} salary India`,
    `${name} certifications`,
    `${name} interview questions`,
    `${branch} career paths`,
    'engineering career guide India',
    'free career roadmap',
    'NexGenU',
    'step by step career plan',
    'engineering job preparation',
  ];

  const canonicalUrl = `${BASE_URL}/careers/${slug}`;

  const courseSchema = {
    '@context': 'https://schema.org',
    '@type': 'Course',
    name: `${name} Career Roadmap`,
    description,
    provider: {
      '@type': 'Organization',
      name: 'NexGenU',
      sameAs: BASE_URL,
    },
    url: canonicalUrl,
    isAccessibleForFree: true,
    inLanguage: 'en-IN',
    educationalLevel: 'Undergraduate',
    about: { '@type': 'Thing', name },
  };

  const breadcrumbSchema = {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: [
      { '@type': 'ListItem', position: 1, name: 'Home', item: BASE_URL },
      { '@type': 'ListItem', position: 2, name: 'Branches', item: `${BASE_URL}/dashboard` },
      { '@type': 'ListItem', position: 3, name, item: canonicalUrl },
    ],
  };

  return {
    title,
    description,
    keywords,
    alternates: { canonical: canonicalUrl },
    openGraph: {
      title: `${title} | NexGenU`,
      description,
      url: canonicalUrl,
      type: 'article',
      images: [{ url: `${BASE_URL}/og-image.png`, width: 1200, height: 630, alt: `${name} Career Roadmap` }],
    },
    twitter: {
      card: 'summary_large_image',
      title: `${title} | NexGenU`,
      description,
      images: [`${BASE_URL}/og-image.png`],
    },
    other: {
      'script:ld+json:course': JSON.stringify(courseSchema),
      'script:ld+json:breadcrumb': JSON.stringify(breadcrumbSchema),
    },
  };
}

export default function CareerLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
