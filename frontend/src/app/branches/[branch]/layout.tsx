import type { Metadata } from 'next';

const BASE_URL = 'https://engineeeringroadmaps.nexgenu.dpdns.org';

// Map of branch slugs to human-readable names and descriptions
const BRANCH_META: Record<string, { name: string; desc: string; keywords: string[] }> = {
  'computer-science-engineering': {
    name: 'Computer Science Engineering (CSE)',
    desc: 'Explore career paths in Computer Science Engineering — from software development and AI to cybersecurity, cloud computing, and data science. Get free step-by-step roadmaps.',
    keywords: ['CSE careers', 'computer science jobs', 'software engineer roadmap', 'programming career India', 'IT jobs for CSE'],
  },
  'information-technology': {
    name: 'Information Technology (IT)',
    desc: 'Discover career options for Information Technology graduates — web development, networking, cybersecurity, and cloud. Free roadmaps with skills, certifications, and interview prep.',
    keywords: ['IT careers', 'information technology jobs India', 'web developer roadmap', 'network engineer career'],
  },
  'artificial-intelligence-and-data-science': {
    name: 'Artificial Intelligence & Data Science',
    desc: 'Career roadmaps for AI and Data Science — machine learning, deep learning, NLP, data analytics, and MLOps. Learn required skills, tools, and certifications.',
    keywords: ['AI careers India', 'data science roadmap', 'machine learning jobs', 'NLP career path', 'MLOps engineer'],
  },
  'electronics-and-communication-engineering': {
    name: 'Electronics & Communication Engineering (ECE)',
    desc: 'ECE career roadmaps covering VLSI design, embedded systems, telecommunications, RF engineering, and IoT. Explore core and IT career paths for ECE graduates.',
    keywords: ['ECE careers', 'electronics engineer jobs', 'VLSI design career', 'embedded systems roadmap', 'telecom career India'],
  },
  'electrical-and-electronics-engineering': {
    name: 'Electrical & Electronics Engineering (EEE)',
    desc: 'Career paths for EEE graduates — power systems, renewable energy, PLC/SCADA, and electrical design engineering. Explore government and core industry jobs.',
    keywords: ['EEE careers', 'electrical engineer jobs India', 'power systems career', 'renewable energy roadmap', 'PSU jobs EEE'],
  },
  'mechanical-engineering': {
    name: 'Mechanical Engineering',
    desc: 'Mechanical Engineering career roadmaps — automobile, manufacturing, CAD/CAM, aerospace, robotics, and thermal engineering. Explore core sector and PSU opportunities.',
    keywords: ['mechanical engineer jobs', 'mechanical career roadmap', 'automobile engineering career', 'CAD CAM jobs India', 'PSU for mechanical'],
  },
  'civil-engineering': {
    name: 'Civil Engineering',
    desc: 'Civil Engineering career guide — structural design, urban planning, geotechnical, transportation, and water resources engineering. Government and private sector roadmaps.',
    keywords: ['civil engineer jobs', 'civil engineering career India', 'structural engineer roadmap', 'urban planning career', 'UPSC for civil engineers'],
  },
  'chemical-engineering': {
    name: 'Chemical Engineering',
    desc: 'Chemical Engineering career roadmaps — petroleum refining, pharmaceutical manufacturing, environmental engineering, and process design. Core and government job pathways.',
    keywords: ['chemical engineer jobs India', 'chemical engineering career', 'petroleum refinery career', 'pharma manufacturing jobs'],
  },
  'automobile-engineering': {
    name: 'Automobile Engineering',
    desc: 'Automobile Engineering career paths — vehicle design, EV engineering, automotive testing, and manufacturing. Explore career roadmaps in the growing Indian auto industry.',
    keywords: ['automobile engineer career', 'automotive engineering jobs India', 'EV engineer roadmap', 'vehicle design career'],
  },
  'biomedical-engineering': {
    name: 'Biomedical Engineering',
    desc: 'Biomedical Engineering career roadmaps — medical devices, clinical engineering, bioinformatics, and hospital management. Explore healthcare and research career paths.',
    keywords: ['biomedical engineer jobs India', 'medical device career', 'clinical engineer roadmap', 'bioinformatics career'],
  },
};

function getBranchMeta(slug: string) {
  return BRANCH_META[slug] || {
    name: slug.split('-').map((w) => w.charAt(0).toUpperCase() + w.slice(1)).join(' '),
    desc: `Explore career roadmaps for ${slug.replace(/-/g, ' ')} graduates. Get step-by-step career guides with skills matrix, certifications, and interview preparation on NexGenU.`,
    keywords: [`${slug.replace(/-/g, ' ')} career`, `${slug.replace(/-/g, ' ')} jobs India`, 'engineering career roadmap'],
  };
}

export async function generateMetadata({
  params,
}: {
  params: { branch: string };
}): Promise<Metadata> {
  const { branch } = params;
  const meta = getBranchMeta(branch);
  const canonicalUrl = `${BASE_URL}/branches/${branch}`;

  return {
    title: `${meta.name} Career Roadmaps`,
    description: meta.desc,
    keywords: [
      ...meta.keywords,
      'NexGenU', 'engineering career guide', 'free career roadmap India',
      'engineering branch career paths', 'campus placement preparation',
    ],
    alternates: { canonical: canonicalUrl },
    openGraph: {
      title: `${meta.name} Career Roadmaps | NexGenU`,
      description: meta.desc,
      url: canonicalUrl,
      type: 'website',
      images: [{ url: `${BASE_URL}/og-image.png`, width: 1200, height: 630, alt: `${meta.name} Career Roadmaps` }],
    },
    twitter: {
      card: 'summary_large_image',
      title: `${meta.name} Career Roadmaps | NexGenU`,
      description: meta.desc,
      images: [`${BASE_URL}/og-image.png`],
    },
  };
}

export default function BranchLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
