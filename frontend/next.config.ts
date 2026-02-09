import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  experimental: {
    typedRoutes: true,
  },
  async rewrites() {
    return [
      // Proxy API requests to the backend in development
      {
        source: '/api/:path*',
        destination: process.env.NODE_ENV === 'development' 
          ? 'http://127.0.0.1:8000/api/:path*' 
          : `${process.env.PROD_BACKEND_URL || process.env.NEXT_PUBLIC_PROD_API_URL || 'http://127.0.0.1:8000'}/api/:path*`,
      },
    ]
  },
}

export default nextConfig