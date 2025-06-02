<template>
  <n-message-provider>
    <div class="home-container">
      <!-- 背景元素 -->
      <div class="background-elements">
        <div class="bg-circle circle-1"></div>
        <div class="bg-circle circle-2"></div>
        <div class="bg-circle circle-3"></div>
      </div>

      <!-- 导航栏 -->
      <div class="nav-bar">
        <div class="logo-container">
          <img src="../assets/nju.png" class="nav-logo" alt="南京大学logo" />
          <span class="logo-text">NJU-IAP</span>
        </div>
        <div class="nav-right">
          <div class="auth-buttons" v-if="!userStore.isLoggedIn">
            <n-button
              @click="showAuthModal = true; activeTab = 'login';"
              quaternary
              size="medium"
              class="login-btn"
            >
              登录
            </n-button>
            <n-button
              @click="showAuthModal = true; activeTab = 'register';"
              type="primary"
              size="medium"
              class="register-btn"
            >
              注册
            </n-button>
          </div>
          <div class="user-avatar" @click="showUserModal = true">
            <AccountIcon v-if="!userStore.isLoggedIn" />
            <AccountIcon_ v-else />
          </div>
        </div>
      </div>

      <!-- 主要内容区 -->
      <div class="hero-section">
        <div class="hero-content">
          <h1 class="main-title">南京大学信息聚合平台</h1>
          <p class="subtitle">汇聚校园资讯，智能推送，尽在掌握</p>
          <div class="cta-buttons">
            <n-button type="primary" size="large" class="cta-button" @click="navigateTo('dashboard')">
              <template #icon>
                <n-icon><dashboard-icon /></n-icon>
              </template>
              开始探索
            </n-button>
            <n-button quaternary size="large" class="cta-button" @click="navigateTo('about')">
              <template #icon>
                <n-icon><book-icon /></n-icon>
              </template>
              了解更多
            </n-button>
          </div>
        </div>
        <div class="hero-image">
          <img src="../assets/xiaoxun.jpg" class="mascot-image" alt="小寻吉祥物" />
        </div>
      </div>

      <!-- 功能特性区 -->
      <div class="features-section">
        <h2 class="section-title">功能导航</h2>
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
            <p>蓝鲸智能助手，免去手动查找信息的烦恼</p>
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
      </div>

      <!-- 页脚 -->
      <div class="footer">
        <div class="footer-logo">
          <img src="../assets/nju.png" class="footer-logo-img" alt="南京大学logo" />
          <span>南京大学信息聚合平台</span>
        </div>
        <p class="copyright">© {{ new Date().getFullYear() }} NJU-IAP ACA团队 保留所有权利</p>
      </div>

      <!-- 登录/注册模态框 -->
      <auth-modal
        v-model:show="showAuthModal"
        :initial-tab="activeTab"
        @login-success="handleLoginSuccess"
        @register-success="handleRegisterSuccess"
      />

      <!-- 用户选项模态框 -->
      <n-modal
        v-model:show="showUserModal"
        style="width: 300px"
        preset="card"
        :title="userStore.isLoggedIn ? '用户选项' : '请登录'"
        size="small"
        :bordered="false"
        :segmented="true"
        :auto-focus="false"
        transform-origin="center"
      >
        <!-- 用户信息区域 -->
        <div class="user-modal-header">
          <div class="user-avatar">
            <AccountIcon v-if="!userStore.isLoggedIn" />
            <AccountIcon_ v-else />
          </div>
          <div class="user-info">
            <div class="user-name">{{ userStore.isLoggedIn ? userStore.user?.username : '未登录' }}</div>
            <div class="user-status">{{ userStore.isLoggedIn ? '在线' : '点击登录以使用完整功能' }}</div>
          </div>
        </div>
        
        <!-- 分割线 -->
        <div class="user-modal-divider"></div>
        
        <!-- 菜单选项 -->
        <n-space vertical class="user-modal-options">
          <n-button 
            v-for="option in dropdownOptions" 
            :key="option.key" 
            @click="handleModalOption(option.key)"
            class="user-option-button"
            text
            size="large"
          >
            {{ option.label }}
          </n-button>
        </n-space>
      </n-modal>
    </div>
  </n-message-provider>
</template>

<script setup lang="ts">
import { NIcon, NButton, NMessageProvider, NModal, NSpace } from "naive-ui";
import { useRouter } from "vue-router";
import { ref, defineAsyncComponent, onMounted, computed } from "vue";
import { DashboardIcon, ChatIcon, BookIcon } from "../components/icons";
import { useUserStore } from "../stores/userStore";
import AccountIcon from "../components/icons/AccountIcon.vue";
import AccountIcon_ from "../components/icons/AccountIcon_.vue";

