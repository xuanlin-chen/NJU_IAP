<template>
  <!-- 登录/注册模态框 -->
  <n-modal v-model:show="localShow" preset="card" style="width: 400px">
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
              <n-button @click="handleCancel">取消</n-button>
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
              <n-button @click="handleCancel">取消</n-button>
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
</template>

<script setup lang="ts">
import {
  NModal,
  NForm,
  NFormItem,
  NInput,
  NTabs,
  NTabPane,
  NButton,
  useMessage,
} from "naive-ui";
import { ref, computed, defineProps, defineEmits } from "vue";
import { useUserStore } from "@/stores/userStore";
import { useRouter } from "vue-router";

const props = defineProps<{
  show: boolean;
  initialTab?: 'login' | 'register';
}>();

const emit = defineEmits<{
  (e: 'update:show', value: boolean): void;
  (e: 'login-success'): void;
  (e: 'register-success'): void;
}>();

const router = useRouter();
const userStore = useUserStore();
const message = useMessage();
const activeTab = ref(props.initialTab || 'login');
const formRef = ref(null);

// 创建计算属性来处理v-model绑定
const localShow = computed({
  get: () => props.show,
  set: (value: boolean) => emit('update:show', value)
});

const authForm = ref({
  username: '',
  password: '',
});

// 处理认证（登录/注册）
const handleAuth = async (type: 'login' | 'register') => {
  try {
    let result: { success: boolean; error?: string };
    
    if (type === 'login') {
      result = await userStore.login(authForm.value.username, authForm.value.password);
    } else {
      result = await userStore.register(authForm.value.username, authForm.value.password);
    }
    
    if (result.success) {
      // 操作成功
      emit('update:show', false);
      message.success(`${type === 'login' ? '登录' : '注册'}成功`);
      
      // 触发登录/注册成功事件
      if (type === 'login') {
        emit('login-success');
      } else {
        emit('register-success');
      }
    } else {
      // 处理错误
      message.error(result.error || `${type === 'login' ? '登录' : '注册'}失败`);
    }
  } catch (error) {
    console.error(`${type === 'login' ? '登录' : '注册'}请求出错:`, error);
    message.error(`${type === 'login' ? '登录' : '注册'}失败，请稍后重试`);
  }
};

// 处理取消按钮
const handleCancel = () => {
  emit('update:show', false);
};
</script>

<style scoped>
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
