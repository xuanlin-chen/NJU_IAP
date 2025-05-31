<template>
  <n-message-provider>
    <div class="settings-view">
      <div class="container">
        <n-card>
          <template #header>
            <div class="view-header">
              <h1>用户设置</h1>
              <n-button @click="router.back()" quaternary>
                <template #icon>
                  <n-icon><arrow-back-icon /></n-icon>
                </template>
                返回
              </n-button>
            </div>
          </template>

          <template #default>
            <!-- 用户未登录时显示提示 -->
            <div v-if="!userStore.isLoggedIn" class="login-prompt">
              <n-result
                status="warning"
                title="未登录"
                description="请先登录再访问用户设置"
              >
                <template #footer>
                  <n-button @click="showAuthModal = true" type="primary">
                    前往登录
                  </n-button>
                </template>
              </n-result>
            </div>

            <!-- 用户已登录时显示设置 -->
            <user-settings v-else />
          </template>
        </n-card>
      </div>

      <!-- 使用复用的登录/注册模态框 -->
      <auth-modal
        v-model:show="showAuthModal"
        initial-tab="login"
        @login-success="handleLoginSuccess"
      />
    </div>
  </n-message-provider>
</template>

<script setup lang="ts">
import {
  NCard,
  NButton,
  NIcon,
  NResult,
  NMessageProvider,
  useMessage,
} from "naive-ui";
import { useRouter } from "vue-router";
import { ArrowBackOutline as ArrowBackIcon } from "@vicons/ionicons5";
import { useUserStore } from "@/stores/userStore";
import UserSettings from "@/components/user/UserSettings.vue";
import { ref, defineAsyncComponent } from "vue";
const AuthModal = defineAsyncComponent(
  () => import("@/components/auth/AuthModal.vue")
);

const router = useRouter();
const userStore = useUserStore();
const message = useMessage();
const showAuthModal = ref(false);

// 登录成功后的处理
const handleLoginSuccess = () => {
  message.success("登录成功");
  // 不需要主动跳转，因为我们希望用户继续在当前的用户设置页面
};
</script>

<style scoped>
.settings-view {
  width: 100%;
  padding: 40px 20px;
}

.container {
  max-width: 900px;
  margin: 0 auto;
}

.view-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.login-prompt {
  padding: 40px 20px;
  text-align: center;
}
</style>
