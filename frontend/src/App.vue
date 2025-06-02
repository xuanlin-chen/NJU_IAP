<script setup lang="ts">
import { ref, onErrorCaptured, onMounted } from 'vue'
// Import Naive UI components individually for better tree-shaking
import { NConfigProvider } from 'naive-ui'
import { NLayout } from 'naive-ui'
import { NLayoutContent } from 'naive-ui'
import { NMessageProvider } from 'naive-ui'
import { defineAsyncComponent } from 'vue'
import { useUserStore } from './stores/userStore'

// Load the sidebar component only when needed using defineAsyncComponent
const SideBar = defineAsyncComponent({
  loader: () => import('./components/SideBar.vue'),
  delay: 100,
  timeout: 2000
})

const userStore = useUserStore()

// 错误处理
const hasError = ref(false)
const errorMsg = ref('')

// 错误捕获
onErrorCaptured((err) => {
  console.error('App error:', err)
  hasError.value = true
  errorMsg.value = String(err)
  return false // 阻止错误继续传播
})

// 页面加载时检查登录状态
onMounted(() => {
  // 移除登录状态检查，因为这个功能已经在 HomeView.vue 中实现了
});
</script>

<template>
  <n-config-provider>
    <n-message-provider>
      <n-layout position="absolute">
        <!-- 侧边栏 -->
        <SideBar />

        <!-- 主内容区 -->
        <n-layout-content class="content-container">
          <div class="background-gradient"></div>
          
          <!-- 错误提示 -->
          <div v-if="hasError" class="error-message">
            发生错误: {{ errorMsg }}
          </div>
          
          <!-- 路由视图 -->
          <router-view />
        </n-layout-content>
      </n-layout>
    </n-message-provider>
  </n-config-provider>
</template>

<style>
html, body, #app {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
}
</style>

<style scoped>
.content-container {
  position: relative;
  background-color: #ffffff;
  color: #333333;
  width: 100%;
  min-height: 100vh;
  padding: 0;
  overflow: hidden; /* 防止内容溢出 */
}

.background-gradient {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: -1;
  background: #f8f9fa;
}

.error-message {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  padding: 10px;
  background-color: #ffdddd;
  color: #ff0000;
  z-index: 9999;
  text-align: center;
}
</style>