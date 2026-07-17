import type { Metadata } from "next";
import "./globals.css";
import Navbar from "@/components/Navbar";
import AdBanner from "@/components/ui/AdBanner";

const BASE_URL = "https://engineeeringroadmaps.nexgenu.dpdns.org";

export const metadata: Metadata = {
  metadataBase: new URL(BASE_URL),
  title: {
    default: "NexGenU | Engineering Career Roadmaps Platform",
    template: "%s | NexGenU",
  },
  description:
    "NexGenU is India's largest engineering career roadmap platform. Explore 300+ career paths across 24 engineering branches with AI-generated roadmaps, skills matrix, projects, certifications, and interview preparation — completely free.",
  keywords: [
    "engineering career roadmap", "career guide for engineers", "engineering jobs India",
    "NexGenU", "software engineer career path", "mechanical engineer career",
    "civil engineer jobs", "ECE career roadmap", "EEE careers India",
    "CSE career guide", "AI career roadmap", "data science career path",
    "engineering branch career", "best careers for engineers", "engineering placement guide",
    "core jobs engineering", "IT careers for engineers", "government jobs engineering",
    "PSU careers", "engineering certifications", "engineering interview preparation",
    "career roadmap India", "engineering learning plan", "project ideas engineering",
    "skills for engineers", "free career guidance", "campus placement preparation",
  ],
  authors: [{ name: "NexGenU Team", url: BASE_URL }],
  creator: "NexGenU",
  publisher: "NexGenU",
  robots: {
    index: true,
    follow: true,
    googleBot: { index: true, follow: true, "max-image-preview": "large", "max-snippet": -1 },
  },
  alternates: { canonical: BASE_URL },
  openGraph: {
    type: "website",
    locale: "en_IN",
    url: BASE_URL,
    siteName: "NexGenU Career Roadmaps",
    title: "NexGenU | Engineering Career Roadmaps Platform",
    description:
      "Explore 300+ engineering career roadmaps with skills matrix, learning plans, projects, certifications, and interview prep — all free on NexGenU.",
    images: [
      {
        url: `${BASE_URL}/og-image.png`,
        width: 1200,
        height: 630,
        alt: "NexGenU Engineering Career Roadmaps Platform",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "NexGenU | Engineering Career Roadmaps Platform",
    description:
      "Explore 300+ engineering career roadmaps for free. Skills, projects, certifications & interview prep — tailored to your branch.",
    images: [`${BASE_URL}/og-image.png`],
    creator: "@NexGenU",
  },
  verification: {
    google: "SVpM6iJtWF8lh7gELxBms7ccD3hF9XuZGsMV0VOwpDQ",
  },
};

const organizationSchema = {
  "@context": "https://schema.org",
  "@type": "EducationalOrganization",
  name: "NexGenU",
  url: BASE_URL,
  logo: `${BASE_URL}/og-image.png`,
  description: "India's largest engineering career roadmap and guidance platform.",
  address: { "@type": "PostalAddress", addressCountry: "IN" },
  contactPoint: { "@type": "ContactPoint", email: "nexgenu.careers@gmail.com", contactType: "customer support" },
  sameAs: ["https://nexgenu.dpdns.org"],
};

const websiteSchema = {
  "@context": "https://schema.org",
  "@type": "WebSite",
  name: "NexGenU Career Roadmaps",
  url: BASE_URL,
  potentialAction: {
    "@type": "SearchAction",
    target: { "@type": "EntryPoint", urlTemplate: `${BASE_URL}/branches/{search_term_string}` },
    "query-input": "required name=search_term_string",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <head>
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(organizationSchema) }}
        />
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(websiteSchema) }}
        />
      </head>
      <body className="antialiased flex flex-col min-h-screen">
        <AdBanner />
        <Navbar />
        <main className="flex-1">
          {children}
        </main>
        <AdBanner />
      </body>
    </html>
  );
}

