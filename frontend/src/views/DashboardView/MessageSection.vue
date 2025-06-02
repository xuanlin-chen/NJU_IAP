<template>
  <div style="position: relative" class="message-section">
    <!-- 消息 -->
    <base-card
      :title="dashboardText.dayMessages.title"
      :item-groups="itemGroups"
      date-field="time"
      extra-field="source"
      :empty-text="dashboardText.dayMessages.noMessages"
      :view-more-text="dashboardText.dayMessages.viewMore"
      @view-more="handleViewMoreToday"
      class="message-card"
    />
  </div>
</template>

<script setup lang="ts">
import { computed, inject } from "vue";
import dashboardText from "../../resource/dashboard";
import { eventTypes } from "@/resource/map";
import type { CardItem, ItemGroup } from "../../components/BaseCard.vue";
import BaseCard from "../../components/BaseCard.vue";
import type { NewsItem } from "../../stores/dashboardStore";

// 注入共享状态
const dashboardState = inject("dashboardState") as {
  Messages: { value: NewsItem[] };
  message: {
    success: (text: string) => void;
    error: (text: string) => void;
    info: (text: string) => void;
  };
};

// 解构以便更容易使用
const { Messages, message } = dashboardState;

// 转换 Messages 为 CardItem 类型
const formattedMessages = computed(() => {
  if (!Messages.value || Messages.value.length === 0) return [];
  return Messages.value.map((message: NewsItem) => {
    const sourceStr = message.summary?.source
      ? typeof message.summary.source === "string"
        ? message.summary.source
        : String(message.summary.source)
      : "";
    return {
      title: message.summary?.title || "",
      time: message.date || "",
      abstract: message.abstract || "",
      eventType: message.summary?.type || "", // store the type as eventType
      source: sourceStr,
      keywords: message.summary?.keywords || "", // 添加关键词
      link: sourceStr, // 添加原文链接，使用source作为链接
    } as CardItem;
  });
});

// 事件组
const itemGroups = computed(() => {
  const groups: ItemGroup[] = [];

  for (const type of eventTypes) {
    const filteredItems = formattedMessages.value.filter(
      (item) => item.eventType === type
    );

    if (filteredItems.length > 0) {
      groups.push({
        groupTitle: type,
        items: filteredItems,
      });
    }
  }

  return groups;
});

// 处理"查看更多"点击事件
function handleViewMoreToday() {
  message.info("查看更多今日消息");
}
</script>

<style scoped>
.message-section {
  transition: all 0.3s ease;
}

.message-section:hover {
  transform: translateY(-2px);
}

.message-card {
  border-radius: 12px;
  overflow: hidden;
}

/* 自定义消息组样式 */
:deep(.n-collapse-item) {
  margin-bottom: 8px;
  border-radius: 8px;
  overflow: hidden;
  transition: all 0.2s ease;
  border-left: 3px solid transparent;
}

:deep(.n-collapse-item:hover) {
  background-color: rgba(245, 245, 250, 0.5);
}

/* 根据不同的消息类型设置不同的边框颜色 */
:deep(.n-collapse-item:nth-child(1)) {
  border-left-color: #8052da; /* 紫色 - 主要消息 */
}

:deep(.n-collapse-item:nth-child(2)) {
  border-left-color: #52b788; /* 绿色 - 活动消息 */
}

:deep(.n-collapse-item:nth-child(3)) {
  border-left-color: #f77f00; /* 橙色 - 通知消息 */
}

:deep(.n-collapse-item:nth-child(4)) {
  border-left-color: #3a86ff; /* 蓝色 - 其他类型 */
}

:deep(.n-collapse-item:nth-child(5)) {
  border-left-color: #ef476f; /* 粉色 - 其他类型 */
}

/* 消息标题样式 */
:deep(.n-collapse-item__header) {
  padding: 12px 16px;
  font-weight: 500;
  transition: background-color 0.2s ease;
}

:deep(.n-collapse-item__header:hover) {
  background-color: rgba(245, 245, 250, 0.8);
}

/* 消息内容样式 */
:deep(.item) {
  padding: 12px 16px;
  border-bottom: 1px solid #f0f0f0;
  transition: all 0.2s ease;
}

:deep(.item:last-child) {
  border-bottom: none;
}

:deep(.item:hover) {
  background-color: rgba(245, 245, 250, 0.3);
}

:deep(.item-title) {
  font-size: 14px;
  font-weight: 500;
  color: #333;
  margin-bottom: 8px;
  transition: color 0.2s ease;
}

:deep(.item-title:hover) {
  color: #8052da;
}

:deep(.item-footer) {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12px;
  color: #888;
}

:deep(.view-details-link) {
  color: #8052da;
  cursor: pointer;
  transition: all 0.2s ease;
  font-weight: 500;
}

:deep(.view-details-link:hover) {
  color: #6039b0;
  text-decoration: underline;
}

/* 空状态样式 */
:deep(.no-data) {
  padding: 24px;
  text-align: center;
  color: #999;
  font-size: 14px;
  background-color: rgba(245, 245, 250, 0.5);
  border-radius: 8px;
}
</style>
