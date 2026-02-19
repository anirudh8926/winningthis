"use client"

import { useState, useEffect } from "react"
import { useAppState } from "@/lib/app-context"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

export function AuthPage() {
  const { setCurrentPage, setIsLoggedIn, setUserName, setIsNewUser } = useAppState()
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [isSignUp, setIsSignUp] = useState(false)
  const [error, setError] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [registeredUsers, setRegisteredUsers] = useState<Set<string>>(new Set())

  // Load registered users from localStorage on mount
  useEffect(() => {
    if (typeof window !== "undefined") {
      const stored = localStorage.getItem("creditbridge_users")
      if (stored) {
        setRegisteredUsers(new Set(JSON.parse(stored)))
      }
    }
  }, [])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError("")
    setIsLoading(true)

    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, 500))

    // Validate email format
    if (!email.includes("@")) {
      setError("Please enter a valid email address")
      setIsLoading(false)
      return
    }

    if (isSignUp) {
      // Sign up - new user flow
      if (registeredUsers.has(email)) {
        setError("Email already registered. Please sign in instead.")
        setIsLoading(false)
        return
      }
      if (password.length < 6) {
        setError("Password must be at least 6 characters")
        setIsLoading(false)
        return
      }
      
      // Register the user
      const updatedUsers = new Set(registeredUsers)
      updatedUsers.add(email)
      setRegisteredUsers(updatedUsers)
      if (typeof window !== "undefined") {
        localStorage.setItem("creditbridge_users", JSON.stringify(Array.from(updatedUsers)))
        localStorage.setItem(`creditbridge_pwd_${email}`, password)
      }

      const name = email.split("@")[0] || "User"
      setUserName(name.charAt(0).toUpperCase() + name.slice(1))
      setIsLoggedIn(true)
      setIsNewUser(true)
      setCurrentPage("profile-select")
    } else {
      // Login - returning user flow
      if (!registeredUsers.has(email)) {
        setError("Email not found. Please sign up first.")
        setIsLoading(false)
        return
      }

      // Verify password
      if (typeof window !== "undefined") {
        const storedPassword = localStorage.getItem(`creditbridge_pwd_${email}`)
        if (storedPassword !== password) {
          setError("Invalid email or password")
          setIsLoading(false)
          return
        }
      }

      const name = email.split("@")[0] || "User"
      setUserName(name.charAt(0).toUpperCase() + name.slice(1))
      setIsLoggedIn(true)
      setIsNewUser(false)
      setCurrentPage("dashboard")
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
