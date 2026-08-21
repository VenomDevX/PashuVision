'use client';

import { useSearchParams } from 'next/navigation';
import { Suspense, useEffect, useState } from 'react';
import PredictionCard from '@/components/PredictionCard';
import Link from 'next/link';
import { useLanguage } from '@/context/LanguageContext';

function ResultContent() {
  const searchParams = useSearchParams();
  const { t } = useLanguage();
  const [imageUrl, setImageUrl] = useState<string | undefined>(undefined);

  useEffect(() => {
    const storedImage = sessionStorage.getItem('scan_image');
    if (storedImage) {
      setImageUrl(storedImage);
    }
  }, []);
  
  const prediction = {
    species: searchParams.get('species') || 'Unknown',
    species_confidence: parseFloat(searchParams.get('species_confidence') || '0'),
    breed: searchParams.get('breed') || 'Unknown',
    breed_confidence: parseFloat(searchParams.get('breed_confidence') || '0'),
    image_url: imageUrl,
    kirti_code: searchParams.get('kirti_code') || undefined
  };

  if (prediction.species === 'Unknown' && prediction.breed === 'Unknown') {
    return (
      <div className="text-center py-20">
        <h2 className="text-2xl font-bold text-gray-700">{t('result_no_data')}</h2>
        <Link href="/scan" className="text-green-600 hover:underline mt-4 inline-block">{t('result_try_again')}</Link>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-12">
      <PredictionCard prediction={prediction} />
      <div className="text-center mt-8">
        <Link href="/scan" className="px-6 py-3 bg-gray-100 text-gray-700 font-semibold rounded-lg hover:bg-gray-200 transition-colors">
          {t('result_scan_another')}
        </Link>
      </div>
    </div>
  );
}

export default function ResultPage() {
  return (
    <Suspense fallback={<div className="text-center py-20">Loading results...</div>}>
      <ResultContent />
    </Suspense>
  );
}
