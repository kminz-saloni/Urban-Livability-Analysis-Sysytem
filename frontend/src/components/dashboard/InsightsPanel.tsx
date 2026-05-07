'use client'

import { motion } from 'framer-motion'
import { Lightbulb, TrendingDown, AlertTriangle, CheckCircle } from 'lucide-react'

interface Insight {
  title: string
  description: string
  type: string
  confidence: number
}

interface InsightsPanelProps {
  insights?: Insight[]
}

function InsightCard({ title, description, type, confidence }: Insight) {
  const getIcon = (type: string) => {
    switch (type) {
      case 'positive':
        return <CheckCircle size={20} />
      case 'warning':
        return <AlertTriangle size={20} />
      case 'critical':
        return <TrendingDown size={20} />
      default:
        return <Lightbulb size={20} />
    }
  }

  const getTypeStyles = (type: string) => {
    switch (type) {
      case 'positive':
        return 'bg-green-50 border-green-200 text-green-700'
      case 'warning':
        return 'bg-yellow-50 border-yellow-200 text-yellow-700'
      case 'critical':
        return 'bg-red-50 border-red-200 text-red-700'
      default:
        return 'bg-blue-50 border-blue-200 text-blue-700'
    }
  }

  return (
    <motion.div
      whileHover={{ scale: 1.02 }}
      className={`${getTypeStyles(type)} border rounded-lg p-5`}
    >
      <div className="flex gap-3">
        <div className="flex-shrink-0 mt-1">{getIcon(type)}</div>
        <div className="flex-1">
          <h4 className="font-heading font-semibold text-sm mb-1">{title}</h4>
          <p className="text-sm opacity-90">{description}</p>
          <p className="text-xs mt-2 opacity-75">
            Confidence: {(confidence * 100).toFixed(0)}%
          </p>
        </div>
      </div>
    </motion.div>
  )
}

export default function InsightsPanel({ insights = [] }: InsightsPanelProps) {
  // Fallback insights if none provided
  const defaultInsights: Insight[] = [
    {
      title: 'Tier-2 City Outperformance',
      description:
        'Tier-2 cities like Kozhikode and Coimbatore outperform Tier-1 metros in balanced livability metrics.',
      type: 'positive',
      confidence: 0.85,
    },
    {
      title: 'Northern Pollution Burden',
      description:
        'Northern cities exhibit elevated pollution levels, significantly impacting livability scores.',
      type: 'critical',
      confidence: 0.90,
    },
    {
      title: 'Traffic Impact',
      description:
        'Traffic congestion strongly correlates with livability decline across metropolitan areas.',
      type: 'warning',
      confidence: 0.88,
    },
    {
      title: 'Balanced Urban Strategy',
      description:
        'Cities balancing infrastructure growth with environmental protection show superior livability.',
      type: 'positive',
      confidence: 0.82,
    },
  ]

  const displayInsights = insights.length > 0 ? insights : defaultInsights

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white rounded-lg p-6 shadow-sm border border-border"
    >
      <div className="flex items-center gap-2 mb-6">
        <Lightbulb className="text-accent" size={24} />
        <h2 className="text-lg font-heading font-bold text-primary">
          Research-Backed Insights
        </h2>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {displayInsights.map((insight, idx) => (
          <InsightCard
            key={idx}
            title={insight.title}
            description={insight.description}
            type={insight.type}
            confidence={insight.confidence}
          />
        ))}
      </div>
    </motion.div>
  )
}
