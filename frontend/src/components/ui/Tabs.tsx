'use client'

import React, { ReactNode, useState } from 'react'

interface TabsProps {
  children: ReactNode
  defaultValue?: string
  className?: string
}

interface TabsListProps {
  children: ReactNode
  className?: string
}

interface TabsTriggerProps {
  value: string
  children: ReactNode
}

interface TabsContentProps {
  value: string
  children: ReactNode
}

export function Tabs({ children, defaultValue = '', className = '' }: TabsProps) {
  const [activeTab, setActiveTab] = useState(defaultValue)

  return (
    <div className={className}>
      {Array.isArray(children)
        ? children.map((child) =>
            child?.type?.name === 'TabsList'
              ? React.cloneElement(child, { activeTab, setActiveTab })
              : child
          )
        : children}
      {Array.isArray(children)
        ? children.map((child) =>
            child?.type?.name === 'TabsContent'
              ? React.cloneElement(child, { activeTab })
              : null
          )
        : null}
    </div>
  )
}

export function TabsList({ children, className = '' }: TabsListProps) {
  return <div className={`flex gap-2 ${className}`}>{children}</div>
}

export function TabsTrigger({ value, children }: TabsTriggerProps) {
  return (
    <button
      data-value={value}
      onClick={(e) => {
        const target = e.currentTarget as HTMLButtonElement
        const value = target.getAttribute('data-value')
        const parent = target.closest('[data-tabs]') as any
        if (parent?.setActiveTab) parent.setActiveTab(value)
      }}
      className="px-4 py-2 rounded-lg font-medium text-secondary hover:bg-surface transition-colors data-active:bg-accent data-active:text-white"
    >
      {children}
    </button>
  )
}

export function TabsContent({ value, children, activeTab }: TabsContentProps & { activeTab?: string }) {
  if (value !== activeTab) return null
  return <div>{children}</div>
}
