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
      style="max-width: 600px"
      size="medium"
    >
      <div class="subscription-list">
        <!-- 未登录用户提示登录 -->
        <div class="login-hint" v-if="!userStore.isLoggedIn">
          <n-alert type="info" title="提示">
            登录后可以永久保存您的订阅设置
            <div style="margin-top: 8px">
              <n-button text type="primary" @click="showAuthModal = true">
                去登录
              </n-button>
            </div>
          </n-alert>
        </div>

        <!-- 已登录用户显示保存按钮 -->
        <div v-if="userStore.isLoggedIn" class="form-actions"></div>

        <!-- 所有用户都使用列表，但只有未登录用户显示取消订阅按钮 -->
        <n-space vertical class="account-list">
          <div
            v-for="(account, index) in subscribedAccounts"
            :key="index"
            class="subscription-item"
          >
            <span class="account-name">{{ account }}</span>
            <!-- 只有未登录用户显示取消订阅按钮 -->
            <n-button
              quaternary
              circle
              size="small"
              @click="unsubscribeAccount(account)"
              class="delete-btn"
            >
              <n-icon><close-icon /></n-icon>
            </n-button>
          </div>
        </n-space>
      </div>
    </n-modal>

    <!-- 登录/注册模态框 -->
    <auth-modal
      v-model:show="showAuthModal"
      initial-tab="login"
      @login-success="handleLoginSuccess"
      @register-success="handleRegisterSuccess"
    />
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
  NTransfer,
  NAlert,
} from "naive-ui";
import { CloseOutline as CloseIcon } from "@vicons/ionicons5";
import { useUserStore } from "@/stores/userStore";
import { useDashboardStore } from "../../stores/dashboardStore";
import dayjs from "dayjs";
import type { DdlEvent } from "../../stores/dashboardStore";
import type { DateString } from "@/utils/DateString";
import { gongzhonghao } from "@/resource/map";
import { defineAsyncComponent } from "vue";
const AuthModal = defineAsyncComponent(
  () => import("@/components/auth/AuthModal.vue")
);
// 初始化 userStore 和 router
const userStore = useUserStore();
const showAuthModal = ref(false);

// 注入共享状态，使用更明确的类型标注
const dashboardState = inject("dashboardState") as {
  ddlData: { value: DdlEvent[] };
  selectedDate: { value: Date };
  loading: { value: boolean };
  message: {
    success: (text: string) => void;
    error: (text: string) => void;
    info: (text: string) => void;
  };
  showSubscriptionModal: { value: boolean };
  showAddDdlModal: { value: boolean };
  newDdl: {
    value: {
      title: string;
      dateTimestamp: number | null;
      timeTimestamp: number | null;
      source: string;
    };
  };
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
  subscriptionStatus,
} = dashboardState;

// 父组件已经完成初始化，这里不需要重复
// 添加调试日志以检查订阅状态
debugLog("当前订阅状态", subscriptionStatus.value);

// 公众号列表
const gongzhonghaoList = computed(() => {
  return gongzhonghao;
});

// 获取已订阅的账号列表
const subscribedAccounts = computed(() => {
  return Object.keys(subscriptionStatus.value).filter(
    (account) => subscriptionStatus.value[account]
  );
});

// 取消订阅某个账号
async function unsubscribeAccount(account: string) {
  try {
    debugLog("取消订阅", account);
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
    console.error("取消订阅失败:", error);
    message.error("取消订阅失败，请重试");
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
  },
});

// 使用computed，并添加详细的日志记录
const subscriptionModalVisible = computed({
  get() {
    debugLog("访问 subscriptionModalVisible", showSubscriptionModal.value);
    return showSubscriptionModal.value;
  },
  set(value) {
    debugLog("设置 subscriptionModalVisible", {
      newValue: value,
      oldValue: showSubscriptionModal.value,
    });
    showSubscriptionModal.value = value;
  },
});

// 监视订阅对话框的状态变化
watchEffect(() => {
  debugLog("模态组件内订阅对话框状态", showSubscriptionModal.value);
});

// 处理表单模型的计算属性
const ddlForm = computed({
  get: () => newDdl.value,
  set: (value) => {
    newDdl.value = value;
  },
});

