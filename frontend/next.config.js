/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export', // Export as static site
  env: {
    NEXT_PUBLIC_API_BASE_URL: process.env.NEXT_PUBLIC_API_BASE_URL,
    NEXT_PUBLIC_VERCEL_URL: process.env.NEXT_PUBLIC_VERCEL_URL,
    NEXT_PUBLIC_PROD_API_URL: process.env.NEXT_PUBLIC_PROD_API_URL,
  },
  async rewrites() {
    return [
      // Proxy API requests to the backend
      {
        source: '/api/:path*',
        destination: process.env.NODE_ENV === 'development' 
          ? 'http://127.0.0.1:8000/api/:path*' 
          : `${process.env.PROD_BACKEND_URL || 'http://127.0.0.1:8000'}/api/:path*`,
      },
    ]
  },
}

module.exports = nextConfig