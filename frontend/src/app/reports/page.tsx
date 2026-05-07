'use client'

import { useEffect, useMemo, useState } from 'react'
import { motion } from 'framer-motion'
import { Download, FileText, Calendar } from 'lucide-react'
import { api } from '@/lib/api'
import { useRankings } from '@/hooks/useData'
import LoadingSpinner from '@/components/common/LoadingSpinner'

type ReportSummary = {
  summary?: {
    cities: number
    top_city: string
    bottom_city: string
    avg_score: number
  }
}

type AnomalyGroup = {
  high_outliers?: { city_name: string; state: string; [key: string]: number | string }[]
}

export default function ReportsPage() {
  const apiBase = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
  const { data: allCities, loading: citiesLoading } = useRankings()
  const [summary, setSummary] = useState<ReportSummary | null>(null)
  const [anomalies, setAnomalies] = useState<Record<string, AnomalyGroup> | null>(null)
  const [selectedCities, setSelectedCities] = useState<string[]>([])
  const [loading, setLoading] = useState(true)
  const isLoading = loading || citiesLoading

  useEffect(() => {
    const fetchReports = async () => {
      try {
        const [summaryRes, anomalyRes] = await Promise.all([
          api.getReportSummary(),
          api.getAnomalyReport(),
        ])
        setSummary(summaryRes.data)
        setAnomalies(anomalyRes.data?.anomalies || null)
      } finally {
        setLoading(false)
      }
    }

    fetchReports()
  }, [])

  const compareUrl = useMemo(() => {
    const cityQuery = selectedCities.join(',')
    return `${apiBase}/api/reports/compare.pdf${cityQuery ? `?cities=${encodeURIComponent(cityQuery)}` : ''}`
  }, [apiBase, selectedCities])

  const reports = [
    {
      title: 'National Urban Livability Report',
      date: 'May 2026',
      type: 'PDF',
      href: `${apiBase}/api/reports/national.pdf`,
    },
    {
      title: 'City Ranking Analysis 2026',
      date: 'May 2026',
      type: 'CSV',
      href: `${apiBase}/api/reports/rankings.csv`,
    },
  ]

  return (
    <motion.div
      className="space-y-6"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
    >
      <div className="mb-8">
        <h1 className="text-3xl font-heading font-bold text-primary">
          Reports & Insights
        </h1>
        <p className="text-secondary mt-2">
          Download research reports and analytical summaries
        </p>
      </div>

      {/* Generate Report Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-gradient-to-r from-primary to-secondary rounded-lg p-6 text-white shadow-md"
      >
        <h2 className="text-xl font-heading font-bold mb-2">
          Generate Custom Report
        </h2>
        <p className="text-blue-100 mb-4">
          Create custom comparative reports for selected cities
        </p>
        <div className="flex flex-wrap items-center gap-3">
          <select
            multiple
            value={selectedCities}
            onChange={(event) => {
              const options = Array.from(event.target.selectedOptions)
              setSelectedCities(options.map((option) => option.value))
            }}
            disabled={isLoading}
            className="min-w-[240px] rounded-lg border border-white/30 bg-white/10 px-3 py-2 text-sm text-white"
          >
            {allCities.map((city) => (
              <option key={city.city_name} value={city.city_name} className="text-primary">
                {city.city_name}
              </option>
            ))}
          </select>
          <a
            href={compareUrl}
            className="px-6 py-2 bg-accent hover:bg-opacity-90 rounded-lg font-semibold transition-all"
          >
            Download Comparison PDF
          </a>
        </div>
      </motion.div>

      {isLoading && <LoadingSpinner message="Loading report summary..." />}

      {summary?.summary && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="grid grid-cols-1 md:grid-cols-4 gap-4"
        >
          <div className="bg-white rounded-lg p-4 shadow-sm border border-border">
            <p className="text-xs text-secondary">Cities Covered</p>
            <p className="text-xl font-semibold text-primary">{summary.summary.cities}</p>
          </div>
          <div className="bg-white rounded-lg p-4 shadow-sm border border-border">
            <p className="text-xs text-secondary">Top City</p>
            <p className="text-xl font-semibold text-primary">{summary.summary.top_city}</p>
          </div>
          <div className="bg-white rounded-lg p-4 shadow-sm border border-border">
            <p className="text-xs text-secondary">Bottom City</p>
            <p className="text-xl font-semibold text-primary">{summary.summary.bottom_city}</p>
          </div>
          <div className="bg-white rounded-lg p-4 shadow-sm border border-border">
            <p className="text-xs text-secondary">Average Score</p>
            <p className="text-xl font-semibold text-primary">{summary.summary.avg_score.toFixed(1)}</p>
          </div>
        </motion.div>
      )}

      {/* Reports List */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="space-y-3"
      >
        {reports.map((report, idx) => (
          <div
            key={idx}
            className="bg-white rounded-lg p-4 shadow-sm border border-border hover:shadow-md transition-shadow flex items-center justify-between"
          >
            <div className="flex items-center gap-4">
              <div className="p-3 bg-surface rounded-lg">
                <FileText size={20} className="text-accent" />
              </div>
              <div>
                <h3 className="font-heading font-semibold text-primary">
                  {report.title}
                </h3>
                <div className="flex items-center gap-4 mt-1 text-sm text-secondary">
                  <div className="flex items-center gap-1">
                    <Calendar size={14} />
                    {report.date}
                  </div>
                  <div>{report.type}</div>
                </div>
              </div>
            </div>
            <a
              href={report.href}
              className="p-2 hover:bg-surface rounded-lg transition-colors text-accent"
            >
              <Download size={20} />
            </a>
          </div>
        ))}
      </motion.div>

      {anomalies && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white rounded-lg p-6 shadow-sm border border-border"
        >
          <h2 className="text-lg font-heading font-bold text-primary mb-4">
            Anomaly Highlights
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
            {Object.entries(anomalies).slice(0, 3).map(([metric, data]) => (
              <div key={metric} className="rounded-lg border border-border p-4">
                <p className="text-xs text-secondary uppercase">{metric.replace('_', ' ')}</p>
                <p className="text-sm font-semibold text-primary mb-2">High Outliers</p>
                <ul className="space-y-1 text-xs text-secondary">
                  {(data.high_outliers || []).slice(0, 3).map((row) => (
                    <li key={`${row.city_name}-${row.state}`}>{row.city_name}, {row.state}</li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </motion.div>
      )}
    </motion.div>
  )
}
