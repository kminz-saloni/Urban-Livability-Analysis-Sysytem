'use client'

import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { motion } from 'framer-motion'

interface City {
  rank: number
  city_name: string
  livability_score: number
  state: string
  tier: string
}

interface CityRankingChartProps {
  cities?: City[]
}

export default function CityRankingChart({ cities = [] }: CityRankingChartProps) {
  // Format data for chart
  const chartData = cities.map(city => ({
    name: city.city_name,
    score: city.livability_score,
    rank: city.rank,
    tier: city.tier
  }))

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white rounded-lg p-6 shadow-sm border border-border"
    >
      <div className="mb-6">
        <h2 className="text-lg font-heading font-bold text-primary">
          City Livability Rankings
        </h2>
        <p className="text-sm text-secondary mt-1">
          Top 10 cities by weighted livability score
        </p>
      </div>

      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#E8ECF1" />
          <XAxis 
            dataKey="name" 
            tick={{ fill: '#2B2B2B', fontSize: 12 }}
            angle={-45}
            textAnchor="end"
            height={80}
          />
          <YAxis 
            domain={[0, 100]}
            tick={{ fill: '#2B2B2B', fontSize: 12 }} 
          />
          <Tooltip
            contentStyle={{
              backgroundColor: '#fff',
              border: '1px solid #E8ECF1',
              borderRadius: '8px',
            }}
            formatter={(value: any) => [`${value.toFixed(1)}`, 'Livability Score']}
          />
          <Legend />
          <Bar 
            dataKey="score" 
            fill="#2F7E79" 
            radius={[8, 8, 0, 0]}
            name="Livability Score"
          />
        </BarChart>
      </ResponsiveContainer>

      {cities.length === 0 && (
        <div className="text-center py-8">
          <p className="text-secondary">No cities data available</p>
        </div>
      )}
    </motion.div>
  )
}
