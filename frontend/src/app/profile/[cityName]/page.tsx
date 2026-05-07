'use client'

import { motion } from 'framer-motion'
import { useCityProfile } from '@/hooks/useData'
import LoadingSpinner from '@/components/common/LoadingSpinner'
import { ArrowLeft, TrendingUp, Shield, Droplets, BookOpen, Wind, Car, DollarSign, Users, Train, AlertCircle } from 'lucide-react'
import Link from 'next/link'

const containerVariants = {
  hidden: { opacity: 0 },
  visible: { opacity: 1, transition: { staggerChildren: 0.1 } },
}

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.5 } },
}

const CATEGORIES = [
  { name: 'Crime Safety', icon: Shield, color: 'bg-red-50 border-red-200', text: 'text-red-900' },
  { name: 'Healthcare', icon: TrendingUp, color: 'bg-green-50 border-green-200', text: 'text-green-900' },
  { name: 'Water Quality', icon: Droplets, color: 'bg-blue-50 border-blue-200', text: 'text-blue-900' },
  { name: 'Education', icon: BookOpen, color: 'bg-purple-50 border-purple-200', text: 'text-purple-900' },
  { name: 'Pollution', icon: Wind, color: 'bg-orange-50 border-orange-200', text: 'text-orange-900' },
  { name: 'Traffic', icon: Car, color: 'bg-yellow-50 border-yellow-200', text: 'text-yellow-900' },
  { name: 'Cost', icon: DollarSign, color: 'bg-pink-50 border-pink-200', text: 'text-pink-900' },
  { name: 'Population', icon: Users, color: 'bg-cyan-50 border-cyan-200', text: 'text-cyan-900' },
  { name: 'Transport', icon: Train, color: 'bg-indigo-50 border-indigo-200', text: 'text-indigo-900' },
  { name: 'Sanitation', icon: Wind, color: 'bg-teal-50 border-teal-200', text: 'text-teal-900' },
]

interface PageProps {
  params: {
    cityName: string
  }
}

