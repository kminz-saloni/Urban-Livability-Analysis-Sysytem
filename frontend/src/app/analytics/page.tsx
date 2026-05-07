'use client'

import { motion } from 'framer-motion'
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/Tabs'

const aqiData = [
  { city: 'Patna', pm25: 250, aqi: 'Severe' },
  { city: 'Delhi', pm25: 180, aqi: 'Very Poor' },
  { city: 'Bengaluru', pm25: 90, aqi: 'Moderate' },
]

const crimeData = [
  { month: 'Jan', cases: 45 },
  { month: 'Feb', cases: 52 },
  { month: 'Mar', cases: 48 },
  { month: 'Apr', cases: 61 },
  { month: 'May', cases: 55 },
]

export default function AnalyticsPage() {
  return (
    <motion.div
      className="space-y-6"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
    >
      <div className="mb-8">
        <h1 className="text-3xl font-heading font-bold text-primary">
          EDA Analytics
        </h1>
        <p className="text-secondary mt-2">
          Research-backed urban analytics and insights
        </p>
      </div>

      <Tabs defaultValue="aqi" className="space-y-6">
        <TabsList className="bg-white border border-border p-1 rounded-lg">
          <TabsTrigger value="aqi">AQI & Pollution</TabsTrigger>
          <TabsTrigger value="crime">Crime Analytics</TabsTrigger>
          <TabsTrigger value="water">Water Intelligence</TabsTrigger>
          <TabsTrigger value="traffic">Traffic Analytics</TabsTrigger>
        </TabsList>

        <TabsContent value="aqi">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white rounded-lg p-6 shadow-sm border border-border"
          >
            <h2 className="text-lg font-heading font-bold text-primary mb-4">
              PM2.5 Levels Across Cities
            </h2>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-border">
                    <th className="text-left px-4 py-3 font-heading font-semibold text-primary">
                      City
                    </th>
                    <th className="text-left px-4 py-3 font-heading font-semibold text-primary">
                      PM2.5 (μg/m³)
                    </th>
                    <th className="text-left px-4 py-3 font-heading font-semibold text-primary">
                      Status
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {aqiData.map((row) => (
                    <tr key={row.city} className="border-b border-border hover:bg-surface">
                      <td className="px-4 py-3 text-sm font-medium text-text">
                        {row.city}
                      </td>
                      <td className="px-4 py-3 text-sm font-semibold text-accent">
                        {row.pm25}
                      </td>
                      <td className="px-4 py-3 text-sm">
                        <span
                          className={`inline-block px-3 py-1 rounded-full text-xs font-semibold ${
                            row.aqi === 'Severe'
                              ? 'bg-red-100 text-red-700'
                              : row.aqi === 'Very Poor'
                                ? 'bg-orange-100 text-orange-700'
                                : 'bg-yellow-100 text-yellow-700'
                          }`}
                        >
                          {row.aqi}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </motion.div>
        </TabsContent>

        <TabsContent value="crime">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white rounded-lg p-6 shadow-sm border border-border"
          >
            <h2 className="text-lg font-heading font-bold text-primary mb-4">
              Crime Trend Analysis
            </h2>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={crimeData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#E8ECF1" />
                <XAxis dataKey="month" tick={{ fill: '#2B2B2B', fontSize: 12 }} />
                <YAxis tick={{ fill: '#2B2B2B', fontSize: 12 }} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#fff',
                    border: '1px solid #E8ECF1',
                    borderRadius: '8px',
                  }}
                />
                <Legend />
                <Line
                  type="monotone"
                  dataKey="cases"
                  stroke="#2F7E79"
                  strokeWidth={2}
                  dot={{ fill: '#2F7E79' }}
                />
              </LineChart>
            </ResponsiveContainer>
          </motion.div>
        </TabsContent>

        <TabsContent value="water">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white rounded-lg p-6 shadow-sm border border-border"
          >
            <h2 className="text-lg font-heading font-bold text-primary mb-4">
              Water Stress Analysis
            </h2>
            <p className="text-secondary">
              Groundwater depletion, contamination overlays, and water complaint density analysis coming soon.
            </p>
          </motion.div>
        </TabsContent>

        <TabsContent value="traffic">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white rounded-lg p-6 shadow-sm border border-border"
          >
            <h2 className="text-lg font-heading font-bold text-primary mb-4">
              Traffic Intelligence
            </h2>
            <p className="text-secondary">
              Congestion severity, peak-hour stress, and infrastructure bottleneck maps coming soon.
            </p>
          </motion.div>
        </TabsContent>
      </Tabs>
    </motion.div>
  )
}
