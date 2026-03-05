import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Environment variables with cross-platform defaults
const API_PROXY = process.env.VITE_API_PROXY || 'http://localhost:5000'
const DEV_PORT = parseInt(process.env.VITE_PORT || '3000', 10)

export default defineConfig({
  plugins: [react()],
  server: {
    port: DEV_PORT,
    proxy: {
      '/api': {
        target: API_PROXY,
        changeOrigin: true,
      }
    }
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
  }
})
