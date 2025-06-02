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
          <div class="header-content">
            <transition name="fade" mode="out-in">
              <h2 :key="chatStore.currentChatIndex">{{ chatStore.currentChat?.title || chatResource.title }}</h2>
            </transition>
            
            <!-- 对话指南按钮 -->
            <n-button
              size="medium"
              type="default"
              @click="showGuide = true"
              class="guide-btn-header"
              text
              strong
            >
              <span class="guide-icon">AI助手交互指南</span>
            </n-button>
          </div>
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
              
              <!-- 错误提示 -->
              <div v-if="chatStore.error" class="error-message">
                {{ chatStore.error }}
              </div>
              
              <!-- 正在输入提示 -->
              <transition name="fade">
                <div v-if="chatStore.isTyping" class="ai-typing">
                  <div class="typing-indicator">
                    <template v-if="progressStore.isPolling && chatStore.currentModel === 'MCP'">
                      {{ progressStore.progressMessage }}
                      <div class="progress-bar">
                        <div class="progress-fill" :style="{ width: progressStore.progress + '%' }"></div>
                      </div>
                    </template>
                    <template v-else>
                      {{ chatResource.thinking }}
                    </template>
                  </div>
                </div>
              </transition>
            </div>
          </transition>
        </div>
        
        <!-- 输入区域 -->
        <chat-input @send="chatStore.onSendMessage">
          <!-- 添加模型切换按钮作为插槽内容 -->
          <template #append>
            <n-button 
              size="medium" 
              :type="chatStore.currentModel === 'RAG' ? 'primary' : 'info'"
              @click="chatStore.toggleModel"
              class="model-toggle-btn-input"
              :ghost="true"
              round
              strong
            >
              <span class="model-icon">{{ chatStore.currentModel === 'RAG' ? 'RAG' : 'MCP' }}</span>
            </n-button>
          </template>
        </chat-input>
      </div>
    </div>
    
    <!-- 对话指南弹出框 -->
    <n-modal
      v-model:show="showGuide"
      preset="card"
      title="AI助手交互指南"
      style="width: 80%; max-width: 600px;"
      :mask-closable="true"
    >
      <div class="guide-content">
        <h3>欢迎使用智能检索助手</h3>
        <p>我们提供智能 AI 检索服务，助您高效获取所需信息。</p>
        
        <h4>一、检索方式</h4>
        <p>本平台智能检索部分采用 RAG（检索增强生成） 和 MCP （模型上下文协议）双模式。RAG 可实现快速响应，MCP 则能实现精确查询。</p>
        
        <h4>二、MCP 查询方式说明</h4>
        <p>● 默认情况下，MCP 查询仅筛选活动开始或结束时间不早于当前提问时间的活动（即您可参与的活动）。若您希望查看历史消息，或仅了解活动资讯（不考虑是否参与），请在提示词中明确添加"不考虑时间限制"或"不考虑消息是否过期"。</p>
        <p>● 智能助手有时会返回"未检索到相关信息"。可能是服务器不稳定，建议再次尝试；也可能是相关消息都已过期，此时建议在提示词末尾加上"不考虑时间限制"以检索历史信息。</p>
        
        <h4>三、与 AI 助手互动</h4>
        <p>您可与 AI 助手进行对话。当助手识别到检索需求时，将自动在知识库或数据库中检索。若助手未能识别您的检索意图，您可在提示词中直接写明"直接帮我检索 [具体信息]"。建议清晰描述检索需求，以便 AI 助手准确理解意图并返回您所需信息。</p>
        
        <h4>四、问题反馈与技术支持</h4>
        <p>使用过程中，如遇 API 调用报错或有任何改进建议，欢迎随时联系：</p>
        <p>● RAG 技术支持邮箱： 241880030@smail.nju.edu.cn</p>
        <p>● MCP 技术支持邮箱： 241880484@smail.nju.edu.cn</p>
        <p>我们将竭诚为您服务，持续优化您的检索体验😊</p>
      </div>
    </n-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import chatResource from '../resource/chat.ts'
