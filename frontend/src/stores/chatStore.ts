import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

export const useChatStore = defineStore('chat', () => {
  const chatHistory = ref([
    { id: '1', title: 'Chat 1', messages: [], date: new Date() },
    { id: '2', title: 'Chat 2', messages: [], date: new Date() },
  ]);
  const currentChatIndex = ref(0);

  const currentChat = computed(() => chatHistory.value[currentChatIndex.value]);

  const messages = ref([]);
  const isTyping = ref(false);

  const startNewChat = () => {
    chatHistory.value.push({
      id: String(chatHistory.value.length + 1),
      title: `Chat ${chatHistory.value.length + 1}`,
      messages: [],
      date: new Date(),
    });
    currentChatIndex.value = chatHistory.value.length - 1;
  };

  const selectChat = (index: number) => {
    currentChatIndex.value = index;
  };

  const deleteChat = (index: number) => {
    chatHistory.value.splice(index, 1);
    if (currentChatIndex.value >= chatHistory.value.length) {
      currentChatIndex.value = chatHistory.value.length - 1;
    }
  };

  const askExample = () => {
    // Example implementation
  };

  const onSendMessage = (message: string) => {
    // Example implementation
  };

  return { chatHistory, currentChatIndex, currentChat, messages, isTyping, startNewChat, selectChat, deleteChat, askExample, onSendMessage };
});