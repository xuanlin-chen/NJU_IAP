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

    <!-- Combined Auth Modal -->
    <n-modal v-model:show="showAuthModal" preset="card" style="width: 400px">
      <div class="auth-tabs">
        <n-tabs v-model:value="activeTab" type="segment" animated>
          <n-tab-pane name="login" tab="登录">
            <div class="login-form">
              <n-form :model="authForm" ref="formRef">
                <n-form-item label="用户名" path="username">
                  <n-input
                    v-model:value="authForm.username"
                    placeholder="请输入用户名"
                  />
                </n-form-item>
                <n-form-item label="密码" path="password">
                  <n-input
                    v-model:value="authForm.password"
                    type="password"
                    placeholder="请输入密码"
                    @keyup.enter="handleAuth('login')"
                  />
                </n-form-item>
              </n-form>
              <div class="form-actions">
                <n-button @click="showAuthModal = false">取消</n-button>
                <n-button
                  type="primary"
                  @click="handleAuth('login')"
                  :loading="userStore.loading"
                >
                  登录
                </n-button>
              </div>
            </div>
          </n-tab-pane>
          <n-tab-pane name="register" tab="注册">
            <div class="login-form">
              <n-form :model="authForm" ref="formRef">
                <n-form-item label="用户名" path="username">
                  <n-input
                    v-model:value="authForm.username"
                    placeholder="请输入用户名"
                  />
                </n-form-item>
                <n-form-item label="密码" path="password">
                  <n-input
                    v-model:value="authForm.password"
                    type="password"
                    placeholder="请输入密码"
                    @keyup.enter="handleAuth('register')"
                  />
                </n-form-item>
              </n-form>
              <div class="form-actions">
                <n-button @click="showAuthModal = false">取消</n-button>
                <n-button
                  type="primary"
                  @click="handleAuth('register')"
                  :loading="userStore.loading"
                >
                  注册
                </n-button>
              </div>
            </div>
          </n-tab-pane>
        </n-tabs>
      </div>
    </n-modal>

    <p class="description">这是教育数据聚合平台的首页，提供功能导航。</p>
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
import {
  NIcon,
  NButton,
  NModal,
  NForm,
  NFormItem,
  NInput,
  NTabs,
  NTabPane,
  NMessageProvider,
  useMessage,
} from "naive-ui";
import { useRouter } from "vue-router";
import { ref } from "vue";
import { DashboardIcon, ChatIcon, BookIcon } from "../components/icons";
import { useUserStore } from "../stores/userStore";

const router = useRouter();
const userStore = useUserStore();
const message = useMessage();
const showAuthModal = ref(false);
const activeTab = ref("login");
const formRef = ref(null);

const authForm = ref({
  username: "",
  password: "",
});

// 导航到指定路由
const navigateTo = (route: string) => {
  router.push(`/${route}`);
};

// 处理认证（登录/注册）
const handleAuth = async (type: "login" | "register") => {
  try {
    let result: { success: boolean; error?: string };
    
    if (type === "login") {
      result = await userStore.login(authForm.value.username, authForm.value.password);
    } else {
      result = await userStore.register(authForm.value.username, authForm.value.password);
    }
    
    if (result.success) {
      // 操作成功
      showAuthModal.value = false;
      router.push("/dashboard"); // 认证成功后跳转到仪表盘页面
      message.success(`${type === "login" ? "登录" : "注册"}成功`);
    } else {
      // 处理错误
      message.error(result.error || `${type === "login" ? "登录" : "注册"}失败`);
    }
  } catch (error) {
    console.error(`${type === "login" ? "登录" : "注册"}请求出错:`, error);
    message.error(`${type === "login" ? "登录" : "注册"}失败，请稍后重试`);
  }
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