// Lazy load chat components
import ChatSidebar from '../components/chat/ChatSidebar.vue'
import ChatMessage from '../components/chat/ChatMessage.vue'
import WelcomeScreen from '../components/chat/WelcomeScreen.vue'
import ChatInput from '../components/chat/ChatInput.vue'
import { useChatStore } from '@/stores/chatStore.ts';
// Import only the needed component from naive-ui
import { NButton, NModal } from 'naive-ui';
import type { SearchModelType } from '@/stores/chatStore';
// Show progress of MCP
import { useProgressStore } from '@/stores/progressStore';

// 初始化进度储存
const progressStore = useProgressStore();

// 对话指南显示状态
const showGuide = ref(false);

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
  currentModel: SearchModelType;
  isTyping: boolean;
  error: string | null;
  startNewChat: () => void;
  selectChat: (index: number) => void;
  deleteChat: (index: number) => void;
  askExample: (question: string) => void;
  onSendMessage: (message: string) => void;
  toggleModel: () => void;
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

// 监听消息和打字状态变化，滚动到底部
import { watch } from 'vue';

watch(
  () => [...chatStore.messages, chatStore.isTyping],
  () => {
    // 使用 nextTick 确保 DOM 已更新
    nextTick(() => {
      scrollToBottom();
    });
  },
  { deep: true }
);

// 页面加载时滚动到底部
onMounted(() => {
  scrollToBottom();
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
  background-color: #ffffff; /* White color */
  border-top-left-radius: 16px;
  border-bottom-left-radius: 16px;
  box-shadow: -2px 0 10px rgba(0, 0, 0, 0.05);
}

.chat-header {
  padding: 0;
  border-bottom: 1px solid #eaeaea;
  background-color: #ffffff; /* White color */
  text-align: center;
  border-top-left-radius: 16px;
}

.header-content {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 8px 16px;
  position: relative;
}

.chat-header h2 {
  margin: 0;
  padding: 8px 16px;
  font-size: 18px;
  font-weight: 500;
  flex-grow: 1;
  text-align: center;
}

/* 移除原来的模型切换按钮和指南按钮样式 */
.model-toggle-btn {
  position: absolute;
  right: 16px;
  font-size: 14px;
  padding: 4px 12px;
  transition: all 0.3s ease;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.08);
  border-width: 1.5px;
}

.guide-btn {
  position: absolute;
  right: 16px;
  top: 45px;
  font-size: 14px;
  padding: 4px 12px;
  transition: all 0.3s ease;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.08);
  border-width: 1.5px;
}

/* 添加新的指南按钮样式 (在头部) */
.guide-btn-header {
  position: absolute;
  right: 16px;
  font-size: 14px;
  padding: 4px 12px;
  transition: all 0.3s ease;
  color: #000000; /* 黑色文字 */
}

/* 添加新的模型切换按钮样式 (在输入框旁) */
.model-toggle-btn-input {
  margin-left: 8px;
  font-size: 14px;
  padding: 4px 12px;
  transition: all 0.3s ease;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.08);
  border-width: 1.5px;
}

.model-toggle-btn:hover, .guide-btn:hover, .guide-btn-header:hover, .model-toggle-btn-input:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.12);
}

.model-icon, .guide-icon {
  font-size: 16px;
  font-weight: 600;
}

.guide-content {
  text-align: left;
  line-height: 1.6;
}

.guide-content h3 {
  margin-top: 0;
  color: #2080f0;
}

.guide-content h4 {
  margin-top: 16px;
  margin-bottom: 8px;
  color: #18a058;
}

.guide-content p {
  margin: 8px 0;
}

.chat-messages {
  flex: 1;
  padding: 0;
  overflow-y: auto;
  background-color: #ffffff; /* White color */
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
  background-color: #f9f9f9; /* Light gray for subtle contrast */
  border-bottom: 1px solid #eaeaea;
}

.typing-indicator {
  display: inline-block;
  animation: pulse 1.2s infinite;
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

/* 错误提示样式 */
.error-message {
  padding: 16px 24px;
  background-color: #ffebee; /* Light red background */
  color: #d32f2f; /* Red text */
  border-bottom: 1px solid #ffcdd2;
  margin-top: 8px;
  border-radius: 8px;
  font-size: 14px;
}
</style>