const AuthModal = defineAsyncComponent(
  () => import("../components/auth/AuthModal.vue")
);

const router = useRouter();
const userStore = useUserStore();
const showAuthModal = ref(false);
const showUserModal = ref(false);
const activeTab = ref<"login" | "register">("login");

// 下拉菜单选项
const dropdownOptions = computed(() => {
  const commonOptions = [
    {
      label: "退订消息",
      key: "unsubscribe",
    }
  ];
  
  // 根据登录状态返回不同选项
  const loginOptions = userStore.isLoggedIn 
    ? [
        {
          label: "个人设置",
          key: "settings",
        },
        {
          label: "退出登录",
          key: "logout",
        }
      ]
    : [
        {
          label: "登录/注册",
          key: "login",
        }
      ];
      
  return [...loginOptions, ...commonOptions];
});

// 处理模态框选项选择
const handleModalOption = (key: string) => {
  switch (key) {
    case 'login':
      showUserModal.value = false;
      showAuthModal.value = true;
      activeTab.value = 'login';
      break;
    case 'settings':
      router.push('/settings');
      showUserModal.value = false;
      break;
    case 'logout':
      userStore.logout();
      showUserModal.value = false;
      break;
    case 'unsubscribe':
      // 处理退订消息逻辑
      showUserModal.value = false;
      break;
  }
};

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

// 检查用户登录状态
const checkLoginStatus = async () => {
  try {
    const response = await fetch('/api/check-login', {
      credentials: 'include'
    });
    const result = await response.json();
    if (response.ok && result.code === 200) {
      userStore.user = result.data;
      userStore.isLoggedIn = true;
    }
  } catch (error) {
    console.error('检查登录状态失败:', error);
  }
};

// 页面加载时检查登录状态
onMounted(() => {
  checkLoginStatus();
  document.querySelector('.home-container')?.classList.add('loaded');
});
</script>

<style scoped>
/* 全局容器样式 */
.home-container {
  min-height: 100vh;
  width: 100%;
  overflow-x: hidden;
  position: relative;
  background-color: #f9f9fb;
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.8s ease, transform 0.8s ease;
}

.home-container.loaded {
  opacity: 1;
  transform: translateY(0);
}

/* 背景元素 */
.background-elements {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  z-index: 0;
}

.bg-circle {
  position: absolute;
  border-radius: 50%;
  opacity: 0.1;
}

