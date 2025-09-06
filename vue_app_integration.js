// main.js
import { createApp } from 'vue'
import App from './App.vue'
import axios from 'axios'

// Configure axios defaults
axios.defaults.baseURL = 'http://localhost:8000'  // Your Django server URL
axios.defaults.timeout = 10000
axios.defaults.headers.common['Content-Type'] = 'application/json'

// Add request interceptor for CSRF token if needed
axios.interceptors.request.use(config => {
  const token = document.querySelector('[name=csrfmiddlewaretoken]')
  if (token) {
    config.headers['X-CSRFToken'] = token.value
  }
  return config
})

// Add response interceptor for error handling
axios.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 403) {
      console.error('CSRF token missing or invalid')
    }
    return Promise.reject(error)
  }
)

const app = createApp(App)
app.config.globalProperties.$http = axios
app.mount('#app')

// App.vue
/*
<template>
  <div id="app">
    <!-- Your existing app content -->
    <div class="main-content">
      <h1>Your Website</h1>
      <p>This is your main website content...</p>
      <!-- Add more content as needed -->
    </div>
    
    <!-- Chatbot Component -->
    <ChatBot />
  </div>
</template>

<script>
import ChatBot from './components/ChatBot.vue'

export default {
  name: 'App',
  components: {
    ChatBot
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  min-height: 100vh;
}

.main-content {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

/* Global styles for your app */
* {
  box-sizing: border-box;
}

body {
  margin: 0;
  padding: 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  background-attachment: fixed;
}
</style>
*/

// package.json dependencies you'll need:
/*
{
  "name": "chatbot-frontend",
  "version": "1.0.0",
  "dependencies": {
    "vue": "^3.3.0",
    "axios": "^1.4.0"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^4.2.0",
    "vite": "^4.3.0"
  },
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "serve": "vite preview"
  }
}
*/

// vite.config.js
/*
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 8080,
    proxy: {
      '/chatbot': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
})
*/