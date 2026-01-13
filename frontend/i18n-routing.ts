import { defineRouting } from 'next-intl/routing';

export const routing = defineRouting({
  // A list of all locales that are supported
  locales: ['en'],

  // Used when no locale matches
  defaultLocale: 'en',

  // Optional: Set locale detection to false if you don't want automatic detection
  localeDetection: false,
});