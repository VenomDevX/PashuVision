'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useLanguage } from '@/context/LanguageContext';

export default function Navbar() {
  const { language, setLanguage, t } = useLanguage();
  const pathname = usePathname();
  const isHome = pathname === '/';

  // Dynamic classes based on route
  const navBgClass = isHome 
    ? 'bg-transparent absolute top-0 w-full z-50' 
    : 'bg-white/80 backdrop-blur-md shadow-sm w-full sticky top-0 z-50 border-b border-gray-200';
  
  const textColorClass = isHome ? 'text-white' : 'text-gray-900';
  const logoTextClass = isHome ? 'text-white drop-shadow-md' : 'text-gray-900';
  const logoGreenClass = isHome ? 'text-green-400 drop-shadow-md' : 'text-green-600';
  const linkHoverClass = isHome ? 'hover:text-green-300 hover:border-green-300' : 'hover:text-green-600 hover:border-green-500';
  const selectBgClass = isHome ? 'bg-white/20 text-white border-white/40' : 'bg-gray-50 text-gray-900 border-gray-300';

  return (
    <nav className={navBgClass}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link href="/" className="flex-shrink-0 flex items-center">
              {language === 'en' ? (
                <span className={`text-2xl font-extrabold tracking-tight ${logoGreenClass}`}>
                  Pashu<span className={logoTextClass}>Drishti</span>
                </span>
              ) : (
                <span className={`text-2xl font-extrabold tracking-tight ${logoGreenClass}`}>
                  {t('brand')}
                </span>
              )}
            </Link>
            <div className="hidden sm:ml-8 sm:flex sm:space-x-8">
              <Link href="/scan" className={`${textColorClass} ${isHome ? 'opacity-90' : 'opacity-70'} inline-flex items-center px-1 pt-1 border-b-2 border-transparent ${linkHoverClass} text-sm font-medium transition-colors`}>
                {t('nav_new_scan')}
              </Link>
              <Link href="/history" className={`${textColorClass} ${isHome ? 'opacity-90' : 'opacity-70'} inline-flex items-center px-1 pt-1 border-b-2 border-transparent ${linkHoverClass} text-sm font-medium transition-colors`}>
                {t('nav_history')}
              </Link>
              <Link href="/dashboard" className={`${textColorClass} ${isHome ? 'opacity-90' : 'opacity-70'} inline-flex items-center px-1 pt-1 border-b-2 border-transparent ${linkHoverClass} text-sm font-medium transition-colors`}>
                {t('nav_dashboard')}
              </Link>
            </div>
          </div>
          
          <div className="flex items-center">
            <select
              value={language}
              // eslint-disable-next-line @typescript-eslint/no-explicit-any
              onChange={(e) => setLanguage(e.target.value as any)}
              className={`${selectBgClass} text-sm rounded-lg focus:ring-green-500 focus:border-green-500 block p-2 outline-none cursor-pointer backdrop-blur-sm`}
            >
              <option value="en" className="text-gray-900">English</option>
              <option value="hi" className="text-gray-900">हिंदी (Hindi)</option>
              <option value="mr" className="text-gray-900">मराठी (Marathi)</option>
              <option value="gu" className="text-gray-900">ગુજરાતી (Gujarati)</option>
              <option value="ta" className="text-gray-900">தமிழ் (Tamil)</option>
              <option value="te" className="text-gray-900">తెలుగు (Telugu)</option>
            </select>
          </div>
        </div>
      </div>
    </nav>
  );
}
