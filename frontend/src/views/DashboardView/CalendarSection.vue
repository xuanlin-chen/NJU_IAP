<template>
  <!-- 使用 BaseCard 组件显示日历 -->
  <base-card
    :title="dashboardText.calendar.title"
    :is-calendar-mode="true"
    calendar-footer-text="点击查看 DDL"
  >
    <template #calendar>
      <SimpleCalendar
        v-model:value="selectedDate.value"
        :disableFutureDates="true"
        @update:value="handleDateSelect"
      />
    </template>
  </base-card>
</template>

<script setup lang="ts">
import { inject } from "vue";
import BaseCard from "../../components/BaseCard.vue";
import SimpleCalendar from "../../components/SimpleCalendar.vue";
import dashboardText from "../../resource/dashboard";
import { useDashboardStore } from "../../stores/dashboardStore";
import dayjs from "dayjs";
import type { DateString } from "@/utils/DateString";
import type { Message } from "../../stores/dashboardStore";

// 注入共享状态
const { selectedDate, loading, Messages, message } = inject("dashboardState") as {
  selectedDate: { value: Date };
  loading: { value: boolean };
  Messages: { value: Message[] };
  message: {
    info: (text: string) => void;
    error: (text: string) => void;
    success: (text: string) => void;
    warning: (text: string) => void;
  };
};

// 日期选择处理
async function handleDateSelect(date: Date) {
  selectedDate.value = date;

  loading.value = true;
  try {
    // 获取选定日期的消息数据
    const dashboardStore = useDashboardStore();
    const formattedDate = dayjs(date).format("YYYY-MM-DD") as DateString;
    await dashboardStore.fetchMessages(formattedDate);

    // 更新 Messages
    Messages.value = dashboardStore.Messages;
  } catch (error) {
    console.error(
      `Failed to load messages for date ${dayjs(date).format("YYYY-MM-DD")}:`,
      error instanceof Error ? error.message : String(error)
    );
    message.error("无法加载所选日期的消息");
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.calendar-card {
  margin-top: 20px;
  width: 100%;
}

.calendar-container {
  display: flex;
  flex-direction: column;
}

.calendar-footer {
  margin-top: 10px;
  text-align: center;
  font-size: 12px;
  color: #999999;
}
</style>
