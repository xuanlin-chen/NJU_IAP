<template>
  <n-message-provider>
    <div class="home-container">
      <div class="top-actions">
        <n-button
          @click="
            showAuthModal = true;
            activeTab = 'login';
          "
          size="large"
        >
          登录
        </n-button>
        <n-button
          @click="
            showAuthModal = true;
            activeTab = 'register';
          "
          size="large"
        >
          注册
        </n-button>
      </div>
      <h1>欢迎使用南京大学信息聚合平台</h1>

      <!-- 使用复用的登录/注册模态框 -->
      <auth-modal
        v-model:show="showAuthModal"
        :initial-tab="activeTab"
        @login-success="handleLoginSuccess"
        @register-success="handleRegisterSuccess"
      />

      <p class="description"></p>
      <div class="features">
        <div class="feature" @click="navigateTo('dashboard')">
          <div class="feature-icon">
            <n-icon size="48">
              <dashboard-icon />
            </n-icon>
          </div>
          <h3>实时信息</h3>
          <p>查看南京大学最新消息，支持历史消息查看</p>
        </div>
        <div class="feature" @click="navigateTo('chat')">
          <div class="feature-icon">
            <n-icon size="48">
              <chat-icon />
            </n-icon>
          </div>
          <h3>AI互动</h3>
          <p>提供AI助手，免去手动查找信息的烦恼</p>
        </div>
        <div class="feature" @click="navigateTo('about')">
          <div class="feature-icon">
            <n-icon size="48">
              <book-icon />
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
  </n-message-provider>
</template>

<script setup lang="ts">
import { NIcon, NButton, NMessageProvider, useMessage } from "naive-ui";
import { useRouter } from "vue-router";
import { ref, defineAsyncComponent } from "vue";
import { DashboardIcon, ChatIcon, BookIcon } from "../components/icons";
const AuthModal = defineAsyncComponent(
  () => import("../components/auth/AuthModal.vue")
);

const router = useRouter();
const showAuthModal = ref(false);
const activeTab = ref<"login" | "register">("login");

// 导航到指定路由
const navigateTo = (route: string) => {
  router.push(`/${route}`);
};

// 登录成功后的处理
const handleLoginSuccess = () => {
  router.push("/dashboard"); // 认证成功后跳转到仪表盘页面
};

// 注册成功后的处理
const handleRegisterSuccess = () => {
  router.push("/dashboard"); // 认证成功后跳转到仪表盘页面
};
</script>

<style scoped>
.top-actions {
  position: absolute;
  top: 20px;
  right: 40px;
  display: flex;
  gap: 16px;
  z-index: 100;
}

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

.auth-tabs {
  margin-top: 10px;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding-top: 20px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 20px;
}
</style>