.circle-1 {
  top: -10%;
  right: -5%;
  width: 45vw;
  height: 45vw;
  background: linear-gradient(135deg, #1976d2, #64b5f6);
  animation: float 15s ease-in-out infinite alternate;
}

.circle-2 {
  bottom: -15%;
  left: -10%;
  width: 40vw;
  height: 40vw;
  background: linear-gradient(135deg, #1565c0, #42a5f5);
  animation: float 18s ease-in-out infinite alternate-reverse;
}

.circle-3 {
  top: 40%;
  right: 25%;
  width: 20vw;
  height: 20vw;
  background: linear-gradient(135deg, #0d47a1, #2196f3);
  animation: float 12s ease-in-out infinite alternate;
}

@keyframes float {
  0% {
    transform: translate(0, 0) rotate(0deg);
  }
  100% {
    transform: translate(2%, 2%) rotate(5deg);
  }
}

/* 导航栏样式 */
.nav-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 40px;
  position: relative;
  z-index: 10;
}

.logo-container {
  display: flex;
  align-items: center;
  gap: 50px;
  border: 1px;
}

.nav-logo {
  height: 40px;
  width: auto;
}

.logo-text {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1976d2;
  letter-spacing: 0.5px;
  margin-right: 40px;
}

.nav-right {
  display: flex;
  align-items: center;
  gap: 20px;
}

.auth-buttons {
  display: flex;
  gap: 16px;
  margin-right: 20px;
}

.user-avatar {
  cursor: pointer;
  transition: transform 0.2s ease;
}

.user-avatar:hover {
  transform: scale(1.05);
}

.login-btn:hover, .register-btn:hover {
  transform: translateY(-2px);
  transition: transform 0.3s ease;
}

/* 主要内容区样式 */
.hero-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 40px 40px 80px;
  position: relative;
  z-index: 1;
}

.hero-content {
  flex: 1;
  max-width: 600px;
  animation: fadeInUp 1s ease 0.2s both;
}

.main-title {
  font-size: 3.5rem;
  font-weight: 800;
  color: #1565c0;
  margin-bottom: 20px;
  line-height: 1.2;
  letter-spacing: -0.5px;
}

.subtitle {
  font-size: 1.5rem;
  color: #546e7a;
  margin-bottom: 40px;
  line-height: 1.5;
}

.cta-buttons {
  display: flex;
  gap: 20px;
  margin-top: 30px;
}

.cta-button {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.cta-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

.hero-image {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  animation: fadeInRight 1s ease 0.4s both;
}

.mascot-image {
  max-width: 90%;
  height: auto;
  border-radius: 20px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  transform: perspective(1000px) rotateY(-5deg);
  transition: transform 0.5s ease;
}

.mascot-image:hover {
  transform: perspective(1000px) rotateY(0deg);
}

/* 功能特性区样式 */
.features-section {
  padding: 80px 40px;
  background-color: white;
  position: relative;
  z-index: 2;
  box-shadow: 0 -10px 30px rgba(0, 0, 0, 0.05);
  border-radius: 40px 40px 0 0;
  margin-top: -40px;
}

.section-title {
  text-align: center;
  font-size: 2.5rem;
  font-weight: 700;
  color: #1565c0;
  margin-bottom: 60px;
  position: relative;
}

.section-title::after {
  content: '';
  position: absolute;
  bottom: -15px;
  left: 50%;
  transform: translateX(-50%);
  width: 80px;
  height: 4px;
  background: linear-gradient(90deg, #1976d2, #64b5f6);
  border-radius: 2px;
}

.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 40px;
  margin-top: 40px;
}

.feature {
  padding: 40px 30px;
  border-radius: 20px;
  background-color: #fff;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
  transition: transform 0.4s ease, box-shadow 0.4s ease;
  cursor: pointer;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.feature:hover {
  transform: translateY(-15px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
}

.feature-icon {
  margin-bottom: 25px;
  color: #1976d2;
  background-color: rgba(25, 118, 210, 0.1);
  width: 90px;
  height: 90px;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: transform 0.3s ease;
}

.feature:hover .feature-icon {
  transform: scale(1.1);
  color: #1565c0;
}

.feature h3 {
  font-size: 1.8rem;
  margin-bottom: 20px;
  color: #1565c0;
  font-weight: 600;
}

.feature p {
  color: #546e7a;
  line-height: 1.7;
  font-size: 1.1rem;
}

/* 页脚样式 */
.footer {
  background-color: #1565c0;
  color: white;
  padding: 40px;
  text-align: center;
  position: relative;
  z-index: 2;
}

.footer-logo {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
  font-size: 1.2rem;
  font-weight: 500;
}

.footer-logo-img {
  height: 40px;
  filter: brightness(0) invert(1);
}

.copyright {
  opacity: 0.8;
  font-size: 0.9rem;
}

/* 动画效果 */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeInRight {
  from {
    opacity: 0;
    transform: translateX(30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .hero-section {
    flex-direction: column;
    text-align: center;
    padding: 20px 20px 60px;
  }

  .hero-content {
    max-width: 100%;
    margin-bottom: 40px;
  }

  .cta-buttons {
    justify-content: center;
  }

  .main-title {
    font-size: 2.8rem;
  }

  .subtitle {
    font-size: 1.3rem;
  }

  .features-section {
    padding: 60px 20px;
  }
}

@media (max-width: 768px) {
  .nav-bar {
    padding: 15px 20px;
  }

  .logo-text {
    font-size: 1.2rem;
  }

  .nav-logo {
    height: 30px;
  }

  .main-title {
    font-size: 2.2rem;
  }

  .subtitle {
    font-size: 1.1rem;
    margin-bottom: 30px;
  }

  .cta-buttons {
    flex-direction: column;
    gap: 15px;
  }

  .section-title {
    font-size: 2rem;
    margin-bottom: 40px;
  }

  .feature {
    padding: 30px 20px;
  }

  .feature h3 {
    font-size: 1.5rem;
  }

  .feature p {
    font-size: 1rem;
  }
}

.user-modal-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 0;
}

.user-info {
  flex: 1;
}

.user-name {
  font-size: 16px;
  font-weight: 500;
  color: #333;
}

.user-status {
  font-size: 14px;
  color: #666;
  margin-top: 4px;
}

.user-modal-divider {
  height: 1px;
  background-color: #eee;
  margin: 16px 0;
}

.user-modal-options {
  width: 100%;
}

.user-option-button {
  width: 100%;
  text-align: left;
  padding: 12px 16px;
}

.user-option-button:hover {
  background-color: #f5f5f5;
}
</style>