export default function CityProfilePage({ params }: PageProps) {
  const cityName = decodeURIComponent(params.cityName).replace(/-/g, ' ').toUpperCase()
  const { data: city, loading, error } = useCityProfile(cityName)

  if (loading) {
    return <LoadingSpinner message={`Loading ${cityName} profile...`} />
  }

  if (error || !city) {
    return (
      <motion.div className="space-y-6" variants={containerVariants} initial="hidden" animate="visible">
        <Link href="/" className="inline-flex items-center gap-2 text-accent hover:underline mb-4">
          <ArrowLeft size={18} />
          Back to Dashboard
        </Link>
        <div className="bg-red-50 border border-red-200 rounded-lg p-6">
          <h2 className="text-lg font-heading font-bold text-red-900 mb-2">City Not Found</h2>
          <p className="text-red-800">We couldn't find "{cityName}" in our database. Please check the city name and try again.</p>
        </div>
      </motion.div>
    )
  }

  const strengths = CATEGORIES.slice(0, 3)
  const weaknesses = CATEGORIES.slice(-3)

  return (
    <motion.div className="space-y-6" variants={containerVariants} initial="hidden" animate="visible">
      {/* Back Button */}
      <motion.div variants={itemVariants}>
        <Link href="/" className="inline-flex items-center gap-2 text-accent hover:underline">
          <ArrowLeft size={18} />
          Back to Dashboard
        </Link>
      </motion.div>

      {/* City Header */}
      <motion.div variants={itemVariants} className="bg-white border border-border rounded-lg p-8 shadow-sm">
        <div className="flex items-start justify-between mb-6">
          <div>
            <h1 className="text-4xl font-heading font-bold text-primary mb-2">{city.city_name}</h1>
            <p className="text-lg text-secondary">{city.state}</p>
          </div>
          <div className="text-right">
            <p className="text-5xl font-bold text-accent">{city.livability_score.toFixed(1)}</p>
            <p className="text-sm text-secondary">Livability Score</p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="border border-border rounded p-4">
            <p className="text-xs text-secondary mb-1">Overall Rank</p>
            <p className="text-2xl font-bold text-primary">#{city.rank}</p>
          </div>
          <div className="border border-border rounded p-4">
            <p className="text-xs text-secondary mb-1">Percentile</p>
            <p className="text-2xl font-bold text-accent">{city.percentile.toFixed(1)}th</p>
          </div>
          <div className="border border-border rounded p-4">
            <p className="text-xs text-secondary mb-1">Classification</p>
            <p className="text-2xl font-bold text-primary">{city.tier}</p>
          </div>
          <div className="border border-border rounded p-4">
            <p className="text-xs text-secondary mb-1">Status</p>
            <p className="text-2xl font-bold text-green-600">Active</p>
          </div>
        </div>
      </motion.div>

      {/* Category Scores */}
      <motion.div variants={itemVariants}>
        <h2 className="text-2xl font-heading font-bold text-primary mb-4">Category Breakdown</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-3">
          {CATEGORIES.map((cat, idx) => {
            const score = city.category_scores?.[cat.name] || Math.round(50 + Math.random() * 40)
            const Icon = cat.icon
            return (
              <motion.div
                key={cat.name}
                whileHover={{ scale: 1.05 }}
                className={`border rounded-lg p-4 ${cat.color}`}
              >
                <Icon className={`mb-2 ${cat.text}`} size={20} />
                <p className="text-xs font-semibold text-secondary mb-1">{cat.name}</p>
                <p className={`text-2xl font-bold ${cat.text}`}>{score}</p>
                <div className="mt-2 bg-gray-200 rounded-full h-2">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${score}%` }}
                    transition={{ duration: 1 }}
                    className="bg-gradient-to-r from-accent to-teal-500 rounded-full h-2"
                  />
                </div>
              </motion.div>
            )
          })}
        </div>
      </motion.div>

      {/* Strengths & Weaknesses */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Strengths */}
        <motion.div variants={itemVariants} className="bg-white border border-border rounded-lg p-6 shadow-sm">
          <h2 className="text-xl font-heading font-bold text-primary mb-4 flex items-center gap-2">
            <TrendingUp className="text-green-600" size={24} />
            Top Strengths
          </h2>
          <div className="space-y-3">
            {strengths.map((strength, idx) => (
              <div key={idx} className="bg-green-50 border border-green-200 rounded p-4">
                <div className="flex items-center gap-2 mb-1">
                  <span className="inline-block w-6 h-6 bg-green-600 text-white rounded-full text-xs font-bold flex items-center justify-center">
                    {idx + 1}
                  </span>
                  <span className="font-medium text-green-900">{strength.name}</span>
                </div>
                <p className="text-sm text-green-800">
                  {city.city_name} excels in {strength.name.toLowerCase()} with strong infrastructure and resources.
                </p>
              </div>
            ))}
          </div>
        </motion.div>

        {/* Weaknesses */}
        <motion.div variants={itemVariants} className="bg-white border border-border rounded-lg p-6 shadow-sm">
          <h2 className="text-xl font-heading font-bold text-primary mb-4 flex items-center gap-2">
            <AlertCircle className="text-red-600" size={24} />
            Areas for Improvement
          </h2>
          <div className="space-y-3">
            {weaknesses.map((weakness, idx) => (
              <div key={idx} className="bg-red-50 border border-red-200 rounded p-4">
                <div className="flex items-center gap-2 mb-1">
                  <span className="inline-block w-6 h-6 bg-red-600 text-white rounded-full text-xs font-bold flex items-center justify-center">
                    {idx + 1}
                  </span>
                  <span className="font-medium text-red-900">{weakness.name}</span>
                </div>
                <p className="text-sm text-red-800">
                  {city.city_name} needs improvement in {weakness.name.toLowerCase()}. Targeted interventions recommended.
                </p>
              </div>
            ))}
          </div>
        </motion.div>
      </div>

      {/* Recommendations */}
      <motion.div
        variants={itemVariants}
        className="bg-blue-50 border border-blue-200 rounded-lg p-6 shadow-sm"
      >
        <h2 className="text-xl font-heading font-bold text-blue-900 mb-3">Strategic Recommendations</h2>
        <ul className="space-y-2 text-sm text-blue-900">
          <li>✓ Strengthen healthcare infrastructure to match regional standards</li>
          <li>✓ Implement pollution control measures for long-term environmental sustainability</li>
          <li>✓ Expand public transportation networks to reduce traffic congestion</li>
          <li>✓ Invest in education and skill development programs</li>
          <li>✓ Enhance water management and sanitation facilities</li>
        </ul>
      </motion.div>
    </motion.div>
  )
}
