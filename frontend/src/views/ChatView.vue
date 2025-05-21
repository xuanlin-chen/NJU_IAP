<template>
  <div class="chat-view-wrapper">
    <div class="chat-container">
      <!-- 聊天侧边栏 -->
      <chat-sidebar
        :chat-history="chatStore.chatHistory"
        :current-chat-index="chatStore.currentChatIndex"
        @new-chat="chatStore.startNewChat"
        @select-chat="chatStore.selectChat"
        @delete-chat="chatStore.deleteChat"
      />
      
      <!-- 主聊天区域 -->
      <div class="chat-main">
        <!-- 聊天头部 -->
        <div class="chat-header">
          <transition name="fade" mode="out-in">
            <h2 :key="chatStore.currentChatIndex">{{ chatStore.currentChat?.title || chatResource.title }}</h2>
          </transition>
        </div>
        
        <!-- 聊天消息区域 -->
        <div class="chat-messages" ref="messagesContainer">
          <!-- 欢迎消息 -->
          <transition name="fade" mode="out-in">
            <welcome-screen
              v-if="chatStore.messages.length === 0"
              @ask-example="chatStore.askExample"
            />
            
            <!-- 聊天消息列表 -->
            <div v-else class="messages-list">
              <transition-group name="message-fade">
                <chat-message
                  v-for="(msg, index) in chatStore.messages"
                  :key="'msg-' + index"
                  :role="msg.role"
                  :content="msg.content"
                />
              </transition-group>
              
              <!-- 正在输入提示 -->
              <transition name="fade">
                <div v-if="chatStore.isTyping" class="ai-typing">
                  <div class="typing-indicator">{{ chatResource.thinking }}</div>
                </div>
              </transition>
            </div>
          </transition>
        </div>
        
        <!-- 输入区域 -->
        <chat-input @send="chatStore.onSendMessage" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import chatResource from '../resource/chat.ts'
import ChatSidebar from '../components/chat/ChatSidebar.vue'
import ChatMessage from '../components/chat/ChatMessage.vue'
import WelcomeScreen from '../components/chat/WelcomeScreen.vue'
import ChatInput from '../components/chat/ChatInput.vue'
import { useChatStore } from '@/stores/chatStore.ts';

// Define the ChatItem type
interface ChatItem {
  id: string;
  title: string;
  messages: { role: string; content: string }[];
  date: Date; // Change 'date' to Date type
}

// Ensure chatStore.chatHistory is typed correctly
const chatStore = useChatStore() as {
  chatHistory: ChatItem[];
  messages: { role: string; content: string }[];
  currentChatIndex: number;
  currentChat: ChatItem | null;
  isTyping: boolean;
  startNewChat: () => void;
  selectChat: (index: number) => void;
  deleteChat: (index: number) => void;
  askExample: () => void;
  onSendMessage: (message: string) => void;
};

// Convert chatHistory dates to Date objects
chatStore.chatHistory = chatStore.chatHistory.map(chat => ({
  ...chat,
  date: new Date(chat.date),
}));

// 消息容器引用
const messagesContainer = ref<HTMLElement | null>(null)

// 滚动到底部
function scrollToBottom() {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

// 页面加载时滚动到底部
onMounted(() => {
  scrollToBottom()
})
</script>

<style scoped>
.chat-view-wrapper {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 100;
  background-color: var(--md-grey-50);
  overflow: hidden;
}

.chat-container {
  display: flex;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.chat-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  max-height: 100%;
  background-color: #fffff0; /* Ivory color */
  border-top-left-radius: 16px;
  border-bottom-left-radius: 16px;
  box-shadow: -2px 0 10px rgba(0, 0, 0, 0.05);
}

.chat-header {
  padding: 0;
  border-bottom: 1px solid #eaeaea;
  background-color: #fffff0; /* Ivory color */
  text-align: center;
  border-top-left-radius: 16px;
}

.chat-header h2 {
  margin: 0;
  padding: 16px 24px;
  font-size: 18px;
  color: var(--md-grey-800);
  font-weight: 500;
}

.chat-messages {
  flex: 1;
  padding: 0;
  overflow-y: auto;
  background-color: #fffff0; /* Ivory color */
  position: relative;
}

.messages-list {
  min-height: 100%;
  padding: 0;
  display: flex;
  flex-direction: column;
}

.ai-typing {
  padding: 16px 24px;
  background-color: #fffbeb; /* Slightly darker ivory for contrast */
  border-bottom: 1px solid #eaeada;
}

.typing-indicator {
  display: inline-block;
  animation: pulse 1.2s infinite;
  color: var(--md-grey-700);
}

@keyframes pulse {
  0% { opacity: 0.6; }
  50% { opacity: 1; }
  100% { opacity: 0.6; }
}

/* 过渡效果 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.message-fade-enter-active {
  transition: all 0.4s ease;
}

.message-fade-leave-active {
  transition: all 0.3s ease;
  position: absolute;
}

.message-fade-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.message-fade-leave-to {
  opacity: 0;
}

.message-fade-move {
  transition: transform 0.4s ease;
}
</style>