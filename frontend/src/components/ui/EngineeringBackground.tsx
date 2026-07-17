'use client';
import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';

// Array of engineering-related icons
const ICONS = [
  '⚙️', // Mechanical
  '⚡', // Electrical
  '🏗️', // Civil
  '</>', // IT/CS
  '📐', // Architecture/Civil
  '🛰️', // Aerospace
  '🔌', // Electronics
  '🔬', // Chemical/Biotech
  '🔧', // Core Engineering
  '📡', // Telecommunications
  '✈️', // Aeronautical
];

interface FloatingIcon {
  id: number;
  icon: string;
  size: number;
  startX: number;
  startY: number;
  duration: number;
  delay: number;
}

export default function EngineeringBackground() {
  const [icons, setIcons] = useState<FloatingIcon[]>([]);

  useEffect(() => {
    // Generate random icons on mount to avoid hydration mismatch
    const generatedIcons = Array.from({ length: 80 }).map((_, i) => ({
      id: i,
      icon: ICONS[Math.floor(Math.random() * ICONS.length)],
      size: Math.floor(Math.random() * 40) + 20, // 20px to 60px
      startX: Math.random() * 100, // 0 to 100%
      startY: Math.random() * 100, // 0 to 100%
      duration: Math.random() * 20 + 20, // 20s to 40s floating duration
      delay: Math.random() * 5, // 0 to 5s delay
    }));
    setIcons(generatedIcons);
  }, []);

  if (icons.length === 0) return null;

  return (
    <div className="absolute inset-0 overflow-hidden pointer-events-none -z-10">
      {icons.map((item) => (
        <motion.div
          key={item.id}
          className="absolute opacity-40 dark:opacity-50 text-foreground/80 select-none flex items-center justify-center font-mono font-bold"
          style={{
            fontSize: item.size,
            left: `${item.startX}%`,
            top: `${item.startY}%`,
          }}
          initial={{
            y: 0,
            x: 0,
            rotate: 0,
          }}
          animate={{
            y: [0, -100, 0, 100, 0],
            x: [0, 50, 100, -50, 0],
            rotate: [0, 90, 180, 270, 360],
          }}
          transition={{
            duration: item.duration,
            repeat: Infinity,
            ease: "linear",
            delay: item.delay,
          }}
        >
          {item.icon}
        </motion.div>
      ))}
    </div>
  );
}
