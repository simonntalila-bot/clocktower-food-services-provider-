import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  base: './',
  server: {
    allowedHosts: [
      'frill-suitor-gone.ngrok-free.dev',
      '.ngrok-free.app',
      '.ngrok-free.dev',
    ],
    proxy: {
      '/api': 'http://127.0.0.1:8000',
      '/admin-panel': 'http://127.0.0.1:8000',
      '/django-admin': 'http://127.0.0.1:8000',
      '/static': 'http://127.0.0.1:8000',
      '/media': 'http://127.0.0.1:8000',
    },
  },
})
