'use client';
import React, { useEffect, useState } from 'react';
import { usePathname } from 'next/navigation';
import { motion, AnimatePresence } from 'framer-motion';

export default function AdBanner() {
  const pathname = usePathname();
  const [ads, setAds] = useState<any[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);

  useEffect(() => {
    fetch('https://nexgenu-career-guide.onrender.com/api/ui/ads')
      .then(res => res.json())
      .then(data => {
        if (Array.isArray(data)) {
          setAds(data.filter(ad => ad.is_active === 1));
        }
      })
      .catch(err => console.error("Failed to fetch ads", err));
  }, []);

  // Rotate ads every 8 seconds if there are multiple
  useEffect(() => {
    if (ads.length > 1) {
      const interval = setInterval(() => {
        setCurrentIndex((prev) => (prev + 1) % ads.length);
      }, 8000);
      return () => clearInterval(interval);
    }
  }, [ads.length]);

  // DO NOT show on homepage '/'
  if (pathname === '/' || ads.length === 0) return null;

  const currentAd = ads[currentIndex];

  // Helper to extract direct image URL if user pastes a Bing Image Search link
  const getCleanImageUrl = (url: string) => {
    if (!url) return url;
    try {
      if (url.includes('bing.com/images/search') && url.includes('mediaurl=')) {
        const urlObj = new URL(url);
        const mediaurl = urlObj.searchParams.get('mediaurl');
        if (mediaurl) return mediaurl;
      }
    } catch (e) {
      // ignore parsing errors
    }
    return url;
  };

  const displayImageUrl = getCleanImageUrl(currentAd.image_url);

  return (
    <div className="w-full bg-gradient-to-r from-purple-900 via-indigo-900 to-purple-900 border-b border-purple-500/30 overflow-hidden relative z-50">
      <AnimatePresence mode="wait">
        <motion.div
          key={currentAd.id}
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: 20 }}
          transition={{ duration: 0.5 }}
          className="max-w-7xl mx-auto px-6 py-5 flex flex-col sm:flex-row items-center justify-center sm:justify-between gap-6"
        >
          <div className="flex items-center gap-5 flex-1 min-w-0">
            {displayImageUrl && (
              <img src={displayImageUrl} alt="Ad" className="h-14 w-auto rounded-lg shadow-sm object-cover flex-shrink-0" />
            )}
            <div className="text-white text-center sm:text-left min-w-0">
              <div className="font-extrabold text-base sm:text-lg flex items-center gap-2 justify-center sm:justify-start">
                <span className="bg-yellow-500 text-black text-[10px] uppercase font-black px-2 py-0.5 rounded-sm tracking-widest shadow-sm flex-shrink-0">Ad</span>
                <span className="truncate">{currentAd.title}</span>
              </div>
              {currentAd.description && (
                <p className="text-sm sm:text-base text-white/80 line-clamp-3 mt-0.5 break-words">{currentAd.description}</p>
              )}
            </div>
          </div>
          
          {currentAd.link_url && (
            <a 
              href={currentAd.link_url} 
              target="_blank" 
              rel="noopener noreferrer"
              className="flex-shrink-0 px-4 py-1.5 bg-white text-purple-900 hover:bg-purple-100 font-bold text-sm rounded-full transition-colors shadow-lg"
            >
              Learn More →
            </a>
          )}
        </motion.div>
      </AnimatePresence>
      
      {/* Indicator dots if multiple ads */}
      {ads.length > 1 && (
        <div className="absolute bottom-1 left-0 right-0 flex justify-center gap-1">
          {ads.map((_, idx) => (
            <div key={idx} className={`w-1.5 h-1.5 rounded-full ${idx === currentIndex ? 'bg-white' : 'bg-white/30'}`} />
          ))}
        </div>
      )}
    </div>
  );
}
