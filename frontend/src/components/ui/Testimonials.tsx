'use client';
import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';

export default function Testimonials() {
  const [feedbacks, setFeedbacks] = useState<any[]>([]);

  useEffect(() => {
    fetch('/api/feedback/approved')
      .then(res => res.json())
      .then(data => {
        if (Array.isArray(data)) {
          setFeedbacks(data);
        }
      })
      .catch(err => console.error("Failed to fetch feedback:", err));
  }, []);

  if (feedbacks.length === 0) return null;

  return (
    <section className="w-full max-w-7xl px-6 py-24 border-t border-foreground/10 mx-auto">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        className="text-center mb-16"
      >
        <p className="text-sm text-foreground/50 uppercase tracking-widest mb-3 font-semibold">Student Success</p>
        <h2 className="text-4xl md:text-5xl font-extrabold mb-4">Trusted by Engineers</h2>
        <p className="text-foreground/60 max-w-xl mx-auto text-lg">
          See how students from top colleges across India are using NexGenU to secure their dream careers.
        </p>
      </motion.div>

      <div className="relative w-full overflow-hidden py-4 [mask-image:_linear-gradient(to_right,transparent_0,_black_128px,_black_calc(100%-128px),transparent_100%)]">
        <motion.div
          className="flex gap-6 w-max"
          animate={{ x: ["0%", "-50%"] }}
          transition={{ duration: 40, ease: "linear", repeat: Infinity }}
        >
          {[...feedbacks, ...feedbacks].map((item, i) => (
            <div
              key={`${item.id}-${i}`}
              className="w-[300px] md:w-[400px] shrink-0 p-8 rounded-2xl border border-foreground/10 bg-foreground/3 hover:border-blue-500/30 transition-colors flex flex-col justify-between h-full min-h-[250px]"
            >
              <div>
                <div className="flex text-yellow-500 mb-4 text-sm">
                  {[...Array(item.rating)].map((_, idx) => (
                    <span key={idx}>★</span>
                  ))}
                </div>
                <p className="text-foreground/80 italic mb-6 leading-relaxed text-sm md:text-base">
                  "{item.text}"
                </p>
              </div>
              
              <div className="flex items-center gap-4 mt-auto">
                <div className="w-12 h-12 rounded-full bg-foreground/10 flex items-center justify-center text-2xl shadow-inner uppercase font-bold text-foreground/50 shrink-0">
                  {item.name.charAt(0)}
                </div>
                <div>
                  <h4 className="font-bold text-foreground text-sm">{item.name}</h4>
                  <p className="text-xs text-foreground/50">{item.branch || 'Engineering Student'}</p>
                  {item.college && <p className="text-xs text-blue-500/80 font-medium">{item.college}</p>}
                </div>
              </div>
            </div>
          ))}
        </motion.div>
      </div>
    </section>
  );
}
