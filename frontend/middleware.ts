import { NextRequest } from 'next/server';

// Simple middleware - remove localization
export function middleware(request: NextRequest) {
  // Allow all routes to pass through
  return undefined;
}

export const config = {
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)'],
};
