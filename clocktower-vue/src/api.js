// Base URL for the Django backend API.
// - Empty string ('') = same-origin (works when the SPA is served by Django).
// - Set VITE_API_BASE at build time (e.g. .env.production) to reach a
//   separate/public backend from a static deploy (e.g. GitHub Pages).
export const API_BASE = (import.meta.env.VITE_API_BASE || '').replace(/\/$/, '');
