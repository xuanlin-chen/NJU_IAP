<template>
  <transition name="slide-up" appear>
    <div class="chat-input-container">
      <div class="input-container-wrapper">
        <div class="input-wrapper">
          <n-input 
            v-model:value="inputValue"
            type="textarea" 
            :autosize="{ minRows: 1, maxRows: 4 }"
            :placeholder="chatResource.placeholder"
            @keydown.enter.prevent="sendMessage"
            class="input-field"
          />
          <div class="input-actions">
            <n-button 
              type="primary" 
              :disabled="!inputValue.trim()" 
              @click="sendMessage"
              :class="{ 'button-active': inputValue.trim() }"
            >
              {{ chatResource.send }}
            </n-button>
            <!-- 添加插槽 -->
            <slot name="append"></slot>
          </div>
        </div>
        <div class="chat-footer">
          <small>内容由 AI 生成，请勿完全依赖</small>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { NButton, NInput } from 'naive-ui'
import chatResource from '../../resource/chat'

const inputValue = ref('')

const emit = defineEmits(['send'])

function sendMessage() {
  if (!inputValue.value.trim()) return
  
  emit('send', inputValue.value)
  inputValue.value = ''
}
</script>

<style scoped>
.chat-input-container {
  padding: 16px 0;
  background-color: #fff;
  border-top: 1px solid #e5e7eb;
  position: relative;
  display: flex;
  justify-content: center;
}

.input-container-wrapper {
  width: 100%;
  max-width: 768px;
  padding: 0 24px;
}

.input-wrapper {
  display: flex;
  align-items: flex-end;
  gap: 12px;
}

.input-field {
  transition: box-shadow 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.input-field:focus-within {
  box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.2);
}

/* 添加非线性光标移动动画 */
:deep(.n-input__textarea-el) {
  caret-color: #1890ff;
}

:deep(.n-input__textarea-el),
:deep(.n-input__input-el) {
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
  caret-shape: block;
}

/* 自定义光标动画 */
@keyframes cursor-pulse {
  0% { caret-color: rgba(24, 144, 255, 1); }
  50% { caret-color: rgba(24, 144, 255, 0.6); }
  100% { caret-color: rgba(24, 144, 255, 1); }
}

/* 针对Webkit浏览器的光标动画 */
@supports (-webkit-appearance: none) {
  :deep(.n-input__textarea-el),
  :deep(.n-input__input-el) {
    scroll-behavior: smooth;
    scroll-padding: 10px;
    animation: cursor-pulse 1s infinite;
  }
  
  :deep(.n-input__textarea-el)::selection,
  :deep(.n-input__input-el)::selection {
    background-color: rgba(24, 144, 255, 0.2);
  }
}

/* 添加打字时输入框的微妙动画效果 */
:deep(.n-input__textarea-el:focus),
:deep(.n-input__input-el:focus) {
  animation: subtle-typing 0.3s ease-out;
}

@keyframes subtle-typing {
  0% { transform: scale(1); }
  50% { transform: scale(1.002); }
  100% { transform: scale(1); }
}

.input-actions {
  margin-bottom: 8px;
  display: flex;
  align-items: center;
}

.button-active {
  animation: pulse-light 2s infinite;
}

.chat-footer {
  margin-top: 12px;
  text-align: center;
  color: #999;
}

/* 输入框的过渡效果 */
.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.slide-up-enter-from,
.slide-up-leave-to {
  opacity: 0;
  transform: translateY(20px);
}

@keyframes pulse-light {
  0% { box-shadow: 0 0 0 0 rgba(24, 144, 255, 0.4); }
  70% { box-shadow: 0 0 0 6px rgba(24, 144, 255, 0); }
  100% { box-shadow: 0 0 0 0 rgba(24, 144, 255, 0); }
}

:deep(.n-input) {
  /* 为输入框添加钝角边框 */
  border-radius: 12px;
}

:deep(.n-button) {
  /* 为发送按钮添加钝角边框 */
  border-radius: 12px;
}
</style>