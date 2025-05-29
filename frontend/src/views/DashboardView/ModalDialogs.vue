<template>
  <div>
    <!-- DDL添加对话框 -->
    <n-modal
      v-model:show="addDdlModalVisible"
      preset="card"
      title="添加DDL"
      style="max-width: 450px"
      size="medium"
    >
      <n-form
        :model="ddlForm"
        label-placement="left"
        label-width="auto"
        :style="{ maxWidth: '100%' }"
      >
        <n-form-item label="标题" path="title">
          <n-input v-model:value="ddlForm.title" placeholder="请输入DDL标题" />
        </n-form-item>
        <n-form-item label="日期" path="date">
          <n-date-picker
            v-model:value="ddlForm.dateTimestamp"
            type="date"
            clearable
            style="width: 100%"
          />
        </n-form-item>
        <n-form-item label="时间" path="time">
          <n-time-picker
            v-model:value="ddlForm.timeTimestamp"
            format="HH:mm"
            clearable
            style="width: 100%"
          />
        </n-form-item>
        <n-form-item label="来源链接" path="source">
          <n-input
            v-model:value="ddlForm.source"
            placeholder="请输入链接（可选）"
          />
        </n-form-item>
        <div
          style="
            display: flex;
            justify-content: flex-end;
            gap: 12px;
            margin-top: 24px;
          "
        >
          <n-button @click="addDdlModalVisible = false">取消</n-button>
          <n-button
            type="primary"
            @click="submitNewDdl"
            :disabled="!ddlForm.title || !ddlForm.dateTimestamp"
          >
            添加
          </n-button>
        </div>
      </n-form>
    </n-modal>

    <!-- 公众号订阅管理对话框 -->
    <n-modal
      v-model:show="subscriptionModalVisible"
      preset="card"
      title="公众号订阅管理"
      style="max-width: 500px"
      size="medium"
    >
      <div class="subscription-list">
        <n-space vertical>
          <div
            v-for="(account, index) in subscribedAccounts"
            :key="index"
            class="subscription-item"
          >
            <span class="account-name">{{ account }}</span>
            <n-button quaternary circle size="small" @click="unsubscribeAccount(account)" class="delete-btn">
              <n-icon><close-icon /></n-icon>
            </n-button>
          </div>
        </n-space>
      </div>
    </n-modal>
  </div>
</template>

<script setup lang="ts">
import { computed, inject, onMounted, ref, watchEffect } from "vue";
import { debugLog } from "../../utils/debug";
import {
  NModal,
  NForm,
  NFormItem,
  NInput,
  NDatePicker,
  NTimePicker,
  NButton,
  NSpace,
  NIcon,
} from "naive-ui";
import { CloseOutline as CloseIcon } from "@vicons/ionicons5";
import { useDashboardStore } from "../../stores/dashboardStore";
import dayjs from "dayjs";
import type { DdlItem } from "../../stores/dashboardStore";
import type { DateString } from "@/utils/DateString";
import { gongzhonghao } from "@/resource/map";

// 注入共享状态，使用更明确的类型标注
const dashboardState = inject("dashboardState") as {
  ddlData: { value: DdlItem[] };
  selectedDate: { value: Date };
  loading: { value: boolean };
  message: {
    success: (text: string) => void;
    error: (text: string) => void;
    info: (text: string) => void;
  };
  showSubscriptionModal: { value: boolean };
  showAddDdlModal: { value: boolean };
  newDdl: { value: {
    title: string;
    dateTimestamp: number | null;
    timeTimestamp: number | null;
    source: string;
  }};
  subscriptionStatus: { value: Record<string, boolean> };
  toggleSubscriptionModal: (value: boolean) => void;
};

// 解构以便更容易使用
const {
  ddlData,
  selectedDate,
  loading,
  message,
  showSubscriptionModal,
  showAddDdlModal,
  newDdl,
  subscriptionStatus
} = dashboardState;

// 父组件已经完成初始化，这里不需要重复
// 添加调试日志以检查订阅状态
debugLog('当前订阅状态', subscriptionStatus.value);

// 公众号列表
const gongzhonghaoList = computed(() => {
  return gongzhonghao;
});

// 获取已订阅的账号列表
const subscribedAccounts = computed(() => {
  return Object.keys(subscriptionStatus.value).filter(account => 
    subscriptionStatus.value[account]
  );
});

