<template>
  <n-notification-provider>
    <div>
      <n-spin :show="loading">
        <n-grid :cols="12" :x-gap="16" :y-gap="16" class="dashboard-grid">
          <!-- 左侧区域 -->
          <n-grid-item :span="1">
            <!-- 占位，保持布局平衡 -->
          </n-grid-item>
          
          <!-- 消息区域 -->
          <n-grid-item :span="5">
            <MessageSection />
          </n-grid-item>

          <!-- 右侧区域 -->
          <n-grid-item :span="4">
            <!-- 日历部分 -->
            <CalendarSection />
            <!-- DDL提醒部分 -->
            <DdlSection />
          </n-grid-item>

          <!-- 用户头像 - 移到右上角 -->
          <n-grid-item :span="1" style="position: absolute; top: 1px; right: 8px; width: 150px;">
            <div class="user-avatar-wrapper" @click="showUserModal = true">
              <!-- 根据登录状态动态切换图标 -->
              <AccountIcon v-if="!userStore.isLoggedIn" />
              <AccountIcon_ v-else />
            </div>
            
            <!-- 使用NModal替代下拉菜单 -->
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
                  <div class="user-name">{{ userStore.isLoggedIn ? '已登录用户' : '未登录' }}</div>
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
          </n-grid-item>
        </n-grid>
      </n-spin>

      <!-- 对话框组件 -->
      <ModalDialogs />
      
      <!-- 登录/注册模态框 -->
      <auth-modal
        v-model:show="showAuthModal"
        initial-tab="login"
        @login-success="handleLoginSuccess"
        @register-success="handleRegisterSuccess"
      />
    </div>
  </n-notification-provider>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, provide, watchEffect, computed, defineAsyncComponent } from "vue";
import { useRouter } from "vue-router";
// Import Naive UI components individually for better tree-shaking
import { NGrid } from "naive-ui";
import { NGridItem } from "naive-ui";
import { NSpin } from "naive-ui";
import { NNotificationProvider } from "naive-ui";
import { NModal } from "naive-ui";
import { NSpace } from "naive-ui";
import { NButton } from "naive-ui";
import { createDiscreteApi } from "naive-ui";
import { debugLog } from "../../utils/debug";
import { useDashboardData } from "../../stores/dashboardStore";
import { useUserStore } from "../../stores/userStore";
import AccountIcon from "@/components/icons/AccountIcon.vue";
import AccountIcon_ from "@/components/icons/AccountIcon_.vue";
import type { DdlEvent, NewsItem } from "../../stores/dashboardStore";

// 导入子组件 - 使用defineAsyncComponent进行更高效的动态导入
const MessageSection = defineAsyncComponent(() => 
  import(/* webpackChunkName: "dashboard-messages" */ "./MessageSection.vue")
);
const DdlSection = defineAsyncComponent(() => 
  import(/* webpackChunkName: "dashboard-ddl" */ "./DdlSection.vue")
);
const CalendarSection = defineAsyncComponent(() => 
  import(/* webpackChunkName: "dashboard-calendar" */ "./CalendarSection.vue")
);
const ModalDialogs = defineAsyncComponent(() => 
  import(/* webpackChunkName: "dashboard-modals" */ "./ModalDialogs.vue")
);
const AuthModal = defineAsyncComponent({
  loader: () => import(/* webpackChunkName: "auth-modal" */ "@/components/auth/AuthModal.vue"),
  delay: 200,
  timeout: 3000
});

// 初始化router和userStore
const router = useRouter();
const userStore = useUserStore();

// 创建离散API，可以在组件外使用
const { message } = createDiscreteApi(["message", "notification"]);

// 定义观测数据
const Messages = ref<NewsItem[]>([]);
const ddlData = ref<DdlEvent[]>([]);
const loading = ref(true);
const selectedDate = ref(new Date());
let refreshData: (() => Promise<void>) | null = null;

// 登录/注册模态框状态
const showAuthModal = ref(false);

// 用户选项模态框状态
const showUserModal = ref(false);

// 添加DDL对话框状态
const showAddDdlModal = ref(false);
const newDdl = ref({
  title: "",
  dateTimestamp: null as number | null,
  timeTimestamp: null as number | null,
  source: "",
});

// 引入公众号列表
import { gongzhonghao } from "@/resource/map";

// 订阅管理对话框状态
const showSubscriptionModal = ref(false);
const subscriptionStatus = ref<Record<string, boolean>>({});

// 确保订阅状态在父组件中初始化
for (const account of gongzhonghao) {
  subscriptionStatus.value[account] = true; // 默认全部订阅
}

