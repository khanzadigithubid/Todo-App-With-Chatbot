import { getRequestConfig } from 'next-intl/server';

// Can be imported from a shared config
const locales = ['en'];

export default getRequestConfig(async ({ locale }) => {
  // Validate that the incoming `locale` parameter is valid
  if (!locale || !locales.includes(locale as any)) {
    // Default to 'en' if locale is undefined or invalid
    locale = 'en';
  }

  return {
    locale,
    messages: (await import(`../../messages/${locale}.json`)).default,
  };
});