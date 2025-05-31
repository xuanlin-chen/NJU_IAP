<template>
  <div style="position: relative">
    <!-- 消息 -->
    <base-card
      :title="dashboardText.dayMessages.title"
      :item-groups="itemGroups"
      date-field="time"
      extra-field="source"
      :empty-text="dashboardText.dayMessages.noMessages"
      :view-more-text="dashboardText.dayMessages.viewMore"
      @view-more="handleViewMoreToday"
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
/* 消息部分的特定样式可以放在这里 */
</style>
