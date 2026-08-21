'use client';

import Link from 'next/link';
import { useLanguage } from '@/context/LanguageContext';

export default function Home() {
  const { t } = useLanguage();

  return (
    <div 
      className="relative flex flex-col items-center justify-center min-h-screen px-4 text-center overflow-hidden"
    >
      {/* Background Image with Overlay */}
      <div 
        className="absolute inset-0 z-0 bg-cover bg-center"
        style={{ backgroundImage: "url('/hero_bg.jpg')" }}
      >
        <div className="absolute inset-0 bg-black/60"></div>
      </div>

      {/* Content */}
      <div className="relative z-10 flex flex-col items-center max-w-4xl w-full">
        {/* Glassmorphism Container */}
        <div className="backdrop-blur-md bg-white/10 border border-white/20 p-8 md:p-12 rounded-2xl shadow-2xl">
          <h1 className="text-4xl md:text-6xl lg:text-7xl font-extrabold text-white tracking-tight mb-6 drop-shadow-lg">
            {t('hero_title_1')}
            <span className="text-green-400">{t('hero_title_2')}</span>
            {t('hero_title_3')}
          </h1>
          <p className="text-lg md:text-2xl text-gray-200 mb-10 leading-relaxed font-light drop-shadow-md">
            {t('hero_subtitle')}
          </p>
          <div className="flex flex-col sm:flex-row gap-6 justify-center">
            <Link 
              href="/scan" 
              className="px-8 py-4 bg-green-600 hover:bg-green-500 text-white font-bold rounded-xl text-lg shadow-[0_0_15px_rgba(34,197,94,0.5)] transition-all hover:scale-105"
            >
              {t('btn_scan')}
            </Link>
            <Link 
              href="/history" 
              className="px-8 py-4 bg-white/20 hover:bg-white/30 backdrop-blur-sm border border-white/30 text-white font-bold rounded-xl text-lg shadow-lg transition-all hover:scale-105"
            >
              {t('btn_history')}
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
