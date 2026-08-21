'use client';

import { useState } from 'react';

export default function ImageUploader({ onUpload, isUploading }: { onUpload: (file: File, speciesHint: string) => void, isUploading: boolean }) {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [speciesHint, setSpeciesHint] = useState<string>('auto');

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const selectedFile = e.target.files[0];
      setFile(selectedFile);
      setPreview(URL.createObjectURL(selectedFile));
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (file && !isUploading) {
      onUpload(file, speciesHint);
    }
  };

  return (
    <div className="max-w-xl mx-auto bg-white p-8 rounded-xl shadow-lg border border-gray-100 mt-8">
      <h2 className="text-2xl font-bold mb-6 text-center text-gray-800">Identify Livestock Breed</h2>
      <form onSubmit={handleSubmit} className="space-y-6">
        
        {/* Upload Area */}
        <div className="flex items-center justify-center w-full">
          <label htmlFor="dropzone-file" className="flex flex-col items-center justify-center w-full h-64 border-2 border-dashed rounded-lg cursor-pointer bg-gray-50 border-gray-300 hover:bg-gray-100 transition-colors">
            {preview ? (
              <img src={preview} alt="Preview" className="w-full h-full object-contain p-2 rounded-lg" />
            ) : (
              <div className="flex flex-col items-center justify-center pt-5 pb-6">
                <svg className="w-10 h-10 mb-3 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
                </svg>
                <p className="mb-2 text-sm text-gray-500"><span className="font-semibold">Click to upload</span> or drag and drop</p>
                <p className="text-xs text-gray-500">PNG, JPG or JPEG (MAX. 5MB)</p>
              </div>
            )}
            <input id="dropzone-file" type="file" className="hidden" accept="image/png, image/jpeg, image/jpg" onChange={handleFileChange} />
          </label>
        </div>

        {/* Species Hint */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Species (Optional Hint)</label>
          <select 
            value={speciesHint} 
            onChange={(e) => setSpeciesHint(e.target.value)}
            className="w-full border border-gray-300 rounded-lg p-3 focus:ring-green-500 focus:border-green-500 bg-white text-gray-900"
          >
            <option value="auto" className="text-gray-900">Auto-Detect</option>
            <option value="cattle" className="text-gray-900">Cattle</option>
            <option value="buffalo" className="text-gray-900">Buffalo</option>
          </select>
        </div>

        <button 
          type="submit" 
          disabled={!file || isUploading}
          className={`w-full py-3 px-4 rounded-lg text-white font-bold text-lg transition-all flex justify-center items-center ${
            file && !isUploading ? 'bg-green-600 hover:bg-green-700 shadow-md' : 'bg-gray-400 cursor-not-allowed'
          }`}
        >
          {isUploading ? (
            <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
          ) : 'Analyze Breed'}
        </button>
      </form>
    </div>
  );
}
