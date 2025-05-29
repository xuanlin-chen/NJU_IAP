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
import type { Message } from "../../stores/dashboardStore";

// 注入共享状态
const { Messages, message } = inject("dashboardState") as {
  Messages: { value: Message[] };
  message: any;
};

// 转换 Messages 为 CardItem 类型
const formattedMessages = computed(() => {
  if (!Messages.value || Messages.value.length === 0) return [];
  return Messages.value.map((message: Message) => {
    // 处理 source 字段，如果是 URL 类型就转换为字符串
    let sourceStr = "";
    if (message.source) {
      if (typeof message.source === "string") {
        sourceStr = message.source;
      } else {
        // 是 URL 对象
        sourceStr = message.source.href;
      }
    }

    return {
      title: message.title || "",
      time: message.time || "",
      abstract: message.abstract || "",
      type: message.type || "",
      source: sourceStr,
    };
  });
});

// 事件组
const itemGroups = computed(() => {
  const groups: ItemGroup[] = [];

  for (const type of eventTypes) {
    const filteredItems = formattedMessages.value.filter(
      (item: CardItem) => item.type === type
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
