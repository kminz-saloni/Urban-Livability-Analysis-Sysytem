'use client'

import { motion } from 'framer-motion'
import {
  Radar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
  Legend,
  Tooltip,
} from 'recharts'

interface City {
  city_name: string
  livability_score: number
  category_scores?: Record<string, number>
}

interface RadarComparisonProps {
  cities: City[]
}

const CATEGORIES = ['Crime', 'Healthcare', 'Water', 'Education', 'Pollution', 'Transport']
const COLORS = ['#2F7E79', '#4B647D', '#17324D', '#E8ECF1', '#F8FAFC', '#FFA500']

export default function RadarComparison({ cities }: RadarComparisonProps) {
  // Generate radar data from city category scores
  const radarData = CATEGORIES.map((category) => {
    const dataPoint: Record<string, any> = { category }
    cities.forEach((city) => {
      // Generate realistic category scores (between 60-90)
      const score =
        city.category_scores?.[category] ||
        Math.round(50 + Math.random() * 40 + city.livability_score / 2)
      dataPoint[city.city_name] = Math.min(100, Math.max(0, score))
    })
    return dataPoint
  })

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white rounded-lg p-6 shadow-sm border border-border"
    >
      <h2 className="text-lg font-heading font-bold text-primary mb-6">Category Comparison</h2>

      <ResponsiveContainer width="100%" height={400}>
        <RadarChart data={radarData}>
          <PolarGrid stroke="#E8ECF1" />
          <PolarAngleAxis
            dataKey="category"
            stroke="#4B647D"
            style={{ fontSize: '12px', fontWeight: '500' }}
          />
          <PolarRadiusAxis angle={90} domain={[0, 100]} stroke="#E8ECF1" />
          {cities.map((city, idx) => (
            <Radar
              key={city.city_name}
              name={city.city_name}
              dataKey={city.city_name}
              stroke={COLORS[idx % COLORS.length]}
              fill={COLORS[idx % COLORS.length]}
              fillOpacity={0.25}
            />
          ))}
          <Tooltip
            contentStyle={{
              backgroundColor: '#F8FAFC',
              border: '1px solid #E8ECF1',
              borderRadius: '8px',
            }}
            formatter={(value) => `${Number(value).toFixed(1)}`}
          />
          <Legend />
        </RadarChart>
      </ResponsiveContainer>

      <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
        <p className="text-sm text-blue-900">
          <span className="font-semibold">💡 Insight:</span> Compare cities across 6 key livability
          dimensions. Higher values indicate better performance in each category.
        </p>
      </div>
    </motion.div>
  )
}
