'use client'

import { useEffect, useState } from 'react'
import { api } from '@/lib/api'

interface City {
  rank: number
  city_name: string
  state: string
  livability_score: number
  percentile: number
  tier: string
  category_scores?: Record<string, number>
  raw_metrics?: Record<string, number>
}

interface RankingStats {
  mean_score: number
  median_score: number
  std_dev: number
  min_score: number
  max_score: number
}

interface Insight {
  title: string
  description: string
  type: string
  confidence: number
}

interface TierStats {
  tier: string
  count: number
  avgScore: number
  stressLevel: 'low' | 'medium' | 'high'
}

/**
 * Hook to fetch all rankings
 */
export function useRankings(limit?: number) {
  const [data, setData] = useState<City[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchRankings = async () => {
      try {
        setLoading(true)
        const response = await api.getRankings()
        setData(response.data)
      } catch (err: any) {
        setError(err.message || 'Failed to fetch rankings')
      } finally {
        setLoading(false)
      }
    }

    fetchRankings()
  }, [])

  return { data, loading, error }
}

/**
 * Hook to fetch top cities
 */
export function useTopCities(limit: number = 10) {
  const [data, setData] = useState<City[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchTopCities = async () => {
      try {
        setLoading(true)
        const response = await api.getTopCities(limit)
        setData(response.data)
      } catch (err: any) {
        setError(err.message || 'Failed to fetch top cities')
      } finally {
        setLoading(false)
      }
    }

    fetchTopCities()
  }, [limit])

  return { data, loading, error }
}

/**
 * Hook to fetch bottom cities
 */
export function useBottomCities(limit: number = 10) {
  const [data, setData] = useState<City[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchBottomCities = async () => {
      try {
        setLoading(true)
        const response = await api.getBottomCities(limit)
        setData(response.data)
      } catch (err: any) {
        setError(err.message || 'Failed to fetch bottom cities')
      } finally {
        setLoading(false)
      }
    }

    fetchBottomCities()
  }, [limit])

  return { data, loading, error }
}

/**
 * Hook to fetch ranking statistics
 */
export function useRankingStats() {
  const [data, setData] = useState<RankingStats | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchStats = async () => {
      try {
        setLoading(true)
        const response = await api.getRankingStats?.()
        setData(response?.data)
      } catch (err: any) {
        setError(err.message || 'Failed to fetch statistics')
      } finally {
        setLoading(false)
      }
    }

    fetchStats()
  }, [])

  return { data, loading, error }
}

/**
 * Hook to fetch insights
 */
export function useInsights() {
  const [insights, setInsights] = useState<Insight[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchInsights = async () => {
      try {
        setLoading(true)
        const response = await api.getRankingInsights?.()
        setInsights(response?.data?.insights || [])
      } catch (err: any) {
        setError(err.message || 'Failed to fetch insights')
      } finally {
        setLoading(false)
      }
    }

    fetchInsights()
  }, [])

  return { insights, loading, error }
}

/**
 * Hook to fetch single city profile
 */
export function useCityProfile(cityName?: string) {
  const [data, setData] = useState<City | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!cityName) {
      setLoading(false)
      return
    }

    const fetchProfile = async () => {
      try {
        setLoading(true)
        const response = await api.getCityRanking(cityName)
        setData(response.data)
      } catch (err: any) {
        setError(err.message || 'Failed to fetch city profile')
      } finally {
        setLoading(false)
      }
    }

    fetchProfile()
  }, [cityName])

  return { data, loading, error }
}

/**
 * Hook to fetch cities by tier
 */
export function useCitiesByTier(tier: string) {
  const [data, setData] = useState<City[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchCitiesByTier = async () => {
      try {
        setLoading(true)
        const response = await api.getCitiesByTier?.(tier)
        setData(response?.data || [])
      } catch (err: any) {
        setError(err.message || 'Failed to fetch cities by tier')
      } finally {
        setLoading(false)
      }
    }

    fetchCitiesByTier()
  }, [tier])

  return { data, loading, error }
}

/**
 * Hook to fetch AQI analytics
 */
export function useAQIAnalytics() {
  const [data, setData] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchAQI = async () => {
      try {
        setLoading(true)
        const response = await api.getAQIAnalytics()
        setData(response.data)
      } catch (err: any) {
        setError(err.message || 'Failed to fetch AQI analytics')
      } finally {
        setLoading(false)
      }
    }

    fetchAQI()
  }, [])

  return { data, loading, error }
}

/**
 * Hook to fetch crime analytics
 */
export function useCrimeAnalytics() {
  const [data, setData] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchCrime = async () => {
      try {
        setLoading(true)
        const response = await api.getCrimeAnalytics()
        setData(response.data)
      } catch (err: any) {
        setError(err.message || 'Failed to fetch crime analytics')
      } finally {
        setLoading(false)
      }
    }

    fetchCrime()
  }, [])

  return { data, loading, error }
}

/**
 * Hook to fetch water analytics
 */
export function useWaterAnalytics() {
  const [data, setData] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchWater = async () => {
      try {
        setLoading(true)
        const response = await api.getWaterAnalytics()
        setData(response.data)
      } catch (err: any) {
        setError(err.message || 'Failed to fetch water analytics')
      } finally {
        setLoading(false)
      }
    }

    fetchWater()
  }, [])

  return { data, loading, error }
}

/**
 * Hook to fetch traffic analytics
 */
export function useTrafficAnalytics() {
  const [data, setData] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchTraffic = async () => {
      try {
        setLoading(true)
        const response = await api.getTrafficAnalytics()
        setData(response.data)
      } catch (err: any) {
        setError(err.message || 'Failed to fetch traffic analytics')
      } finally {
        setLoading(false)
      }
    }

    fetchTraffic()
  }, [])

  return { data, loading, error }
}

/**
 * Hook to fetch stress indicators by tier
 */
export function useStressIndicators() {
  const [tiers, setTiers] = useState<TierStats[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchStressData = async () => {
      try {
        setLoading(true)
        // Fetch all cities and process by tier
        const response = await api.getRankings()
        const cities = response.data as City[]

        // Group by tier and calculate stats
        const tierMap: Record<string, { count: number; totalScore: number; scores: number[] }> = {}

        cities.forEach((city) => {
          if (!tierMap[city.tier]) {
            tierMap[city.tier] = { count: 0, totalScore: 0, scores: [] }
          }
          tierMap[city.tier].count += 1
          tierMap[city.tier].totalScore += city.livability_score
          tierMap[city.tier].scores.push(city.livability_score)
        })

        // Convert to tier stats with stress levels
        const tierStats: TierStats[] = Object.entries(tierMap)
          .map(([tier, stats]) => {
            const avgScore = stats.totalScore / stats.count
            let stressLevel: 'low' | 'medium' | 'high' = 'medium'
            if (avgScore >= 70) stressLevel = 'low'
            else if (avgScore < 60) stressLevel = 'high'

            return {
              tier,
              count: stats.count,
              avgScore,
              stressLevel,
            }
          })
          .sort((a, b) => {
            const tierOrder = { 'Tier-1': 1, 'Tier-2': 2, 'Tier-3': 3 }
            return (tierOrder[a.tier as keyof typeof tierOrder] || 0) - (tierOrder[b.tier as keyof typeof tierOrder] || 0)
          })

        setTiers(tierStats)
      } catch (err: any) {
        setError(err.message || 'Failed to fetch stress indicators')
      } finally {
        setLoading(false)
      }
    }

    fetchStressData()
  }, [])

  return { tiers, loading, error }
}
