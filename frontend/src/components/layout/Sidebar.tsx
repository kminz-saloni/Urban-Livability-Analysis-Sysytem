'use client'

import Link from 'next/link'
import { MapPin, BarChart3, Map, FileText } from 'lucide-react'

export default function Sidebar() {
  const menuItems = [
    {
      label: 'Dashboard',
      href: '/',
      icon: BarChart3,
    },
    {
      label: 'City Comparison',
      href: '/comparison',
      icon: MapPin,
    },
    {
      label: 'Analytics',
      href: '/analytics',
      icon: BarChart3,
    },
    {
      label: 'Map Intelligence',
      href: '/map',
      icon: Map,
    },
    {
      label: 'Reports',
      href: '/reports',
      icon: FileText,
    },
  ]

  return (
    <aside className="w-64 bg-primary text-white flex flex-col border-r border-border">
      {/* Logo */}
      <div className="p-6 border-b border-opacity-10 border-white">
        <h1 className="text-2xl font-heading font-bold">UrbanPulse IQ</h1>
        <p className="text-xs text-blue-200 mt-1">Urban Intelligence Platform</p>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-4 py-6 space-y-2">
        {menuItems.map((item) => {
          const Icon = item.icon
          return (
            <Link
              key={item.label}
              href={item.href}
              className="flex items-center gap-3 px-4 py-3 rounded-lg text-blue-100 hover:bg-secondary transition-colors"
            >
              <Icon size={20} />
              <span className="font-medium">{item.label}</span>
            </Link>
          )
        })}
      </nav>
    </aside>
  )
}
