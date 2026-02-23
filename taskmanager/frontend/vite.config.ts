import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// api calls proxy to backend

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api':{
        target: 'http://localhost:8888',
        changeOrigin: true,
      }
    }
  }
})
