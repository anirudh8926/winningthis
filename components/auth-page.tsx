"use client"

import { useState } from "react"
import { useAppState } from "@/lib/app-context"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

// Demo credentials for testing
const DEMO_USERS = {
  "user@example.com": "password123",
  "demo@creditbridge.com": "demo123",
  "test@test.com": "test123",
}

export function AuthPage() {
  const { setCurrentPage, setIsLoggedIn, setUserName } = useAppState()
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [isSignUp, setIsSignUp] = useState(false)
  const [error, setError] = useState("")
  const [isLoading, setIsLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError("")
    setIsLoading(true)

    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, 500))

    if (isSignUp) {
      // For sign up, just validate email format
      if (!email.includes("@")) {
        setError("Please enter a valid email address")
        setIsLoading(false)
        return
      }
      if (password.length < 6) {
        setError("Password must be at least 6 characters")
        setIsLoading(false)
        return
      }
      const name = email.split("@")[0] || "User"
      setUserName(name.charAt(0).toUpperCase() + name.slice(1))
      setIsLoggedIn(true)
      setCurrentPage("profile-select")
    } else {
      // For login, validate against demo users
      const isValidCredentials = DEMO_USERS[email as keyof typeof DEMO_USERS] === password
      
      if (!isValidCredentials) {
        setError("Invalid email or password")
        setIsLoading(false)
        return
      }

      const name = email.split("@")[0] || "User"
      setUserName(name.charAt(0).toUpperCase() + name.slice(1))
      setIsLoggedIn(true)
      setCurrentPage("profile-select")
    }
  }

  return (
    <main className="flex min-h-screen items-center justify-center px-4 pt-20">
      <div className="w-full max-w-md">
        <div className="rounded-2xl border border-border bg-card p-8 shadow-sm">
          <div className="mb-8 text-center">
            <h1 className="font-serif text-3xl font-bold text-foreground">
              {isSignUp ? "Create Account" : "Welcome back"}
            </h1>
            <p className="mt-2 text-sm text-muted-foreground">
              {isSignUp
                ? "Sign up to discover your alternative credit score"
                : "Sign in to access your credit dashboard"}
            </p>
          </div>

          {error && (
            <div className="mb-4 rounded-lg bg-red-50 p-3 text-sm text-red-700 border border-red-200">
              {error}
            </div>
          )}

          {!isSignUp && (
            <div className="mb-4 rounded-lg bg-blue-50 p-3 text-xs text-blue-700 border border-blue-200">
              <p className="font-medium mb-2">Demo credentials:</p>
              <p>user@example.com / password123</p>
              <p>demo@creditbridge.com / demo123</p>
            </div>
          )}

          <form onSubmit={handleSubmit} className="flex flex-col gap-5">
            <div className="flex flex-col gap-2">
              <Label htmlFor="email" className="text-sm font-medium text-foreground">
                Email
              </Label>
              <Input
                id="email"
                type="email"
                placeholder="you@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className="rounded-lg border-border bg-background px-4 py-3"
              />
            </div>

            <div className="flex flex-col gap-2">
              <Label htmlFor="password" className="text-sm font-medium text-foreground">
                Password
              </Label>
              <Input
                id="password"
                type="password"
                placeholder="Enter your password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="rounded-lg border-border bg-background px-4 py-3"
              />
            </div>

            <Button
              type="submit"
              size="lg"
              disabled={isLoading}
              className="mt-2 w-full rounded-full bg-foreground py-6 text-base font-medium text-background hover:bg-foreground/90 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? "Verifying..." : "Continue"}
            </Button>
          </form>

          <p className="mt-6 text-center text-sm text-muted-foreground">
            {isSignUp ? "Already have an account?" : "Don't have an account?"}{" "}
            <button
              onClick={() => setIsSignUp(!isSignUp)}
              className="font-medium text-foreground underline underline-offset-4 hover:text-foreground/80"
            >
              {isSignUp ? "Sign in" : "Sign up"}
            </button>
          </p>
        </div>
      </div>
    </main>
  )
}
