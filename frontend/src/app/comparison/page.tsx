'use client'

import { useState, useMemo } from 'react'
import { motion } from 'framer-motion'
import { Plus, Trash2, TrendingUp, AlertCircle } from 'lucide-react'
import { useRankings } from '@/hooks/useData'
import LoadingSpinner from '@/components/common/LoadingSpinner'
import RadarComparison from '@/components/comparison/RadarComparison'
import ComparativeTable from '@/components/comparison/ComparativeTable'
import StrengthWeaknessAnalysis from '@/components/comparison/StrengthWeaknessAnalysis'

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { staggerChildren: 0.1 },
  },
}

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.5 } },
}

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

export default function ComparisonPage() {
  const { data: allCities, loading } = useRankings()
  const [selectedCities, setSelectedCities] = useState<City[]>([])
  const [searchInput, setSearchInput] = useState('')

  const filteredCities = useMemo(() => {
    if (!searchInput.trim()) return allCities
    return allCities.filter((city) =>
      city.city_name.toLowerCase().includes(searchInput.toLowerCase()) ||
      city.state.toLowerCase().includes(searchInput.toLowerCase())
    )
  }, [allCities, searchInput])

  const availableCities = useMemo(() => {
    return filteredCities.filter(
      (city) => !selectedCities.some((selected) => selected.city_name === city.city_name)
    )
  }, [filteredCities, selectedCities])

  const handleAddCity = (city: City) => {
    if (selectedCities.length < 5) {
      setSelectedCities([...selectedCities, city])
    }
  }

  const handleRemoveCity = (cityName: string) => {
    setSelectedCities(selectedCities.filter((city) => city.city_name !== cityName))
  }

  const handleClearAll = () => {
    setSelectedCities([])
  }

  if (loading) {
    return <LoadingSpinner message="Loading city data..." />
  }

  return (
    <motion.div
      className="space-y-6"
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      <motion.div variants={itemVariants} className="mb-8">
        <h1 className="text-3xl font-heading font-bold text-primary">City Comparison</h1>
        <p className="text-secondary mt-2">Compare up to 5 cities across livability dimensions</p>
      </motion.div>

      <motion.div
        variants={itemVariants}
        className="bg-white rounded-lg p-6 shadow-sm border border-border"
      >
        <h2 className="text-lg font-heading font-bold text-primary mb-4">Select Cities</h2>

        <div className="mb-4">
          <input
            type="text"
            placeholder="Search cities by name or state..."
            value={searchInput}
            onChange={(e) => setSearchInput(e.target.value)}
            className="w-full px-4 py-2 border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-accent"
          />
        </div>

        {selectedCities.length > 0 && (
          <div className="mb-6">
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-sm font-semibold text-text">
                Selected ({selectedCities.length}/5)
              </h3>
              {selectedCities.length > 0 && (
                <button
                  onClick={handleClearAll}
                  className="text-xs text-red-600 hover:text-red-700 font-medium"
                >
                  Clear All
                </button>
              )}
            </div>
            <div className="flex flex-wrap gap-2">
              {selectedCities.map((city) => (
                <div
                  key={city.city_name}
                  className="flex items-center gap-2 bg-accent/10 border border-accent px-3 py-2 rounded-lg"
                >
                  <span className="text-sm font-medium text-accent">{city.city_name}</span>
                  <button
                    onClick={() => handleRemoveCity(city.city_name)}
                    className="text-accent hover:text-red-600"
                  >
                    <Trash2 size={14} />
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}

        <div className="space-y-2 max-h-64 overflow-y-auto">
          {availableCities.length > 0 ? (
            availableCities.map((city) => (
              <motion.div
                key={city.city_name}
                whileHover={{ scale: 1.01 }}
                className="flex items-center justify-between p-3 border border-border rounded-lg hover:bg-surface cursor-pointer transition"
                onClick={() => selectedCities.length < 5 && handleAddCity(city)}
              >
                <div className="flex-1">
                  <p className="font-medium text-primary">{city.city_name}</p>
                  <p className="text-xs text-secondary">{city.state}</p>
                </div>
                <div className="flex items-center gap-3">
                  <div className="text-right">
                    <p className="font-bold text-accent">{city.livability_score.toFixed(1)}</p>
                    <p className="text-xs text-secondary">Rank #{city.rank}</p>
                  </div>
                  {selectedCities.length < 5 && (
                    <button className="text-accent hover:bg-accent/10 p-2 rounded">
                      <Plus size={18} />
                    </button>
                  )}
                </div>
              </motion.div>
            ))
          ) : (
            <p className="text-center text-secondary py-4">No cities found</p>
          )}
        </div>
      </motion.div>

      {selectedCities.length >= 2 && (
        <>
          <motion.div variants={itemVariants}>
            <RadarComparison cities={selectedCities} />
          </motion.div>

          <motion.div variants={itemVariants}>
            <ComparativeTable cities={selectedCities} />
          </motion.div>

          <motion.div variants={itemVariants}>
            <StrengthWeaknessAnalysis cities={selectedCities} />
          </motion.div>
        </>
      )}

      {selectedCities.length === 0 && (
        <motion.div
          variants={itemVariants}
          className="bg-blue-50 border border-blue-200 rounded-lg p-8 text-center"
        >
          <TrendingUp className="inline text-blue-600 mb-3" size={32} />
          <p className="text-blue-900 font-medium">
            Select 2-5 cities to start comparing
          </p>
        </motion.div>
      )}

      {selectedCities.length === 1 && (
        <motion.div
          variants={itemVariants}
          className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 flex items-center gap-3 text-yellow-900"
        >
          <AlertCircle size={20} />
          <p className="text-sm">Select at least one more city to enable comparison</p>
        </motion.div>
      )}
    </motion.div>
  )
}
