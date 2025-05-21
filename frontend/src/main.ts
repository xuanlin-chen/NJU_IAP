import './assets/main.css'
import './assets/material-design-colors.css'
import { applyMaterialTheme } from './assets/themeUtils'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia';
import {
  create,
  NButton,
  NLayout,
  NLayoutSider,
  NLayoutContent,
  NMenu,
  NIcon,
  NMessageProvider,
  NCard,
  NDataTable,
  NStatistic,
  NGrid,
  NGridItem,
  NSpin,
  NSpace,
  NProgress,
  NConfigProvider,
  NInput,
  NAvatar
} from 'naive-ui'

// 创建 Naive UI 实例
const naive = create({
  components: [
    NButton,
    NLayout,
    NLayoutSider,
    NLayoutContent,
    NMenu,
    NIcon,
    NMessageProvider,
    NCard,
    NDataTable,
    NStatistic,
    NGrid,
    NGridItem,
    NSpin,
    NSpace,
    NProgress,
    NConfigProvider,
    NInput,
    NAvatar
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
