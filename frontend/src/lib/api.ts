import axios from 'axios'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// API methods
export const api = {
  // Rankings
  getRankings: () => apiClient.get('/api/rankings'),
  getTopCities: (limit: number = 10) =>
    apiClient.get(`/api/rankings/top?limit=${limit}`),
  getBottomCities: (limit: number = 10) =>
    apiClient.get(`/api/rankings/bottom?limit=${limit}`),
  getCityRanking: (cityName: string) =>
    apiClient.get(`/api/rankings/${cityName}`),
  getRankingStats: () => apiClient.get('/api/rankings/stats'),
  getRankingInsights: () => apiClient.get('/api/rankings/insights'),
  getCitiesByTier: (tier: string) => apiClient.get(`/api/rankings/by-tier/${tier}`),

  // Cities
  getCities: () => apiClient.get('/api/cities'),
  getCity: (cityId: number) => apiClient.get(`/api/cities/${cityId}`),

  // Analytics
  getAQIAnalytics: () => apiClient.get('/api/analytics/aqi'),
  getCrimeAnalytics: () => apiClient.get('/api/analytics/crime'),
  getWaterAnalytics: () => apiClient.get('/api/analytics/water'),
  getTrafficAnalytics: () => apiClient.get('/api/analytics/traffic'),
  getCorrelationMatrix: () => apiClient.get('/api/analytics/correlation'),
  getAnomalyReport: () => apiClient.get('/api/analytics/anomalies'),

  // Maps
  getLivabilityMapData: () => apiClient.get('/api/maps/livability'),
  getAQILayer: () => apiClient.get('/api/maps/aqi-layer'),
  getCrimeDensity: () => apiClient.get('/api/maps/crime-density'),
  getWaterStress: () => apiClient.get('/api/maps/water-stress'),

  // Reports
  getReportSummary: () => apiClient.get('/api/reports/summary'),
}

export default apiClient
