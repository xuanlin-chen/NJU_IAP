<script setup lang="ts">
import { ref, onErrorCaptured } from 'vue'
import { 
  NConfigProvider, 
  NLayout, 
  NLayoutContent,
  NMessageProvider,
} from 'naive-ui'
import SideBar from './components/SideBar.vue'

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
  /* 添加左边距，为顶部菜单按钮留出空间 */
  padding-left: 60px;
  padding-right: 0;
  padding-top: 0;
  padding-bottom: 0;
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