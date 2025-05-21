<template>
  <div class="home-container">
    <h1>欢迎使用南京大学信息聚合平台</h1>
    <p class="description">这是教育数据聚合平台的首页，提供功能导航。</p>
    <div class="features">
      <div class="feature" @click="navigateTo('dashboard')">
        <div class="feature-icon">
          <n-icon size="48">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="currentColor" d="M21 18H3V6h18m0-2H3c-1.11 0-2 .89-2 2v12c0 1.1.9 2 2 2h18c1.1 0 2-.9 2-2V6a2 2 0 0 0-2-2m-9 6.5A2.5 2.5 0 0 1 14.5 9A2.5 2.5 0 0 1 17 11.5a2.5 2.5 0 0 1-2.5 2.5A2.5 2.5 0 0 1 12 11.5m1 3h3c1.1 0 2 .9 2 2V17h-8v-.5c0-1.1.9-2 2-2h1Z"/></svg>
          </n-icon>
        </div>
        <h3>实时信息</h3>
        <p>查看南京大学最新消息，支持历史消息查看</p>
      </div>
      <div class="feature" @click="navigateTo('chat')">
        <div class="feature-icon">
          <n-icon size="48">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="currentColor" d="M17 22v2H7v-2h10m2-2H5v2h14v-2m1-8V3c0-.55-.45-1-1-1H8c-.55 0-1 .45-1 1v9h13m-5.5-7c0 .83-.67 1.5-1.5 1.5s-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5s1.5.67 1.5 1.5m0 3.5c0 .83-.67 1.5-1.5 1.5s-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5s1.5.67 1.5 1.5M22 14H7v7h15v-7Z"/></svg>
          </n-icon>
        </div>
        <h3>AI互动</h3>
        <p>提供AI助手，免去手动查找信息的烦恼</p>
      </div>
      <div class="feature" @click="navigateTo('about')">
        <div class="feature-icon">
          <n-icon size="48">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="currentColor" d="M19 1l-5 5v11l5-4.5V1m2 4v13.5c-1.1-.35-2.3-.5-3.5-.5c-1.7 0-4.15.65-5.5 1.5V6c-1.45-1.1-3.55-1.5-5.5-1.5c-1.95 0-4.05.4-5.5 1.5v14.65c0 .25.25.5.5.5c.1 0 .15-.05.25-.05C3.1 20.45 5.05 20 6.5 20c1.95 0 4.05.4 5.5 1.5c1.35-.85 3.8-1.5 5.5-1.5c1.65 0 3.35.3 4.75 1.05c.1.05.15.05.25.05c.25 0 .5-.25.5-.5V6c-.6-.45-1.25-.75-2-1m-2 13.5v-7C18.85 10.05 17.7 10 16.5 10c-1.15 0-3.35.4-5.5 1.5v6.95c1.05-.55 2.95-1.45 5.5-1.45c1.65 0 3.35.3 4.75 1.05c.1.05.15.05.25.05z"/></svg>
          </n-icon>
        </div>
        <h3>关于我们</h3>
        <p>如果你有兴趣了解我们的话</p>
      </div>
    </div>
    
    <div class="mascot-container">
      <img src="../assets/xiaoxun.jpg" class="mascot-image" />
      <img src="../assets/nju.png" class="logo-image" />
    </div>
    
  </div>
</template>

<script setup lang="ts">
import { NIcon } from 'naive-ui'
import { useRouter } from 'vue-router'

const router = useRouter()

// 导航到指定路由
const navigateTo = (route: string) => {
  router.push(`/${route}`)
}
</script>

<style scoped>
.home-container {
  padding: 40px 20px;
  text-align: center;
  max-width: 1200px;
  margin: 0 auto;
  margin-top: 60px;
}

h1 {
  font-size: 2.5rem;
  color: #333;
  margin-bottom: 20px;
}

.description {
  font-size: 1.2rem;
  color: #666;
  max-width: 800px;
  margin: 0 auto 60px;
}

.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 40px;
  margin-top: 40px;
}

.feature {
  padding: 30px;
  border-radius: 12px;
  background-color: #fff;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
  transition: transform 0.3s, box-shadow 0.3s;
  cursor: pointer; /* 添加鼠标指针样式，表明可点击 */
}

.feature:hover {
  transform: translateY(-10px);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
}

.feature-icon {
  margin-bottom: 20px;
  color: #2080f0;
}

.feature h3 {
  font-size: 1.5rem;
  margin-bottom: 15px;
  color: #333;
}

.feature p {
  color: #666;
  line-height: 1.6;
}

/* 调整两张图片的关系，使它们并排显示，并在小屏幕上自动换行 */
.mascot-container {
  margin-top: 120px;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap; /* 允许在小屏幕上换行 */
  gap: 60px; /* 增加图片之间的间距 */
}

.mascot-image {
  max-width: 500px; /* 调整图片大小 */
  width: 100%;
  border-radius: 16px;
}

.logo-image {
  max-width: 180px; /* 调整Logo大小 */
  width: 100%;
  height: auto;
}
</style>