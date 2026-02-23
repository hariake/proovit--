import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// api calls proxy to backend

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': 'http://localhost:8888'
    }
  }
})
