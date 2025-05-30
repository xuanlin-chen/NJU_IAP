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
import { useRouter } from "vue-router";
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
import { useUserStore } from "../../stores/userStore";
import AccountIcon from "@/components/icons/AccountIcon.vue";
import type { DdlItem, Message } from "../../stores/dashboardStore";

// 导入子组件
import MessageSection from "./MessageSection.vue";
import DdlSection from "./DdlSection.vue";
import CalendarSection from "./CalendarSection.vue";
import ModalDialogs from "./ModalDialogs.vue";

// 初始化router和userStore
const router = useRouter();
const userStore = useUserStore();

// 创建离散API，可以在组件外使用
const { message } = createDiscreteApi(["message", "notification"]);

// 定义观测数据
const Messages = ref<Message[]>([]);
const ddlData = ref<DdlItem[]>([]);
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
    if (userStore.isLoggedIn) {
      userStore.logout();
      message.success('已成功退出登录');
    }
  } else if (key === "settings") {
    // 导航到用户设置页面
    router.push('/settings');
  }
  debugLog('处理下拉菜单选择', { key });
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

// 提供方法给子组件
provide("toggleAddDdlModal", toggleAddDdlModal);
provide("toggleSubscriptionModal", toggleSubscriptionModal);
provide("updateSelectedDate", updateSelectedDate);
provide("subscriptionStatus", subscriptionStatus);

// 在组件挂载时异步加载数据
onMounted(async () => {
  try {
    // 异步获取数据
    const dashboardData = await useDashboardData();
    
    // 将非响应式数据转换为响应式数据
    ddlData.value = dashboardData.ddlData;
    Messages.value = dashboardData.Messages;
    refreshData = dashboardData.refreshData;
    
    // 不需要更新 dashboardState，因为它已经引用了正确的响应式对象
    // dashboardState 中的引用在初始化时已经建立，不需要再赋值
    
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
</style>
