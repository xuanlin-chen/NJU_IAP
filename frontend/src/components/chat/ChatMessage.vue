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
import { marked } from 'marked'

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

// 格式化消息内容
const formattedContent = computed(() => {
  // 对AI回复使用marked库进行完整的Markdown格式化
  if (props.role === 'assistant') {
    return marked(props.content, { 
      gfm: true, // GitHub Flavored Markdown
      breaks: true // 识别回车为换行
    });
  }
  
  // 用户和系统消息使用简单的格式化
  let formatted = props.content.replace(/\n/g, '<br>')
  formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
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

.message-content :deep(pre) {
  background-color: #f5f5f5;
  padding: 12px;
  border-radius: 6px;
  overflow-x: auto;
  margin: 12px 0;
}

.message-content :deep(code) {
  font-family: monospace;
  background-color: #f5f5f5;
  padding: 2px 4px;
  border-radius: 3px;
  font-size: 0.9em;
}

.message-content :deep(p) {
  margin: 8px 0;
}

.message-content :deep(ul), .message-content :deep(ol) {
  margin: 8px 0;
  padding-left: 24px;
}

.message-content :deep(table) {
  border-collapse: collapse;
  width: 100%;
  margin: 16px 0;
}

.message-content :deep(th), .message-content :deep(td) {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

.message-content :deep(th) {
  background-color: #f5f5f5;
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