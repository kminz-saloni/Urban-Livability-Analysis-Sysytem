'use client'

import { motion } from 'framer-motion'
import { LucideIcon } from 'lucide-react'

interface KPICardProps {
  label: string
  value: string
  icon: LucideIcon
  color: string
  trend: string
}

export default function KPICard({
  label,
  value,
  icon: Icon,
  color,
  trend,
}: KPICardProps) {
  return (
    <motion.div
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
      className={`${color} border border-border rounded-lg p-5 shadow-sm hover:shadow-md transition-shadow cursor-pointer`}
    >
      <div className="flex items-start justify-between mb-3">
        <h3 className="text-sm font-medium text-secondary">{label}</h3>
        <Icon size={20} className="text-accent" />
      </div>
      <div className="space-y-2">
        <p className="text-2xl font-heading font-bold text-primary">{value}</p>
        <p className="text-xs text-secondary">{trend}</p>
      </div>
    </motion.div>
  )
}
