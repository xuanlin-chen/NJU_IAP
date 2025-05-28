<template>
  <div class="message-container" :class="role">
    <!-- 用户消息 -->
    <div v-if="role === 'user'" class="message-bubble">
      <div v-html="formattedContent" class="message-content"></div>
    </div>
    
    <!-- AI助手消息 -->
    <div v-else-if="role === 'assistant'" class="ai-content-wrapper">
      <div class="ai-content">
        <div v-html="formattedContent" class="message-content"></div>
      </div>
    </div>
    
    <!-- 系统消息 -->
    <div v-else-if="role === 'system'" class="system-content-wrapper">
      <div class="system-content">
        <div v-html="formattedContent" class="message-content"></div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps({
  role: {
    type: String,
    required: true,
    validator: (value: string) => ['user', 'assistant', 'system'].includes(value)
  },
  content: {
    type: String,
    required: true
  }
})

// 格式化消息内容，支持简单的markdown
const formattedContent = computed(() => {
  // 处理换行
  let formatted = props.content.replace(/\n/g, '<br>')
  // 处理加粗
  formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
  // 处理列表
  formatted = formatted.replace(/- (.*?)(?=<br>|$)/g, '• $1')
  return formatted
})
</script>

<style scoped>
.message-container {
  display: flex;
  width: 100%;
  margin: 0;
  gap: 12px;
  align-items: flex-start;
}

.message-container.user {
  justify-content: flex-end;
  padding: 8px 8px 8px 16px; /* Reduced right padding */
  width: 100%;
  max-width: 768px;
  margin: 0 auto;
}

.message-container.ai {
  flex-direction: column;
  padding: 16px 0;
  border-bottom: 1px solid #eaeaea;
  display: flex;
  align-items: center;
}

.message-bubble {
  max-width: 80%;
  word-wrap: break-word;
  padding: 10px 16px;
  /* 修改为钝角边框 */
  border-radius: 16px;
  background-color: #1890ff;
  color: white;
  border-bottom-right-radius: 6px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

/* AI 内容居中但文本左对齐 */
.ai-content-wrapper {
  width: 100%;
  display: flex;
  justify-content: center;
}

.ai-content {
  width: 100%;
  max-width: 768px;
  padding: 0 24px;
  word-wrap: break-word;
  text-align: left;
}

.message-content {
  line-height: 1.6;
}

.ai .message-content {
  font-size: 15px;
}

.user .message-content {
  text-align: left;
}

.ai + .ai {
  border-top: none;
  margin-top: -16px; /* 使连续的AI消息更加紧凑 */
  padding-top: 0;
}

/* 系统消息样式 */
.system {
  margin-bottom: 8px;
  display: flex;
  justify-content: center;
}

.system-content-wrapper {
  max-width: 80%;
}

.system-content {
  background-color: #fff3e0; /* 暖橙色背景 */
  border-radius: 12px;
  padding: 12px 16px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
  font-size: 14px;
  color: #d84315; /* 暖橙色文字 */
  border: 1px solid #ffe0b2;
}
</style>