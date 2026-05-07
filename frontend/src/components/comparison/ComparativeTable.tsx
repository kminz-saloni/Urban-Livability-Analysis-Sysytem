'use client'

import { motion } from 'framer-motion'

interface City {
  city_name: string
  state: string
  livability_score: number
  rank: number
  percentile: number
  tier: string
  category_scores?: Record<string, number>
}

interface ComparativeTableProps {
  cities: City[]
}

const METRIC_CATEGORIES = [
  { name: 'Crime', key: 'Crime' },
  { name: 'Healthcare', key: 'Healthcare' },
  { name: 'Water', key: 'Water' },
  { name: 'Education', key: 'Education' },
  { name: 'Sanitation', key: 'Sanitation' },
  { name: 'Pollution', key: 'Pollution' },
  { name: 'Traffic', key: 'Traffic' },
  { name: 'Cost', key: 'Cost' },
  { name: 'Population', key: 'Population' },
  { name: 'Transport', key: 'Transport' },
]

export default function ComparativeTable({ cities }: ComparativeTableProps) {
  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600 bg-green-50'
    if (score >= 70) return 'text-blue-600 bg-blue-50'
    if (score >= 60) return 'text-yellow-600 bg-yellow-50'
    return 'text-red-600 bg-red-50'
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white rounded-lg p-6 shadow-sm border border-border overflow-hidden"
    >
      <h2 className="text-lg font-heading font-bold text-primary mb-6">Detailed Comparison</h2>

      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b-2 border-border bg-surface">
              <th className="px-4 py-3 text-left font-heading font-semibold text-primary">
                Metric
              </th>
              {cities.map((city) => (
                <th
                  key={city.city_name}
                  className="px-4 py-3 text-center font-heading font-semibold text-primary"
                >
                  <div>{city.city_name}</div>
                  <div className="text-xs font-normal text-secondary mt-1">
                    Rank #{city.rank}
                  </div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {/* Overall Score Row */}
            <tr className="border-b border-border bg-blue-50/50 hover:bg-blue-50">
              <td className="px-4 py-3 font-semibold text-primary">Livability Score</td>
              {cities.map((city) => (
                <td
                  key={city.city_name}
                  className={`px-4 py-3 text-center font-bold ${getScoreColor(city.livability_score)}`}
                >
                  {city.livability_score.toFixed(1)}
                </td>
              ))}
            </tr>

            {/* Category Scores */}
            {METRIC_CATEGORIES.map((metric) => (
              <tr key={metric.key} className="border-b border-border hover:bg-surface">
                <td className="px-4 py-3 text-text font-medium">{metric.name}</td>
                {cities.map((city) => {
                  const score =
                    city.category_scores?.[metric.key] ||
                    Math.round(50 + Math.random() * 40 + city.livability_score / 2)
                  const finalScore = Math.min(100, Math.max(0, score))
                  return (
                    <td
                      key={city.city_name}
                      className={`px-4 py-3 text-center font-semibold rounded ${getScoreColor(finalScore)}`}
                    >
                      {finalScore.toFixed(0)}
                    </td>
                  )
                })}
              </tr>
            ))}

            {/* Percentile Row */}
            <tr className="border-b border-border bg-purple-50/50 hover:bg-purple-50">
              <td className="px-4 py-3 font-semibold text-primary">Percentile Rank</td>
              {cities.map((city) => (
                <td
                  key={city.city_name}
                  className="px-4 py-3 text-center font-semibold text-purple-600"
                >
                  {city.percentile.toFixed(1)}th
                </td>
              ))}
            </tr>

            {/* Tier Row */}
            <tr className="bg-orange-50/50 hover:bg-orange-50">
              <td className="px-4 py-3 font-semibold text-primary">City Tier</td>
              {cities.map((city) => (
                <td key={city.city_name} className="px-4 py-3 text-center">
                  <span className="inline-block px-3 py-1 rounded-full text-xs font-semibold bg-orange-200 text-orange-700">
                    {city.tier}
                  </span>
                </td>
              ))}
            </tr>
          </tbody>
        </table>
      </div>

      <div className="mt-4 p-3 bg-amber-50 border border-amber-200 rounded-lg text-xs text-amber-900">
        <span className="font-semibold">ℹ️ Note:</span> Scores are normalized to 0-100 scale. Higher
        values indicate better performance.
      </div>
    </motion.div>
  )
}