// 取消订阅某个账号
async function unsubscribeAccount(account: string) {
  try {
    debugLog('取消订阅', account);
    subscriptionStatus.value[account] = false;
    
    // TODO: 调用后端API保存设置
    // const dashboardStore = useDashboardStore();
    // await dashboardStore.updateSubscription(account, false);
    
    message.success(`已取消订阅: ${account}`);
    
    // 如果没有任何订阅了，关闭对话框
    if (subscribedAccounts.value.length === 0) {
      subscriptionModalVisible.value = false;
    }
  } catch (error) {
    console.error('取消订阅失败:', error);
    message.error('取消订阅失败，请重试');
    // 恢复状态
    subscriptionStatus.value[account] = true;
  }
}

// 计算属性，用于将 ref.value 转换为直接值用于 v-model
const addDdlModalVisible = computed({
  get() {
    return showAddDdlModal.value;
  },
  set(value) {
    showAddDdlModal.value = value;
  }
});

// 使用computed，并添加详细的日志记录
const subscriptionModalVisible = computed({
  get() {
    debugLog('访问 subscriptionModalVisible', showSubscriptionModal.value);
    return showSubscriptionModal.value;
  },
  set(value) {
    debugLog('设置 subscriptionModalVisible', {newValue: value, oldValue: showSubscriptionModal.value});
    showSubscriptionModal.value = value;
  }
});

// 监视订阅对话框的状态变化
watchEffect(() => {
  debugLog('模态组件内订阅对话框状态', showSubscriptionModal.value);
});

// 处理表单模型的计算属性
const ddlForm = computed({
  get: () => newDdl.value,
  set: (value) => {
    newDdl.value = value;
  }
});

// 提交新的DDL
async function submitNewDdl() {
  try {
    if (!ddlForm.value.title || !ddlForm.value.dateTimestamp) {
      message.error("标题和日期不能为空");
      return;
    }

    // 创建新的DDL项
    const newDdlItem: DdlItem = {
      title: ddlForm.value.title,
      date: dayjs(ddlForm.value.dateTimestamp),
      time: ddlForm.value.timeTimestamp
        ? dayjs(ddlForm.value.timeTimestamp)
        : dayjs(new Date()),
      source: ddlForm.value.source || "",
    };

    // 使用store的addCustomDdl方法调用后端API
    loading.value = true;
    const dashboardStore = useDashboardStore();
    const result = await dashboardStore.addCustomDdl(newDdlItem);

    if (result) {
      message.success("DDL添加成功");
      addDdlModalVisible.value = false;

      // 重新加载当前日期的DDL数据
      const formattedDate = dayjs(selectedDate.value).format(
        "YYYY-MM-DD"
      ) as DateString;
      await dashboardStore.fetchDdlData(formattedDate);
      ddlData.value = dashboardStore.ddlData;
    } else {
      message.error("DDL添加失败，请稍后再试");
    }
  } catch (error) {
    console.error("添加DDL失败:", error);
    message.error("添加DDL失败");
  } finally {
    loading.value = false;
  }
}

// 保存订阅设置
async function saveSubscriptionSettings() {
  try {
    loading.value = true;

    // TODO: 与后端集成，保存订阅设置
    // const dashboardStore = useDashboardStore();
    // const result = await dashboardStore.saveSubscriptionSettings(subscriptionStatus.value);
    
    // 临时实现，直接显示成功
    const result = true;

    if (result) {
      message.success("订阅设置已保存");
      subscriptionModalVisible.value = false;
      // 不需要单独设置showSubscriptionModal，因为computed setter会处理
    } else {
      message.error("保存订阅设置失败");
    }
  } catch (error) {
    console.error("保存订阅设置失败:", error);
    message.error("保存订阅设置失败");
  } finally {
    loading.value = false;
  }
}

// onMounted 钩子，用于组件挂载后执行的逻辑
onMounted(() => {
  debugLog('ModalDialogs组件已挂载，初始模态框状态', {
    showSubscriptionModal: showSubscriptionModal.value,
    subscriptionModalVisible: subscriptionModalVisible.value
  });
  
  // 检查订阅状态是否正确初始化
  debugLog('订阅状态', {
    status: subscriptionStatus.value,
    keys: Object.keys(subscriptionStatus.value),
    firstAccount: gongzhonghao[0],
    firstStatus: subscriptionStatus.value[gongzhonghao[0]]
  });
});
</script>

<style scoped>
.subscription-list {
  max-height: 400px;
  overflow-y: auto;
  padding: 4px 0;
}

.subscription-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 12px;
  border-radius: 4px;
  margin-bottom: 8px;
  background-color: rgba(0, 0, 0, 0.02);
  transition: background-color 0.2s ease;
}

.subscription-item:hover {
  background-color: rgba(0, 0, 0, 0.05);
}

.account-name {
  font-size: 14px;
  flex-grow: 1;
}

.delete-btn {
  color: rgba(0, 0, 0, 0.45);
  transition: color 0.2s ease;
}

.delete-btn:hover {
  color: #ff4d4f;
}
</style>