// 提交新的DDL
async function submitNewDdl() {
  try {
    if (!ddlForm.value.title || !ddlForm.value.dateTimestamp) {
      message.error("标题和日期不能为空");
      return;
    }

    // 创建新的DDL项，合并日期和时间
    let dateTime = dayjs(ddlForm.value.dateTimestamp);
    
    // 如果有时间，则合并日期和时间
    if (ddlForm.value.timeTimestamp) {
      const timeObj = dayjs(ddlForm.value.timeTimestamp);
      // 从时间对象中提取小时和分钟，并设置到日期对象中
      dateTime = dateTime
        .hour(timeObj.hour())
        .minute(timeObj.minute())
        .second(0);
    } else {
      // 如果没有设置时间，默认设置为00:00:00
      dateTime = dateTime.hour(0).minute(0).second(0);
    }
    
    const newDdlItem: DdlEvent = {
      summary: {
        title: ddlForm.value.title,
        time: dateTime,
      },
    };

    // 使用store的addCustomDdl方法调用后端API
    loading.value = true;
    const result = await useUserStore().addCustomDdl(newDdlItem);
    const dashboardStore = useDashboardStore();
    if (result.success) {
      message.success("DDL添加成功");
      addDdlModalVisible.value = false;

      // 添加成功后立即刷新当前日期的数据
      const selectedDateStr = dayjs(selectedDate.value).format("YYYY-MM-DD");
      const newDdlDateStr = newDdlItem.summary.time?.format("YYYY-MM-DD");

      // 直接添加新DDL到当前数据集，以实现即时显示效果
      if (selectedDateStr === newDdlDateStr) {
        // 检查是否已存在相同的DDL（防止重复）
        const exists = ddlData.value.some(
          (item) =>
            item.summary.title === newDdlItem.summary.title &&
            item.summary.time?.format("YYYY-MM-DD") === newDdlDateStr
        );

        if (!exists) {
          // 添加完整的DDL项目，确保时间信息正确，添加到数组开头而不是末尾
          ddlData.value.unshift({
            summary: {
              title: newDdlItem.summary.title,
              time: newDdlItem.summary.time,
            },
          });
          console.log("Added new DDL to current dashboard at the beginning:", newDdlItem);
        }
      }

      // 保存当前添加的DDL，以确保它不会在刷新数据时丢失
      const addedDdl = { ...newDdlItem };

      // 后台异步刷新所有数据，确保与服务器保持同步
      // 添加小延迟，确保后端有时间处理添加的DDL
      const formattedDate = dayjs(selectedDate.value).format(
        "YYYY-MM-DD"
      ) as DateString;

      // 延迟500毫秒再刷新数据，给后端API处理时间
      setTimeout(() => {
        dashboardStore.fetchDdlData(formattedDate).then(() => {
          // 更新本地数据，但保留刚添加的DDL
          const freshDdlData = [...dashboardStore.ddlData];

          // 检查新添加的DDL是否已存在于刷新后的数据中
          const ddlExists = freshDdlData.some(
            (item) =>
              item.summary.title === addedDdl.summary.title &&
              item.summary.time?.format("YYYY-MM-DD") ===
                addedDdl.summary.time?.format("YYYY-MM-DD")
          );

          // 如果不存在（服务器尚未返回），则添加到本地数据的开头
          if (!ddlExists && selectedDateStr === newDdlDateStr) {
            freshDdlData.unshift(addedDdl);
          }

          // 更新本地数据
          ddlData.value = freshDdlData;
        });
      }, 500);
    } else {
      message.error(result.error || "DDL添加失败，请稍后再试");
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

// 登录成功处理
const handleLoginSuccess = () => {
  message.success("登录成功");
  // 刷新订阅状态，将来可以从用户设置中读取
  // 这里可以根据需要添加其他逻辑
};

// 注册成功处理
const handleRegisterSuccess = () => {
  message.success("注册成功");
  // 注册成功后的逻辑
};

// onMounted 钩子，用于组件挂载后执行的逻辑
onMounted(() => {
  debugLog("ModalDialogs组件已挂载，初始模态框状态", {
    showSubscriptionModal: showSubscriptionModal.value,
    subscriptionModalVisible: subscriptionModalVisible.value,
  });

  // 检查订阅状态是否正确初始化
  debugLog("订阅状态", {
    status: subscriptionStatus.value,
    keys: Object.keys(subscriptionStatus.value),
    firstAccount: gongzhonghao[0],
    firstStatus: subscriptionStatus.value[gongzhonghao[0]],
  });
});
</script>

<style scoped>
.subscription-list {
  max-height: 400px;
  overflow-y: auto;
  padding: 4px 0;
}

.login-hint {
  margin-bottom: 16px;
}

.account-list {
  width: 100%;
  margin-top: 16px;
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

.form-actions {
  display: flex;
  justify-content: flex-end;
  margin: 16px 0;
}
</style>
