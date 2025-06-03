import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

// API路由
const api_router = {
  knowledgeQuery: () => '/api/knowledge/query',
};

// API响应接口
interface ApiResponse {
  code: number;
  // biome-ignore lint/suspicious/noExplicitAny: <explanation>
  data: any;
  message: string;
  errors?: string;
}

// 查询模型类型
export type SearchModelType = 'RAG' | 'MCP';

import { useProgressStore } from './progressStore';

export const useChatStore = defineStore('chat', () => {
  interface Message {
    role: string;
    content: string;
  }
  
  interface Chat {
    id: string;
    title: string;
    messages: Message[];
    date: Date;
  }

  // 从 localStorage 加载聊天历史，如果没有则使用默认值
  const loadChatHistory = (): Chat[] => {
    try {
      const savedHistory = localStorage.getItem('chatHistory');
      if (savedHistory) {
        const parsed = JSON.parse(savedHistory);
        return parsed.map((chat: any) => ({
          ...chat,
          date: new Date(chat.date)
        }));
      }
    } catch (e) {
      console.error('Error loading chat history:', e);
    }
    return [
      { id: '1', title: '新对话', messages: [], date: new Date() }
    ];
  };

  const chatHistory = ref<Chat[]>(loadChatHistory());
  const currentChatIndex = ref(0);
  const currentModel = ref<SearchModelType>('RAG');
  const messages = ref<Array<{ role: string; content: string }>>([]);
  const isTyping = ref(false);
  const error = ref<string | null>(null);

  // 使用 computed 属性来获取当前聊天
  const currentChat = computed(() => {
    return chatHistory.value[currentChatIndex.value] || null;
  });

  // 初始化进度存储
  const progressStore = useProgressStore();

  // 初始化时加载当前聊天的消息
  if (currentChat.value) {
    messages.value = [...currentChat.value.messages];
  }

  const startNewChat = () => {
    chatHistory.value.push({
      id: String(chatHistory.value.length + 1),
      title: `Chat ${chatHistory.value.length + 1}`,
      messages: [],
      date: new Date(),
    });
    currentChatIndex.value = chatHistory.value.length - 1;
    messages.value = [];
  };

  const selectChat = (index: number) => {
    currentChatIndex.value = index;
    // Load messages from chat history when selecting a chat
    messages.value = [...currentChat.value.messages];
  };

  const deleteChat = (index: number) => {
    chatHistory.value.splice(index, 1);
    if (currentChatIndex.value >= chatHistory.value.length) {
      currentChatIndex.value = chatHistory.value.length - 1;
    }
    // Update messages to reflect the current chat after deletion
    messages.value = currentChat.value ? [...currentChat.value.messages] : [];
  };

  const askExample = (question: string) => {
    onSendMessage(question);
  };

  // 在setup函数中添加事件监听
  window.addEventListener('mcp-result-ready', ((event: CustomEvent) => {
      const { recommendation } = event.detail;
      if (recommendation && messages.value.length > 0) {
          // 添加AI响应到聊天
          const aiMessage = { 
              role: 'assistant', 
              content: recommendation
          };
          messages.value.push(aiMessage);
          isTyping.value = false;
          
          // 添加：更新聊天历史
          if (currentChat.value) {
              // 保存消息到聊天历史
              currentChat.value.messages = [...messages.value];
              currentChat.value.date = new Date();
              
              // 更新聊天历史
              chatHistory.value[currentChatIndex.value] = currentChat.value;
              localStorage.setItem('chatHistory', JSON.stringify(chatHistory.value));
          }
      }
  }) as EventListener);
  
  // 修改onSendMessage函数
  const onSendMessage = async (message: string) => {
      if (!message.trim()) return;
      
      // 添加用户消息到聊天
      messages.value.push({ role: 'user', content: message });
      isTyping.value = true;
      error.value = null;
      
      // 如果是MCP模型，先停止之前的轮询
      let queryId = "";
      if (currentModel.value === 'MCP') {
          progressStore.stopPolling();
          queryId = "temp-" + Date.now(); // create template ID
          progressStore.startPolling(queryId);
      }
      
      try {
          // Call the knowledge query API
          const response = await fetch(api_router.knowledgeQuery(), {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json',
              },
              credentials: 'include',
              body: JSON.stringify({
                  question: message,
                  model: currentModel.value
              }),
          });
          
          if (!response.ok) {
              throw new Error(`HTTP error! status: ${response.status}`);
          }
          
          const result: ApiResponse = await response.json();
          
          // 更新queryId
          if (currentModel.value === 'MCP' && result.data.queryId) {
              progressStore.stopPolling(true);
              queryId = result.data.queryId;
              progressStore.startPolling(queryId, false, true);
              
              // 对于MCP模型，我们不立即添加AI响应，而是等待轮询完成
              // 响应将通过事件监听器添加
              return;
          }
          
          // 检查API是否返回错误
          if (result.code !== 200) {
              throw new Error(result.message || 'API请求失败');
          }
          
          // 对于RAG模型，立即添加AI响应到聊天
          if (currentModel.value === 'RAG') {
              const aiMessage = { 
                  role: 'assistant', 
                  content: result.data.recommendation || '抱歉，我没能找到相关信息。'
              };
              messages.value.push(aiMessage);
          }
          
          // 更新聊天历史
          if (currentChat.value) {
              // 更新聊天标题（如果是第一条消息）
              if (currentChat.value.messages.length === 0) {
                  currentChat.value.title = message.length > 20 
                      ? `${message.substring(0, 20)}...` 
                      : message;
              }
              
              // 保存消息到聊天历史
              currentChat.value.messages = [...messages.value];
              currentChat.value.date = new Date();
              
              // 更新聊天历史
              chatHistory.value[currentChatIndex.value] = currentChat.value;
              localStorage.setItem('chatHistory', JSON.stringify(chatHistory.value));
          }
      } catch (e) {
          error.value = e instanceof Error ? e.message : '发送消息失败，请稍后重试';
          console.error('Error sending message:', e);
          
          // 停止轮询
          if (currentModel.value === 'MCP' && queryId) {
              progressStore.stopPolling();
          }
      } finally {
        if (currentModel.value !== 'MCP' || error.value) {
          isTyping.value = false;
        }
      }
  };

  const toggleModel = () => {
    currentModel.value = currentModel.value === 'RAG' ? 'MCP' : 'RAG';
  };
  
  return { 
    chatHistory, 
    currentChatIndex, 
    currentChat, 
    currentModel,
    messages, 
    isTyping, 
    error,
    startNewChat, 
    selectChat, 
    deleteChat, 
    askExample, 
    onSendMessage,
    toggleModel
  };
});