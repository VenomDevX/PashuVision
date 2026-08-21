'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import ImageUploader from '@/components/ImageUploader';
import { predictBreed } from '@/lib/api';
import { useLanguage } from '@/context/LanguageContext';

export default function ScanPage() {
  const router = useRouter();
  const { t } = useLanguage();
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleUpload = async (file: File, speciesHint: string) => {
    setIsUploading(true);
    setError(null);
    try {
      const reader = new FileReader();
      const imageDataUrl = await new Promise<string>((resolve) => {
        reader.onloadend = () => resolve(reader.result as string);
        reader.readAsDataURL(file);
      });

      const data = await predictBreed(file, speciesHint);

      sessionStorage.setItem('scan_image', imageDataUrl);

      const query = new URLSearchParams({
        species: data.species,
        species_confidence: data.species_confidence.toString(),
        breed: data.breed,
        breed_confidence: data.breed_confidence.toString(),
        kirti_code: data.kirti_code || '',
      }).toString();
      
      router.push(`/result?${query}`);
    } catch (err) {
      setError(t('scan_error'));
      console.error(err);
      setIsUploading(false);
    }
  };

  return (
    <div className="container mx-auto px-4 py-12">
      <div className="text-center mb-12">
        <h1 className="text-4xl font-extrabold text-gray-900 tracking-tight sm:text-5xl">
          {t('scan_title_1')}<span className="text-green-600">{t('scan_title_2')}</span>
        </h1>
        <p className="mt-4 text-xl text-gray-500 max-w-2xl mx-auto">
          {t('scan_subtitle')}
        </p>
      </div>

      <ImageUploader onUpload={handleUpload} isUploading={isUploading} />
      
      {error && (
        <div className="max-w-xl mx-auto mt-6 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-center font-medium">
          {error}
        </div>
      )}
    </div>
  );
}
