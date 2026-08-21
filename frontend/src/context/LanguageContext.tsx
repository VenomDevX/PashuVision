'use client';

import React, { createContext, useContext, useState, ReactNode } from 'react';
import { en } from '@/translations/en';
import { hi } from '@/translations/hi';
import { mr } from '@/translations/mr';
import { gu } from '@/translations/gu';
import { ta } from '@/translations/ta';
import { te } from '@/translations/te';

type Language = 'en' | 'hi' | 'mr' | 'gu' | 'ta' | 'te';
type Translations = typeof en;

interface LanguageContextType {
  language: Language;
  setLanguage: (lang: Language) => void;
  t: (key: keyof Translations) => string;
}

const LanguageContext = createContext<LanguageContextType | undefined>(undefined);

const translations: Record<Language, Translations> = {
  en,
  hi,
  mr,
  gu,
  ta,
  te,
};

export const LanguageProvider = ({ children }: { children: ReactNode }) => {
  const [language, setLanguage] = useState<Language>('en');

  const t = (key: keyof Translations) => {
    return translations[language][key] || translations['en'][key] || key;
  };

  return (
    <LanguageContext.Provider value={{ language, setLanguage, t }}>
      {children}
    </LanguageContext.Provider>
  );
};

export const useLanguage = () => {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error('useLanguage must be used within a LanguageProvider');
  }
  return context;
};
