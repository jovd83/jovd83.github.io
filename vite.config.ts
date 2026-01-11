import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  base: '/',
  build: {
    rollupOptions: {
      input: {
        main: 'index.html',
        radar: 'ai-radar.html',
        tester: 'tester-life.html',
        prompts: 'prompts.html',
        shownotes: 'shownotes.html',
        speaking: 'speaking.html',
      },
    },
  },
})