// 下拉菜单选项 - 使用计算属性根据登录状态动态生成
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
function handleModalOption(key: string) {
  debugLog('模态框选项选择', key);
  if (key === "unsubscribe") {
    toggleSubscriptionModal(true);
    showUserModal.value = false;
  } else if (key === "logout") {
    // 处理退出登录逻辑
    if (userStore.isLoggedIn) {
      userStore.logout();
      message.success('已成功退出登录');
    }
    showUserModal.value = false;
  } else if (key === "settings") {
    // 导航到用户设置页面
    router.push('/settings');
    showUserModal.value = false;
  } else if (key === "login") {
    // 显示登录/注册模态框
    showAuthModal.value = true;
    showUserModal.value = false;
  }
  debugLog('处理模态框选项选择', { key });
}

// 切换订阅管理对话框
function toggleSubscriptionModal(show: boolean) {
  debugLog('切换订阅管理对话框', { show });
  showSubscriptionModal.value = show;
}

// 切换添加DDL对话框
function toggleAddDdlModal(show: boolean) {
  debugLog('切换添加DDL对话框', { show });
  showAddDdlModal.value = show;
}

// 更新选定的日期
function updateSelectedDate(date: Date) {
  debugLog('更新选定的日期', { date });
  selectedDate.value = date;
}

// 登录成功处理函数
function handleLoginSuccess() {
  message.success('登录成功');
  showAuthModal.value = false;
  showUserModal.value = false;
  // 如果需要，可以在这里刷新数据
  if (refreshData) {
    refreshData();
  }
}

// 注册成功处理函数
function handleRegisterSuccess() {
  message.success('注册成功并已登录');
  showAuthModal.value = false;
  showUserModal.value = false;
  if (refreshData) {
    refreshData();
  }
}

// 提供方法给子组件
provide("toggleAddDdlModal", toggleAddDdlModal);
provide("toggleSubscriptionModal", toggleSubscriptionModal);
provide("updateSelectedDate", updateSelectedDate);
provide("subscriptionStatus", subscriptionStatus);

// 在组件挂载时异步加载数据
onMounted(async () => {
  try {
    // 检查登录状态
    const response = await fetch('/api/check-login', {
      credentials: 'include'
    });
    const result = await response.json();
    if (response.ok && result.code === 200) {
      userStore.user = result.data;
      userStore.isLoggedIn = true;
    }

    // 异步获取数据
    const dashboardData = await useDashboardData();
    
    // 将非响应式数据转换为响应式数据
    ddlData.value = dashboardData.ddlData;
    Messages.value = dashboardData.Messages;
    refreshData = dashboardData.refreshData;
    
    // 确认订阅状态已经初始化
    debugLog('组件挂载后的订阅状态', { 
      status: subscriptionStatus.value, 
      keys: Object.keys(subscriptionStatus.value) 
    });
  } catch (error) {
    console.error("Failed to load dashboard data:", error);
  } finally {
    loading.value = false;
  }
});

// 组件销毁前的清理工作
onBeforeUnmount(() => {
  debugLog('组件即将销毁', {});
});

// 监听日期变化
watchEffect(() => {
  if (selectedDate.value) {
    debugLog('监听到日期变化', { selectedDate: selectedDate.value });
  }
});

// 创建仪表板状态对象
const dashboardState = {
  Messages,
  ddlData,
  refreshData,
  selectedDate,
  loading,
  message, // 来自 createDiscreteApi
  showAddDdlModal, 
  showSubscriptionModal,
  newDdl,
  subscriptionStatus,
  toggleAddDdlModal,
  toggleSubscriptionModal,
  updateSelectedDate
};

// 导出单个状态和整个状态对象给子组件
provide("Messages", Messages);
provide("ddlData", ddlData); 
provide("refreshData", refreshData);
provide("selectedDate", selectedDate);
provide("dashboardState", dashboardState);
</script>

<style scoped>
.dashboard-grid {
  margin: 16px;
  margin-top: 60px;
}

.user-avatar-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: #f0f0f0;
  cursor: pointer;
  transition: background-color 0.3s;
}

.user-avatar-wrapper:hover {
  background-color: #e0e0e0;
}

/* 用户模态框样式 */
.user-modal-header {
  display: flex;
  align-items: center;
  padding-bottom: 16px;
}

.user-avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background-color: #f0f0f0;
}

.user-info {
  margin-left: 16px;
}

.user-name {
  font-weight: 600;
  font-size: 16px;
  margin-bottom: 4px;
}

.user-status {
  font-size: 12px;
  color: #999;
}

.user-modal-divider {
  height: 1px;
  background-color: rgba(0, 0, 0, 0.06);
  margin: 8px 0 16px 0;
}

.user-modal-options {
  width: 100%;
}

.user-option-button {
  text-align: left;
  padding: 10px 0;
  font-size: 14px;
  width: 100%;
  transition: background-color 0.2s;
  border-radius: 4px;
}

.user-option-button:hover {
  background-color: rgba(0, 0, 0, 0.04);
}
</style>
