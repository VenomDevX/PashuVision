const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function predictBreed(file: File, speciesHint: string) {
  const formData = new FormData();
  formData.append('image', file);
  formData.append('species_hint', speciesHint);

  const response = await fetch(`${API_URL}/api/v1/predict/`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    throw new Error('Prediction failed');
  }

  return response.json();
}
