<template>
  <div class="chat-sidebar">
    <!-- Logo -->
    <div class="logo">
      <h2>小蓝鲸</h2>
    </div>

    <!-- 开启新对话 按钮 -->
    <div class="new-chat-button">
      <n-button class="new-chat-btn" @click="$emit('new-chat')">
        <div class="btn-content">
          <div class="btn-icon">
            <n-icon>
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                <path
                  fill="currentColor"
                  d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2Z"
                />
              </svg>
            </n-icon>
          </div>
          <span>开启新对话</span>
        </div>
      </n-button>
    </div>

    <!-- 历史对话列表 -->
    <div class="history-container">
      <div class="history-list">
        <div
          v-for="(chat, index) in chatHistory"
          :key="chat.id"
          class="history-item"
          :class="{ active: currentChatIndex === index }"
          @click="$emit('select-chat', index)"
        >
          {{ chat.title }}
          <div class="item-actions">
            <n-button
              quaternary
              circle
              size="small"
              @click.stop="showMoreActions(chat)"
            >
              <template #icon>
                <n-icon>
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                    <path
                      fill="currentColor"
                      d="M12 8c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm0 2c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z"
                    />
                  </svg>
                </n-icon>
              </template>
            </n-button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { NButton, NIcon, NAvatar } from "naive-ui";

interface ChatItem {
  id: string;
  title: string;
  date: Date; // 添加日期属性
}

const props = defineProps({
  chatHistory: {
    type: Array as () => ChatItem[],
    required: true,
  },
  currentChatIndex: {
    type: Number,
    required: true,
  },
});

defineEmits(["new-chat", "select-chat", "delete-chat"]);

// 不需要按日期分组的计算属性

// 显示更多操作菜单
const showMoreActions = (chat: ChatItem) => {
  // 这里可以实现点击省略号按钮后的逻辑，例如显示下拉菜单
  console.log("Show more actions for:", chat.title);
};
</script>

<style scoped>
.chat-sidebar {
  width: 240px;
  background-color: #ffffff;
  display: flex;
  flex-direction: column;
  height: 100%;
  border-top-right-radius: 24px;
  border-bottom-right-radius: 24px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  border-right: 1px solid rgba(0, 0, 0, 0.08);
  color: #333333;
}

.logo {
  padding: 16px 16px 10px 16px;
  border-bottom: none;
}

.logo h2 {
  color: #333;
  font-size: 22px;
  font-weight: 600;
  margin: 0;
}

.new-chat-button {
  padding: 8px 16px;
}

.new-chat-btn {
  width: 100%;
  height: 38px;
  background-color: var(--md-sys-color-surface);
  border: 1px solid var(--md-grey-200);
  border-radius: 12px;
  color: var(--md-primary);
  transition: all 0.2s ease;
}

.new-chat-btn:hover {
  background-color: var(--md-grey-100);
}

.btn-content {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  width: 100%;
}

.btn-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 8px;
  color: var(--md-primary);
}

.history-container {
  flex: 1;
  overflow-y: auto;
  padding: 0 16px;
  margin-top: 10px;
}

/* 删除了日期分组相关样式 */

.history-list {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.history-item {
  padding: 8px 12px;
  border-radius: 10px;
  cursor: pointer;
  font-size: 14px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: all 0.2s ease;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  color: var(--md-grey-800);
}

.history-item.active {
  background-color: var(--md-grey-100);
  color: var(--md-primary);
}

.history-item:hover {
  background-color: var(--md-grey-100);
}

.item-actions {
  opacity: 0;
  transition: opacity 0.2s;
}

.history-item:hover .item-actions {
  opacity: 1;
}
</style>
