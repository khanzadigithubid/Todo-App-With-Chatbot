"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { signupUser } from "@/services/api"
import { storeJwt } from "@/services/authService"
import Link from "next/link"
import { motion } from "framer-motion"
import { EyeIcon, EyeOffIcon } from "lucide-react"

export default function SignupForm() {
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    const [name, setName] = useState("")
    const [showPassword, setShowPassword] = useState(false)
    const [error, setError] = useState<string | null>(null)
    const [isLoading, setIsLoading] = useState(false)
    const router = useRouter()

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        setError(null)
        setIsLoading(true)

        try {
            const data = await signupUser(email, password, name)
            storeJwt(data.access_token)
            router.push("/dashboard") // Redirect to dashboard after signup
        } catch (err: any) {
            if (err.status === 409) {
                setError("Email already exists. Please try a different email.");
            } else {
                setError(err.message || "Signup failed");
            }
        } finally {
            setIsLoading(false)
        }
    }

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="w-full max-w-md"
        >
            <div className="bg-gradient-to-br from-gray-800/50 to-gray-900/50 backdrop-blur-sm p-8 rounded-2xl border border-gray-700/50 shadow-2xl">
                <div className="text-center mb-8">
                    <div className="mx-auto mb-4 w-16 h-16 rounded-full bg-gradient-to-br from-emerald-500/20 to-cyan-500/20 flex items-center justify-center">
                        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" className="text-emerald-400">
                            <path d="M16 7C16 9.20914 14.2091 11 12 11C9.79086 11 8 9.20914 8 7C8 4.79086 9.79086 3 12 3C14.2091 3 16 4.79086 16 7Z" stroke="currentColor" strokeWidth="2"/>
                            <path d="M3 21V19C3 17.9391 3.42143 16.9217 4.17157 16.1716C4.92172 15.4214 5.93913 15 7 15H17C18.0609 15 19.0783 15.4214 19.8284 16.1716C20.5786 16.9217 21 17.9391 21 19V21" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                        </svg>
                    </div>
                    <h2 className="text-2xl font-bold bg-gradient-to-r from-emerald-400 to-cyan-400 bg-clip-text text-transparent mb-2">
                        Create Account
                    </h2>
                    <p className="text-gray-400">Join FlowTask today</p>
                </div>

                <form onSubmit={handleSubmit} className="space-y-5">
                    <div>
                        <label htmlFor="name" className="block text-sm font-medium text-gray-300 mb-2">
                            Full Name
                        </label>
                        <div className="relative">
                            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" className="text-gray-400">
                                    <path d="M16 7C16 9.20914 14.2091 11 12 11C9.79086 11 8 9.20914 8 7C8 4.79086 9.79086 3 12 3C14.2091 3 16 4.79086 16 7Z" stroke="currentColor" strokeWidth="2"/>
                                    <path d="M20 21V19C20 17.9391 19.5786 16.9217 18.8284 16.1716C18.0783 15.4214 17.0609 15 16 15H8C6.93913 15 5.92172 15.4214 5.17157 16.1716C4.42143 16.9217 4 17.9391 4 19V21" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                                </svg>
                            </div>
                            <input
                                id="name"
                                type="text"
                                value={name}
                                onChange={(e) => setName(e.target.value)}
                                placeholder="Enter your full name"
                                required
                                className="w-full pl-10 pr-4 py-3 rounded-lg bg-gray-700/50 border border-gray-600 placeholder:text-gray-400 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition-all duration-300 text-white"
                            />
                        </div>
                    </div>

                    <div>
                        <label htmlFor="email" className="block text-sm font-medium text-gray-300 mb-2">
                            Email Address
                        </label>
                        <div className="relative">
                            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" className="text-gray-400">
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
                                className="w-full pl-10 pr-4 py-3 rounded-lg bg-gray-700/50 border border-gray-600 placeholder:text-gray-400 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition-all duration-300 text-white"
                            />
                        </div>
                    </div>

                    <div>
                        <label htmlFor="password" className="block text-sm font-medium text-gray-300 mb-2">
                            Password
                        </label>
                        <div className="relative">
                            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" className="text-gray-400">
                                    <path d="M19 11H5M15 15V17C15 18.069 14.308 18.9583 13.3567 19.4279C12.4054 19.8975 11.2946 19.8975 10.3433 19.4279C9.39205 18.9583 8.7 18.069 8.7 17V15M5 11V9C5 6.23858 7.23858 4 10 4H14C16.7614 4 19 6.23858 19 9V11C19 13.7614 16.7614 16 14 16H10C7.23858 16 5 13.7614 5 11Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                                </svg>
                            </div>
                            <input
                                id="password"
                                type={showPassword ? "text" : "password"}
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                placeholder="Create a password"
                                required
                                minLength={6}
                                className="w-full pl-10 pr-12 py-3 rounded-lg bg-gray-700/50 border border-gray-600 placeholder:text-gray-400 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition-all duration-300 text-white"
                            />
                            <button
                                type="button"
                                onClick={() => setShowPassword(!showPassword)}
                                className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-white transition-colors"
                            >
                                {showPassword ? <EyeOffIcon className="w-5 h-5" /> : <EyeIcon className="w-5 h-5" />}
                            </button>
                        </div>
                        <p className="mt-2 text-xs text-gray-500">Password must be at least 6 characters</p>
                    </div>

                    <div className="flex items-start">
                        <input
                            id="terms"
                            type="checkbox"
                            required
                            className="mt-1 h-4 w-4 text-emerald-600 focus:ring-emerald-500 border-gray-600 rounded bg-gray-700"
                        />
                        <label htmlFor="terms" className="ml-2 block text-sm text-gray-300">
                            I agree to the <a href="#" className="text-emerald-400 hover:text-emerald-300">Terms of Service</a> and <a href="#" className="text-emerald-400 hover:text-emerald-300">Privacy Policy</a>
                        </label>
                    </div>

                    <motion.button
                        type="submit"
                        disabled={isLoading}
                        whileHover={{ scale: 1.02 }}
                        whileTap={{ scale: 0.98 }}
                        className="w-full px-4 py-3.5 bg-gradient-to-r from-emerald-600 to-emerald-700 hover:from-emerald-500 hover:to-emerald-600 rounded-lg text-white font-semibold shadow-lg hover:shadow-emerald-500/25 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        {isLoading ? (
                            <div className="flex items-center justify-center">
                                <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
                                Creating account...
                            </div>
                        ) : (
                            "Create Account"
                        )}
                    </motion.button>

                    {error && (
                        <motion.div
                            initial={{ opacity: 0, y: -10 }}
                            animate={{ opacity: 1, y: 0 }}
                            className="p-3 bg-red-500/10 border border-red-500/30 rounded-lg text-red-400 text-sm"
                        >
                            {error}
                        </motion.div>
                    )}
                </form>

                <div className="mt-6 text-center text-sm text-gray-400">
                    <p>
                        Already have an account?{' '}
                        <Link href="/login" className="font-medium text-emerald-400 hover:text-emerald-300 transition-colors">
                            Sign in
                        </Link>
                    </p>
                </div>
            </div>
        </motion.div>
    )
}
