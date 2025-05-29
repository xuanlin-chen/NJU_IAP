<template>
  <n-notification-provider>
    <div>
      <n-spin :show="loading">
        <n-grid :cols="12" :x-gap="16" :y-gap="16" class="dashboard-grid">
          <!-- 用户头像 -->
          <n-grid-item :span="1">
            <n-dropdown trigger="click" @select="handleDropdownSelect" :options="dropdownOptions">
              <div class="user-avatar-wrapper">
                <AccountIcon />
              </div>
            </n-dropdown>
          </n-grid-item>
          
          <!-- 左侧区域 -->
          <n-grid-item :span="5">
            <MessageSection />
          </n-grid-item>

          <!-- 右侧区域 -->
          <n-grid-item :span="4">
            <!-- DDL提醒部分 -->
            <DdlSection />
            
            <!-- 日历部分 -->
            <CalendarSection />
          </n-grid-item>
        </n-grid>
      </n-spin>

      <!-- 对话框组件 -->
      <ModalDialogs />
    </div>
  </n-notification-provider>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, provide, watchEffect } from "vue";
import {
  NGrid,
  NGridItem,
  NSpin,
  NNotificationProvider,
  NDropdown,
  createDiscreteApi
} from "naive-ui";
import { debugLog } from "../../utils/debug";
import { useDashboardData } from "../../stores/dashboardStore";
import AccountIcon from "@/components/icons/AccountIcon.vue";
import type { DdlItem, Message } from "../../stores/dashboardStore";

// 导入子组件
import MessageSection from "./MessageSection.vue";
import DdlSection from "./DdlSection.vue";
import CalendarSection from "./CalendarSection.vue";
import ModalDialogs from "./ModalDialogs.vue";

// 创建状态容器
const ddlData = ref<DdlItem[]>([]);
const Messages = ref<Message[]>([]);
const loading = ref(true);
const selectedDate = ref(new Date());
let refreshData: (() => Promise<void>) | null = null;

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

// 下拉菜单选项
const dropdownOptions = [
  {
    label: "个人设置",
    key: "settings",
  },
  {
    label: "退出登录",
    key: "logout",
  },
  {
    label: "退订消息",
    key: "unsubscribe",
  },
];

// 处理下拉菜单选择
function handleDropdownSelect(key: string) {
  debugLog('下拉菜单选择', key);
  if (key === "unsubscribe") {
    toggleSubscriptionModal(true);
  } else if (key === "logout") {
    // 处理退出登录逻辑
    console.log("用户选择了退出登录");
  } else if (key === "settings") {
    // 处理个人设置逻辑
    console.log("用户选择了个人设置");
  }
  debugLog('处理下拉菜单选择', { key });
}

// 创建离散API，可以在组件外使用
const { message } = createDiscreteApi(["message", "notification"]);

// 在组件挂载时异步加载数据
onMounted(async () => {
  try {
    // 异步获取数据
    const dashboardData = await useDashboardData();
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
  loading.value = false;
  // 如果有其他事件监听器或计时器，这里也应该清理它们
});

// 定义控制模态框的操作方法
const toggleSubscriptionModal = (value: boolean) => {
  debugLog('toggleSubscriptionModal 被调用', {value, current: showSubscriptionModal.value});
  showSubscriptionModal.value = value;
};

// 监视订阅对话框的状态变化
watchEffect(() => {
  debugLog('订阅模态框状态变化', showSubscriptionModal.value);
});

// 将共享状态提供给子组件
provide("dashboardState", {
  ddlData,
  Messages,
  loading,
  selectedDate,
  refreshData,
  message,
  showSubscriptionModal,
  showAddDdlModal,
  newDdl,
  subscriptionStatus,
  // 提供直接操作方法
  toggleSubscriptionModal
});
</script>

<style scoped>
.dashboard-grid {
  margin-top: 20px;
  width: 100%;
  max-width: 1600px;
  margin-right: auto;
  box-sizing: border-box;
  display: flex;
  gap: 24px;
}

.user-avatar-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  padding: 6px;
  border-radius: 50%;
  transition: background-color 0.2s;
}

.user-avatar-wrapper:hover {
  background-color: rgba(0, 0, 0, 0.05);
}
</style>
