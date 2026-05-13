const API_BASE_URL = 'http://localhost:4000/api';

export async function getExpenses() {
  const response = await fetch(`${API_BASE_URL}/expenses`);
  return response.json();
}
