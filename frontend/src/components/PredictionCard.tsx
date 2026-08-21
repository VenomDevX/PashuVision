import ConfidenceBar from './ConfidenceBar';
import { useLanguage } from '@/context/LanguageContext';

interface PredictionProps {
  prediction: {
    species: string;
    species_confidence: number;
    breed: string;
    breed_confidence: number;
    image_url?: string;
    kirti_code?: string;
  };
}

export default function PredictionCard({ prediction }: PredictionProps) {
  const { t } = useLanguage();
  const imageUrl = prediction.image_url || null;

  return (
    <div className="max-w-2xl mx-auto bg-white p-8 rounded-xl shadow-lg border border-gray-100 mt-8">
      <h2 className="text-3xl font-bold text-center text-gray-800 mb-8 border-b pb-4">{t('result_title')}</h2>
      
      <div className="flex flex-col md:flex-row gap-8">
        {imageUrl && (
          <div className="w-full md:w-1/2">
            <div className="aspect-square rounded-lg overflow-hidden border border-gray-200 shadow-sm">
              <img src={imageUrl} alt="Analyzed Livestock" className="w-full h-full object-cover" />
            </div>
          </div>
        )}
        
        <div className={`w-full ${imageUrl ? 'md:w-1/2' : ''} flex flex-col justify-center`}>
          {prediction.kirti_code && (
            <div className="bg-green-50 p-4 rounded-lg border border-green-200 shadow-sm mb-6 text-center">
              <p className="text-xs text-green-600 font-bold uppercase tracking-wider mb-1">Kirti Code (Tag)</p>
              <p className="text-2xl font-mono font-extrabold text-green-800 tracking-widest">{prediction.kirti_code}</p>
            </div>
          )}
          
          <div className="bg-gray-50 p-6 rounded-lg border border-gray-200 shadow-sm mb-6">
            <p className="text-sm text-gray-500 font-medium uppercase tracking-wider mb-1">{t('card_species')}</p>
            <p className="text-xl font-bold text-gray-800">{prediction.species}</p>
          </div>

          <div className="bg-gray-50 p-6 rounded-lg border border-gray-200 shadow-sm mb-6">
            <p className="text-sm text-gray-500 font-medium uppercase tracking-wider mb-1">{t('card_breed')}</p>
            <p className="text-3xl font-extrabold text-green-700">{prediction.breed}</p>
          </div>
          
          <div className="space-y-4">
            <ConfidenceBar label={t('card_conf_species')} value={prediction.species_confidence} />
            <ConfidenceBar label={t('card_conf_breed')} value={prediction.breed_confidence} />
          </div>
        </div>
      </div>
    </div>
  );
}
