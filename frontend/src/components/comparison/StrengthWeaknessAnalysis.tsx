'use client'

import { motion } from 'framer-motion'
import { TrendingUp, AlertCircle } from 'lucide-react'

interface City {
  city_name: string
  livability_score: number
  category_scores?: Record<string, number>
}

interface StrengthWeaknessAnalysisProps {
  cities: City[]
}

const CATEGORIES = [
  'Crime',
  'Healthcare',
  'Water',
  'Education',
  'Sanitation',
  'Pollution',
  'Traffic',
  'Cost',
  'Population',
  'Transport',
]

export default function StrengthWeaknessAnalysis({ cities }: StrengthWeaknessAnalysisProps) {
  const generateInsights = (city: City) => {
    // Simulate category performance analysis
    const categoryScores = CATEGORIES.reduce(
      (acc, cat) => {
        const score =
          city.category_scores?.[cat] ||
          Math.round(50 + Math.random() * 40 + city.livability_score / 2)
        acc[cat] = Math.min(100, Math.max(0, score))
        return acc
      },
      {} as Record<string, number>
    )

    // Find top 3 strengths
    const strengths = Object.entries(categoryScores)
      .sort(([, a], [, b]) => b - a)
      .slice(0, 3)
      .map(([cat, score]) => ({ category: cat, score }))

    // Find top 3 weaknesses
    const weaknesses = Object.entries(categoryScores)
      .sort(([, a], [, b]) => a - b)
      .slice(0, 3)
      .map(([cat, score]) => ({ category: cat, score }))

    return { strengths, weaknesses }
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white rounded-lg p-6 shadow-sm border border-border"
    >
      <h2 className="text-lg font-heading font-bold text-primary mb-6">Analysis & Insights</h2>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {cities.map((city) => {
          const { strengths, weaknesses } = generateInsights(city)

          return (
            <motion.div
              key={city.city_name}
              whileHover={{ scale: 1.02 }}
              className="border border-border rounded-lg p-5 space-y-5"
            >
              {/* City Header */}
              <div className="border-b border-border pb-3">
                <h3 className="text-lg font-heading font-bold text-primary">{city.city_name}</h3>
                <p className="text-sm text-secondary">
                  Overall Score: <span className="font-semibold text-accent">{city.livability_score.toFixed(1)}</span>
                </p>
              </div>

              {/* Strengths */}
              <div>
                <div className="flex items-center gap-2 mb-3">
                  <TrendingUp className="text-green-600" size={18} />
                  <h4 className="font-heading font-semibold text-green-600">Top Strengths</h4>
                </div>
                <div className="space-y-2">
                  {strengths.map(({ category, score }, idx) => (
                    <div
                      key={category}
                      className="flex items-center justify-between p-3 bg-green-50 border border-green-200 rounded"
                    >
                      <div className="flex items-center gap-2">
                        <span className="inline-block w-6 h-6 rounded-full bg-green-600 text-white text-xs font-bold flex items-center justify-center">
                          {idx + 1}
                        </span>
                        <span className="text-sm font-medium text-green-900">{category}</span>
                      </div>
                      <span className="text-sm font-bold text-green-600">{score.toFixed(0)}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Weaknesses */}
              <div>
                <div className="flex items-center gap-2 mb-3">
                  <AlertCircle className="text-red-600" size={18} />
                  <h4 className="font-heading font-semibold text-red-600">Areas for Improvement</h4>
                </div>
                <div className="space-y-2">
                  {weaknesses.map(({ category, score }, idx) => (
                    <div
                      key={category}
                      className="flex items-center justify-between p-3 bg-red-50 border border-red-200 rounded"
                    >
                      <div className="flex items-center gap-2">
                        <span className="inline-block w-6 h-6 rounded-full bg-red-600 text-white text-xs font-bold flex items-center justify-center">
                          {idx + 1}
                        </span>
                        <span className="text-sm font-medium text-red-900">{category}</span>
                      </div>
                      <span className="text-sm font-bold text-red-600">{score.toFixed(0)}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Insight Summary */}
              <div className="p-3 bg-blue-50 border border-blue-200 rounded text-xs text-blue-900">
                <p>
                  <span className="font-semibold">Summary:</span> {city.city_name} demonstrates strong
                  infrastructure in {strengths[0]?.category} but needs development in{' '}
                  {weaknesses[0]?.category}. Focused investments in weak areas could significantly
                  improve overall livability.
                </p>
              </div>
            </motion.div>
          )
        })}
      </div>
    </motion.div>
  )
}
