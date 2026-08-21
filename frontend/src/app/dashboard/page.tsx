'use client';

export default function DashboardPage() {
  return (
    <div className="container mx-auto px-4 py-12">
      <div className="flex items-center justify-between mb-10">
        <h1 className="text-4xl font-extrabold text-gray-900 tracking-tight">Analytics Dashboard</h1>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-10">
        <div className="bg-white/80 backdrop-blur-md p-8 rounded-2xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
          <h3 className="text-gray-400 text-xs font-bold tracking-wider uppercase mb-3">Total Scans</h3>
          <p className="text-5xl font-extrabold text-gray-900">1,248</p>
          <span className="inline-flex items-center mt-3 bg-green-50 text-green-700 border border-green-200 text-xs font-bold px-2 py-0.5 rounded-full">
            ↑ 12% this week
          </span>
        </div>
        
        <div className="bg-white/80 backdrop-blur-md p-8 rounded-2xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
          <h3 className="text-gray-400 text-xs font-bold tracking-wider uppercase mb-3">Accuracy Average</h3>
          <p className="text-5xl font-extrabold text-gray-900">94.2%</p>
          <span className="inline-flex items-center mt-3 bg-green-50 text-green-700 border border-green-200 text-xs font-bold px-2 py-0.5 rounded-full">
            ↑ 2.1% this week
          </span>
        </div>
        
        <div className="bg-white/80 backdrop-blur-md p-8 rounded-2xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
          <h3 className="text-gray-400 text-xs font-bold tracking-wider uppercase mb-3">Top Breed Detected</h3>
          <p className="text-5xl font-extrabold text-green-600">Gir</p>
          <span className="inline-flex items-center mt-3 text-gray-400 text-sm font-medium">
            342 scans
          </span>
        </div>
      </div>
      
      <div className="bg-white/50 backdrop-blur-sm p-12 rounded-3xl shadow-sm border border-gray-100 text-center">
        <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-green-100 text-green-600 mb-6">
          <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path></svg>
        </div>
        <h3 className="text-2xl text-gray-800 font-bold mb-3">Detailed charts coming soon</h3>
        <p className="text-gray-500 font-medium max-w-md mx-auto">This area will feature interactive graphs showing breed distribution over time.</p>
      </div>
    </div>
  );
}
