'use client'

import { motion } from 'framer-motion'
import { AlertCircle, Shield, TrendingUp } from 'lucide-react'

interface TierData {
  tier: string
  count: number
  avgScore: number
  stressLevel: 'low' | 'medium' | 'high'
}

interface UrbanStressIndicatorsProps {
  tiers?: TierData[]
}

const defaultTiers: TierData[] = [
  {
    tier: 'Tier-1',
    count: 3,
    avgScore: 62.45,
    stressLevel: 'high',
  },
  {
    tier: 'Tier-2',
    count: 4,
    avgScore: 67.32,
    stressLevel: 'medium',
  },
  {
    tier: 'Tier-3',
    count: 3,
    avgScore: 61.20,
    stressLevel: 'high',
  },
]

function StressMeter({ level, score }: { level: 'low' | 'medium' | 'high'; score: number }) {
  const colors = {
    low: 'bg-green-500',
    medium: 'bg-yellow-500',
    high: 'bg-red-500',
  }

  return (
    <div className="flex items-center gap-3">
      <div className="flex-1">
        <div className="w-full bg-gray-200 rounded-full h-2">
          <motion.div
            initial={{ width: 0 }}
            animate={{ width: `${score}%` }}
            transition={{ duration: 1, ease: 'easeOut' }}
            className={`h-2 rounded-full ${colors[level]}`}
          />
        </div>
      </div>
      <span className="text-sm font-semibold text-gray-700 min-w-max">{score.toFixed(1)}</span>
    </div>
  )
}

function TierCard({ tier, count, avgScore, stressLevel }: TierData) {
  const getTierColor = (tier: string) => {
    switch (tier) {
      case 'Tier-1':
        return 'border-blue-200 bg-blue-50'
      case 'Tier-2':
        return 'border-purple-200 bg-purple-50'
      case 'Tier-3':
        return 'border-orange-200 bg-orange-50'
      default:
        return 'border-gray-200 bg-gray-50'
    }
  }

  const getStressIcon = (level: string) => {
    switch (level) {
      case 'low':
        return <Shield className="text-green-600" size={20} />
      case 'medium':
        return <AlertCircle className="text-yellow-600" size={20} />
      case 'high':
        return <TrendingUp className="text-red-600" size={20} />
      default:
        return <AlertCircle size={20} />
    }
  }

  return (
    <motion.div
      whileHover={{ scale: 1.02 }}
      className={`${getTierColor(tier)} border rounded-lg p-5 transition-all`}
    >
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1">
          <h4 className="font-heading font-bold text-primary mb-1">{tier}</h4>
          <p className="text-sm text-gray-600">{count} cities</p>
        </div>
        {getStressIcon(stressLevel)}
      </div>

      <div className="space-y-2">
        <div className="text-xs font-semibold text-gray-700 mb-2">Avg Score: {avgScore.toFixed(1)}</div>
        <StressMeter level={stressLevel} score={avgScore} />
      </div>
    </motion.div>
  )
}

export default function UrbanStressIndicators({ tiers = defaultTiers }: UrbanStressIndicatorsProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white rounded-lg p-6 shadow-sm border border-border"
    >
      <h2 className="text-lg font-heading font-bold text-primary mb-6">Urban Stress Index by Tier</h2>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {tiers.map((tier) => (
          <TierCard
            key={tier.tier}
            tier={tier.tier}
            count={tier.count}
            avgScore={tier.avgScore}
            stressLevel={tier.stressLevel}
          />
        ))}
      </div>

      <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
        <p className="text-sm text-blue-900">
          <span className="font-semibold">📊 Research Finding:</span> Tier-2 cities demonstrate superior
          livability scores with lower stress levels compared to traditional Tier-1 metros, suggesting
          more balanced infrastructure development and quality of life.
        </p>
      </div>
    </motion.div>
  )
}
