import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useSidebarStore = defineStore('sidebar', () => {
  const collapsed = ref(true);

  const toggleSidebar = () => {
    collapsed.value = !collapsed.value;
  };

  return { collapsed, toggleSidebar };
});