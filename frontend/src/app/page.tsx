'use client'

import { motion } from 'framer-motion'
import { BarChart3, MapPin, TrendingUp, Shield } from 'lucide-react'
import { useTopCities, useRankingStats, useInsights, useStressIndicators } from '@/hooks/useData'
import KPICard from '@/components/dashboard/KPICard'
import CityRankingChart from '@/components/dashboard/CityRankingChart'
import UrbanStressIndicators from '@/components/dashboard/UrbanStressIndicators'
import InsightsPanel from '@/components/dashboard/InsightsPanel'
import LoadingSpinner from '@/components/common/LoadingSpinner'

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
    },
  },
}

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.5 },
  },
}

export default function Dashboard() {
  const { data: topCities, loading: citiesLoading } = useTopCities(10)
  const { data: stats, loading: statsLoading } = useRankingStats()
  const { insights, loading: insightsLoading } = useInsights()
  const { tiers, loading: tiersLoading } = useStressIndicators()

  const isLoading = citiesLoading || statsLoading || insightsLoading || tiersLoading

  if (isLoading) {
    return <LoadingSpinner message="Loading urban livability data..." />
  }

  // Get best, worst, and stats from real data
  const bestCity = topCities[0] || null

  return (
    <motion.div
      className="space-y-6"
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      {/* Page Title */}
      <motion.div variants={itemVariants} className="mb-8">
        <h1 className="text-3xl font-heading font-bold text-primary">
          Urban Livability Intelligence
        </h1>
        <p className="text-secondary mt-2">
          National-level urban livability snapshot and analytics
        </p>
      </motion.div>

      {/* KPI Cards Row */}
      <motion.div
        variants={itemVariants}
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4"
      >
        <KPICard
          label="Avg Livability Score"
          value={stats?.mean_score.toFixed(1) ?? 'N/A'}
          icon={BarChart3}
          color="bg-blue-50"
          trend={`Range: ${stats?.min_score.toFixed(1)}-${stats?.max_score.toFixed(1)}`}
        />
        <KPICard
          label="Best City"
          value={bestCity?.city_name ?? 'Loading...'}
          icon={TrendingUp}
          color="bg-green-50"
          trend={`Score: ${bestCity?.livability_score.toFixed(1)}`}
        />
        <KPICard
          label="Rank #1"
          value={bestCity?.state ?? 'N/A'}
          icon={Shield}
          color="bg-purple-50"
          trend={`Tier: ${bestCity?.tier}`}
        />
        <KPICard
          label="Cities Analyzed"
          value="10"
          icon={MapPin}
          color="bg-cyan-50"
          trend={`Updated today`}
        />
        <KPICard
          label="Median Score"
          value={stats?.median_score.toFixed(1) ?? 'N/A'}
          icon={BarChart3}
          color="bg-orange-50"
          trend={`Std Dev: ${stats?.std_dev.toFixed(1)}`}
        />
      </motion.div>

      {/* Main Analytics Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* City Ranking Chart */}
        <motion.div variants={itemVariants} className="lg:col-span-2">
          <CityRankingChart cities={topCities} />
        </motion.div>

        {/* Urban Stress Indicators */}
        <motion.div variants={itemVariants}>
          <UrbanStressIndicators tiers={tiers} />
        </motion.div>
      </div>

      {/* Insights Panel */}
      <motion.div variants={itemVariants}>
        <InsightsPanel insights={insights} />
      </motion.div>
    </motion.div>
  )
}
