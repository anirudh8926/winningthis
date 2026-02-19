'use client'

import { useEffect } from 'react'
import { ThemeProvider } from '@/components/theme-provider'

export function Providers({ children }: { children: React.ReactNode }) {
  useEffect(() => {
    // Initialize demo account on first load
    if (typeof window !== 'undefined') {
      const registered = localStorage.getItem('creditbridge_users')
      if (!registered) {
        // Set up demo account
        const demoUsers = ['demo@creditbridge.com']
        localStorage.setItem('creditbridge_users', JSON.stringify(demoUsers))
        localStorage.setItem('creditbridge_pwd_demo@creditbridge.com', 'demo123')
      }
    }
  }, [])

  return (
    <ThemeProvider attribute="class" defaultTheme="light" enableSystem>
      {children}
    </ThemeProvider>
  )
}
