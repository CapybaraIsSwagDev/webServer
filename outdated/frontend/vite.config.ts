import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'
import path from 'path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  build: {
    // 1. Write the build files to the Flask static folder
    outDir: '../static',
    // 2. Clear the folder before building
    emptyOutDir: true,
    // 3. Ensure the asset paths work with Flask
    assetsDir: 'assets',
  },
  server: {
    proxy: {
      // Proxying API calls to Flask
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        secure: false,
      }
    }
  },
  resolve: {
    alias: {
      // This creates a shortcut to your styles folder
      '@styles': path.resolve(__dirname, './src/styles'),
    },
  },
})
