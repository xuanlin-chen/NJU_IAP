// Import CSS with special comment to instruct Vite to handle separately
import './assets/main.css' /* webpackChunkName: "main-styles" */
import './assets/material-design-colors.css' /* webpackChunkName: "theme-styles" */
import { applyMaterialTheme } from './assets/themeUtils'

// Core app imports
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia';

// Implement preloading for important routes
const preloadComponents = () => {
  // Preload critical components with a delay to not impact initial load
  setTimeout(() => {
    import(/* webpackChunkName: "dashboard" */ './views/DashboardView/index.vue')
    import(/* webpackChunkName: "home" */ './views/HomeView.vue')
  }, 1000)
}

// Import only the required Naive UI components for the main layout
// Other components will be imported on-demand in their respective views
import {
  create,
  NLayout,
  NLayoutContent,
  NMessageProvider,
  NConfigProvider
} from 'naive-ui'

// Create a minimal Naive UI instance with only essential components
const naive = create({
  components: [
    NLayout,
    NLayoutContent,
    NMessageProvider,
    NConfigProvider
  ]
})

// 初始化 Material Design 主题
applyMaterialTheme('#1976d2', false) // 使用蓝色作为主题色，明亮模式

const app = createApp(App)
const pinia = createPinia();
app.use(router)
app.use(pinia);
app.use(naive)
app.mount('#app')

// Initialize preloading after app is mounted
preloadComponents()
