import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

// API路由
const api_router = {
  knowledgeQuery: () => '/api/knowledge/query',
};

// API响应接口
interface ApiResponse {
  code: number;
  data: any;
  message: string;
  errors?: string;
}

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

  const chatHistory = ref<Chat[]>([
    { id: '1', title: 'Chat 1', messages: [], date: new Date() },
    { id: '2', title: 'Chat 2', messages: [], date: new Date() },
  ]);
  const currentChatIndex = ref(0);

  const currentChat = computed(() => chatHistory.value[currentChatIndex.value]);

  const messages = ref<Array<{ role: string; content: string }>>([]);
  const isTyping = ref(false);
  const error = ref<string | null>(null);

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

  const askExample = () => {
    onSendMessage("请介绍一下南京大学");
  };

  const onSendMessage = async (message: string) => {
    if (!message.trim()) return;
    
    // Add user message to the chat
    const userMessage = { role: 'user', content: message };
    messages.value.push(userMessage);
    
    // Update chat history
    if (currentChat.value) {
      currentChat.value.messages = [...messages.value];
    }
    
    try {
      // Show typing indicator
      isTyping.value = true;
      error.value = null;
      
      // Call the knowledge query API
      const response = await fetch(api_router.knowledgeQuery(), {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question: message,
          model: 'RAG'  // 默认使用RAG模型
        }),
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const result: ApiResponse = await response.json();
      
      // Check if API returned an error
      if (result.code !== 200) {
        throw new Error(result.message || 'API请求失败');
      }
      
      // Add AI response to the chat
      const aiMessage = { 
        role: 'assistant', 
        content: result.data.recommendation || '抱歉，我没能找到相关信息。'
      };
      messages.value.push(aiMessage);
      
      // Update chat history
      if (currentChat.value) {
        // Update chat title based on first user message if this is the first message
        if (currentChat.value.messages.length === 0) {
          currentChat.value.title = message.length > 20 
            ? `${message.substring(0, 20)}...` 
            : message;
        }
        currentChat.value.messages = [...messages.value];
      }
      
    } catch (e) {
      console.error('消息发送失败:', e);
      error.value = e instanceof Error ? e.message : '消息发送失败，请稍后重试';
      
      // Add error message
      messages.value.push({
        role: 'system',
        content: `错误: ${error.value}`
      });
    } finally {
      isTyping.value = false;
    }
  };

  return { 
    chatHistory, 
    currentChatIndex, 
    currentChat, 
    messages, 
    isTyping, 
    error,
    startNewChat, 
    selectChat, 
    deleteChat, 
    askExample, 
    onSendMessage 
  };
});