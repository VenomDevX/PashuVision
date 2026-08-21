'use client';

import { useEffect, useState } from 'react';
import { useLanguage } from '@/context/LanguageContext';

export default function HistoryPage() {
  const [scans, setScans] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const { t } = useLanguage();

  const fetchScans = async (search = '') => {
    setLoading(true);
    try {
      const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const url = search ? `${API_URL}/api/v1/scans/?search=${search}` : `${API_URL}/api/v1/scans/`;
      const res = await fetch(url);
      if (res.ok) {
        const data = await res.json();
        setScans(data);
      }
    } catch (err) {
      console.error("Failed to load history", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchScans();
  }, []);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    fetchScans(searchQuery);
  };

  const handleImageError = (e: React.SyntheticEvent<HTMLImageElement, Event>) => {
    e.currentTarget.style.display = 'none';
    e.currentTarget.parentElement!.innerHTML = '<div class="w-full h-full flex items-center justify-center text-gray-400 bg-gray-50 text-sm font-medium">Image Unavailable</div>';
  };

  return (
    <div className="container mx-auto px-4 py-12">
      <div className="flex flex-col md:flex-row items-center justify-between mb-10 gap-4">
        <h1 className="text-4xl font-extrabold text-gray-900 tracking-tight">{t('nav_history')}</h1>
        
        <form onSubmit={handleSearch} className="w-full md:w-auto relative">
          <input
            type="text"
            placeholder="Search by Kirti Code..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full md:w-80 pl-10 pr-4 py-3 bg-white/80 backdrop-blur-md border border-gray-200 rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all"
          />
          <div className="absolute left-3 top-3.5 text-gray-400">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
          </div>
          <button type="submit" className="hidden">Search</button>
        </form>
      </div>
      
      {loading ? (
        <div className="flex justify-center py-32">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600"></div>
        </div>
      ) : scans.length === 0 ? (
        <div className="text-center py-32 bg-white/50 backdrop-blur-sm rounded-2xl border border-gray-100 shadow-sm">
          <p className="text-gray-500 text-xl font-light">No scans found.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">
          {/* eslint-disable-next-line @typescript-eslint/no-explicit-any */}
          {scans.map((scan: any) => (
            <div key={scan.id} className="group bg-white/80 backdrop-blur-md rounded-2xl shadow-sm border border-gray-100/50 overflow-hidden hover:shadow-xl hover:-translate-y-1 transition-all duration-300">
              <div className="h-56 bg-gray-50 overflow-hidden relative border-b border-gray-100">
                {scan.image_url ? (
                  <img 
                    src={`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}${scan.image_url}`} 
                    alt="Scan" 
                    onError={handleImageError}
                    className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105" 
                  />
                ) : (
                  <div className="w-full h-full flex items-center justify-center text-gray-400 text-sm font-medium">No Image</div>
                )}
                
                {scan.kirti_code && (
                  <div className="absolute bottom-2 left-2 bg-black/60 backdrop-blur-sm text-white text-xs font-mono px-2 py-1 rounded">
                    {scan.kirti_code}
                  </div>
                )}
              </div>
              <div className="p-6">
                <div className="flex justify-between items-start mb-3">
                  <h3 className="font-extrabold text-xl text-gray-900 truncate pr-2">{scan.breed}</h3>
                  <span className="bg-green-50 text-green-700 border border-green-200 text-xs font-bold px-2.5 py-1 rounded-full whitespace-nowrap">
                    {scan.breed_confidence.toFixed(1)}%
                  </span>
                </div>
                <p className="text-sm text-gray-500 font-medium mb-5">{scan.species} ({scan.species_confidence.toFixed(1)}%)</p>
                <div className="text-xs text-gray-400 flex items-center font-medium">
                  <svg className="w-4 h-4 mr-1.5 opacity-70" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                  {new Date(scan.created_at).toLocaleString(undefined, { dateStyle: 'medium', timeStyle: 'short' })}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
