'use client'

import { Bell, Search, User } from 'lucide-react'

export default function Header() {
  return (
    <header className="bg-white border-b border-border px-6 py-4 flex items-center justify-between shadow-sm">
      <div className="flex-1">
        <div className="relative max-w-md">
          <Search className="absolute left-3 top-3 text-secondary" size={20} />
          <input
            type="text"
            placeholder="Search cities, insights..."
            className="w-full pl-10 pr-4 py-2 rounded-lg border border-border focus:outline-none focus:ring-2 focus:ring-accent"
          />
        </div>
      </div>

      <div className="flex items-center gap-4">
        <button className="p-2 hover:bg-surface rounded-lg transition-colors">
          <Bell size={20} className="text-secondary" />
        </button>
        <div className="w-px h-6 bg-border" />
        <button className="flex items-center gap-2 px-4 py-2 hover:bg-surface rounded-lg transition-colors">
          <User size={20} className="text-secondary" />
          <span className="text-sm font-medium text-text">Admin</span>
        </button>
      </div>
    </header>
  )
}
