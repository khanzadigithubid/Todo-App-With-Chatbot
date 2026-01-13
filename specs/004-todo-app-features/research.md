# Research Findings: Todo App Enhancements

**Feature Branch**: `004-todo-app-features`  
**Date**: 2025-12-15  
**Spec**: [specs/004-todo-app-features/spec.md](specs/004-todo-app-features/spec.md)
**Plan**: [specs/004-todo-app-features/plan.md](specs/004-todo-app-features/plan.md)

## Phase 0: Research

### Research Task 1: Frontend Testing Framework

-   **Decision**: No existing frontend testing framework found in the project. A suitable framework (e.g., Jest with React Testing Library) will need to be chosen and integrated during the implementation phase to ensure robust testing of UI components and interactions.
-   **Rationale**: Examination of `frontend/package.json` revealed no explicit dependencies on common frontend testing libraries (such as Jest, React Testing Library, Cypress, etc.). This indicates a current absence of a formalized frontend testing setup within the project's frontend directory.
-   **Alternatives Considered**:
    -   **Jest with React Testing Library**: A popular and well-supported combination for React/Next.js applications, offering unit and integration testing capabilities.
    -   **Cypress**: An end-to-end testing framework suitable for testing full user flows.
    -   **Playwright**: Another end-to-end testing framework, offering similar capabilities to Cypress.

### Research Task 2: Best Practices for Urdu Language Support (Localization) in Next.js 16+ App Router

-   **Decision**: Implement localization using the `next-intl` library in conjunction with Next.js App Router's built-in i18n routing features. This approach will cover all new user-facing strings for Urdu language support.
-   **Rationale**: `next-intl` provides robust integration with the Next.js App Router and supports Server Components, making it a highly recommended solution for modern Next.js applications. The App Router's folder-based routing for locales (`app/[locale]/...`) simplifies URL management for different languages.
-   **Alternatives Considered**:
    -   **`react-i18next`**: A widely used i18n library for React, but its integration with Next.js App Router and Server Components might require more manual setup compared to `next-intl`.
    -   **Manual Implementation**: Building a custom i18n solution, which would be more time-consuming and prone to errors, especially when dealing with complexities like RTL.

**Key Considerations for Urdu Localization Implementation**:

1.  **Next.js App Router i18n Features**:
    -   Utilize folder-based routing (`app/[locale]/`).
    -   Define supported locales (`en`, `ur`) in an `i18n.config.ts` file.
2.  **`next-intl` Library**:
    -   Set up `next-intl` to load translations from JSON files (e.g., `messages/ur.json`).
    -   Use `NextIntlClientProvider` in `app/[locale]/layout.tsx` to make translations available throughout the app.
    -   Employ `useTranslations` hook in components for string translation.
3.  **Right-to-Left (RTL) Support**:
    -   Dynamically set the `dir="rtl"` attribute on the `<html>` tag for the Urdu locale.
    -   Prefer logical CSS properties (e.g., `margin-inline-start`, `text-align-end`) over physical properties to ensure correct layout for RTL languages.
    -   Leverage existing RTL support within CSS frameworks like Tailwind CSS if applicable.
4.  **Font Considerations**:
    -   Select a font that properly supports Urdu Nastaliq script (e.g., `Noto Nastaliq Urdu`).
    -   Use `@next/font` for optimized font loading.
5.  **Date, Time, and Number Formatting**:
    -   Utilize the built-in `Intl.DateTimeFormat` and `Intl.NumberFormat` APIs for locale-aware formatting of dates, times, and numbers specific to Urdu (`ur-PK` locale).
6.  **SEO Considerations (`hreflang`)**:
    -   Implement `hreflang` meta tags in the page `head` (e.g., via Next.js `Metadata` API) to inform search engines about localized content versions.
7.  **User Preference and Language Switching**:
    -   Provide a UI element (e.g., a dropdown) for users to manually switch between English and Urdu.
    -   Detect initial language preference using the `Accept-Language` header and store user's choice in a cookie or local storage.
8.  **Testing**:
    -   Thoroughly test RTL layout, correct translations, proper formatting, and navigation for both locales.
