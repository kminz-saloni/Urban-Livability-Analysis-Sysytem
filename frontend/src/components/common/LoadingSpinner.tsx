'use client'

import { motion } from 'framer-motion'

interface LoadingSpinnerProps {
  message?: string
  fullHeight?: boolean
}

export default function LoadingSpinner({
  message = 'Loading...',
  fullHeight = true,
}: LoadingSpinnerProps) {
  return (
    <div className={`flex items-center justify-center ${fullHeight ? 'h-screen' : 'h-40'}`}>
      <motion.div className="text-center">
        <motion.div
          className="w-12 h-12 mx-auto mb-4 rounded-full border-4 border-border border-t-accent"
          animate={{ rotate: 360 }}
          transition={{ duration: 1, repeat: Infinity }}
        />
        <p className="text-secondary font-medium">{message}</p>
      </motion.div>
    </div>
  )
}
