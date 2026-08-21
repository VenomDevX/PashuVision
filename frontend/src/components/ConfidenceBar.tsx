export default function ConfidenceBar({ label, value }: { label: string, value: number }) {
  const color = value > 80 ? 'bg-green-500' : value > 50 ? 'bg-yellow-500' : 'bg-red-500';
  
  return (
    <div className="mb-4">
      <div className="flex justify-between items-center mb-1">
        <span className="text-sm font-medium text-gray-700">{label}</span>
        <span className="text-sm font-bold text-gray-900">{value.toFixed(1)}%</span>
      </div>
      <div className="w-full bg-gray-200 rounded-full h-2.5">
        <div className={`h-2.5 rounded-full ${color}`} style={{ width: `${value}%` }}></div>
      </div>
    </div>
  );
}
