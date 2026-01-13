"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { loginUser } from "@/services/api"
import { storeJwt } from "@/services/authService"
import Link from "next/link"
import { motion } from "framer-motion"
import { EyeIcon, EyeOffIcon } from "lucide-react"

export default function LoginPage() {
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    const [showPassword, setShowPassword] = useState(false)
    const [error, setError] = useState<string | null>(null)
    const [isLoading, setIsLoading] = useState(false)
    const router = useRouter()

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        setError(null)
        setIsLoading(true)

        try {
            const data = await loginUser(email, password)
            storeJwt(data.access_token)
            router.push("/dashboard") // Redirect to dashboard after login
        } catch (err: any) {
            setError(err.message || "Login failed")
        } finally {
            setIsLoading(false)
        }
    }

    return (
        <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-surface-light to-background px-4 py-12">
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
                className="w-full max-w-md"
            >
                <div className="text-center mb-10">
                    <div className="mx-auto mb-5 w-20 h-20 rounded-2xl bg-gradient-to-r from-primary to-accent flex items-center justify-center shadow-lg">
                        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" className="text-white">
                            <path d="M16 7C16 9.20914 14.2091 11 12 11C9.79086 11 8 9.20914 8 7C8 4.79086 9.79086 3 12 3C14.2091 3 16 4.79086 16 7Z" stroke="currentColor" strokeWidth="2"/>
                            <path d="M3 21V19C3 17.9391 3.42143 16.9217 4.17157 16.1716C4.92172 15.4214 5.93913 15 7 15H17C18.0609 15 19.0783 15.4214 19.8284 16.1716C20.5786 16.9217 21 17.9391 21 19V21" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                        </svg>
                    </div>
                    <h2 className="text-3xl font-bold text-text-primary mb-3">
                        Welcome Back
                    </h2>
                    <p className="text-text-secondary">Sign in to your FlowTask account</p>
                </div>

                <div className="bg-surface rounded-2xl shadow-xl p-8 border border-border">
                    <form onSubmit={handleSubmit} className="space-y-6">
                        <div>
                            <label htmlFor="email" className="block text-sm font-medium text-text-primary mb-2">
                                Email Address
                            </label>
                            <div className="relative">
                                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" className="text-text-secondary">
                                        <path d="M3 8L10.8906 13.2604C11.5624 13.7083 12.4376 13.7083 13.1094 13.2604L21 8M5 19H19C20.1046 19 21 18.1046 21 17V7C21 5.89543 20.1046 5 19 5H5C3.89543 5 3 5.89543 3 7V17C3 18.1046 3.89543 19 5 19Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                                    </svg>
                                </div>
                                <input
                                    id="email"
                                    type="email"
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    placeholder="Enter your email"
                                    required
                                    className="w-full pl-10 pr-4 py-3.5 rounded-xl bg-surface-light border border-border placeholder-text-muted focus:ring-2 focus:ring-primary focus:border-transparent transition-all duration-200 text-text-primary"
                                />
                            </div>
                        </div>

                        <div>
                            <label htmlFor="password" className="block text-sm font-medium text-text-primary mb-2">
                                Password
                            </label>
                            <div className="relative">
                                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" className="text-text-secondary">
                                        <path d="M19 11H5M15 15V17C15 18.069 14.308 18.9583 13.3567 19.4279C12.4054 19.8975 11.2946 19.8975 10.3433 19.4279C9.39205 18.9583 8.7 18.069 8.7 17V15M5 11V9C5 6.23858 7.23858 4 10 4H14C16.7614 4 19 6.23858 19 9V11C19 13.7614 16.7614 16 14 16H10C7.23858 16 5 13.7614 5 11Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                                    </svg>
                                </div>
                                <input
                                    id="password"
                                    type={showPassword ? "text" : "password"}
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    placeholder="Enter your password"
                                    required
                                    className="w-full pl-10 pr-12 py-3.5 rounded-xl bg-surface-light border border-border placeholder-text-muted focus:ring-2 focus:ring-primary focus:border-transparent transition-all duration-200 text-text-primary"
                                />
                                <button
                                    type="button"
                                    onClick={() => setShowPassword(!showPassword)}
                                    className="absolute right-3 top-1/2 transform -translate-y-1/2 text-text-secondary hover:text-text-primary transition-colors"
                                >
                                    {showPassword ? <EyeOffIcon className="w-5 h-5" /> : <EyeIcon className="w-5 h-5" />}
                                </button>
                            </div>
                        </div>

                        <div className="flex items-center justify-between">
                            <div className="flex items-center">
                                <input
                                    id="remember-me"
                                    type="checkbox"
                                    className="h-4 w-4 text-primary focus:ring-primary border-border rounded bg-surface-light"
                                />
                                <label htmlFor="remember-me" className="ml-2 block text-sm text-text-secondary">
                                    Remember me
                                </label>
                            </div>
                            <div className="text-sm">
                                <a href="#" className="font-medium text-primary hover:text-primary-light transition-colors">
                                    Forgot password?
                                </a>
                            </div>
                        </div>

                        <motion.button
                            type="submit"
                            disabled={isLoading}
                            whileHover={{ scale: 1.02 }}
                            whileTap={{ scale: 0.98 }}
                            className="w-full px-4 py-4 bg-gradient-to-r from-primary to-accent hover:from-primary-light hover:to-accent rounded-xl text-white font-bold transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed shadow-md hover:shadow-blue-lg"
                        >
                            {isLoading ? (
                                <div className="flex items-center justify-center">
                                    <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
                                    Signing in...
                                </div>
                            ) : (
                                "Sign In"
                            )}
                        </motion.button>

                        {error && (
                            <motion.div
                                initial={{ opacity: 0, y: -10 }}
                                animate={{ opacity: 1, y: 0 }}
                                className="p-4 bg-error/10 border border-error rounded-xl text-error text-sm mt-4"
                            >
                                {error}
                            </motion.div>
                        )}
                    </form>

                    <div className="mt-8 text-center text-sm text-text-secondary">
                        <p>
                            Don't have an account?{' '}
                            <Link href="/signup" className="font-medium text-primary hover:text-primary-light transition-colors">
                                Sign up for free
                            </Link>
                        </p>
                    </div>
                </div>
            </motion.div>
        </div>
    )
}