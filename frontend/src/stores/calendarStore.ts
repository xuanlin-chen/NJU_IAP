import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useCalendarStore = defineStore('calendar', () => {
  const selectedDate = ref(new Date());

  const updateSelectedDate = (date: Date) => {
    selectedDate.value = date;
  };

  return { selectedDate, updateSelectedDate };
});