<template>
  <div class="simple-calendar">
    <div class="calendar-header">
      <button class="nav-button" @click="prevMonth">&lt;</button>
      <div class="month-year">{{ currentMonthYear }}</div>
      <button class="nav-button" @click="nextMonth">&gt;</button>
    </div>
    
    <div class="weekday-header">
      <div v-for="day in weekdays" :key="day" class="weekday">{{ day }}</div>
    </div>
    
    <div class="calendar-grid">
      <div 
        v-for="day in calendarDays" 
        :key="day.date.toISOString()" 
        class="calendar-day"
        :class="{
          'other-month': !day.isCurrentMonth,
          'today': day.isToday,
          'selected': isSelected(day.date),
          'disabled': isDisabled(day.date)
        }"
        @click="selectDate(day)"
      >
        {{ day.dayOfMonth }}
      </div>
    </div>
    
    <!-- 添加底部滑动条 -->
    <div class="calendar-slider">
      <div class="slider-track">
        <div class="slider-handle"></div>
      </div>
      <div class="slider-buttons">
        <button class="slider-nav-btn">&lt;</button>
        <button class="slider-nav-btn">&gt;</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';

// 定义组件props
const props = defineProps({
  value: {
    type: Date,
    default: () => new Date()
  },
  disableFutureDates: {
    type: Boolean,
    default: true
  }
});

const emit = defineEmits(['update:value']);

// 日历状态
const currentMonth = ref(props.value.getMonth());
const currentYear = ref(props.value.getFullYear());
const selectedDate = ref(new Date(props.value));

// 星期名称
const weekdays = ['S', 'M', 'T', 'W', 'T', 'F', 'S'];

// 获取当前月份和年份的显示文本
const currentMonthYear = computed(() => {
  const monthNames = [
    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 
    'July', 'Aug', 'Sept', 'Oct','Nov', 'Dec'
  ];
  return `${monthNames[currentMonth.value]} ${currentYear.value}`;
});

// 获取日历网格数据
const calendarDays = computed(() => {
  const days = [];
  const today = new Date();
  
  // 当前月份的第一天
  const firstDayOfMonth = new Date(currentYear.value, currentMonth.value, 1);
  // 当前月份的最后一天
  const lastDayOfMonth = new Date(currentYear.value, currentMonth.value + 1, 0);
  
  // 计算日历网格的起始日期（上个月的部分日期）
  const startDay = new Date(firstDayOfMonth);
  startDay.setDate(startDay.getDate() - startDay.getDay());
  
  // 生成6周的日历数据（确保总是显示6行）
  for (let i = 0; i < 42; i++) {
    const currentDate = new Date(startDay);
    currentDate.setDate(startDay.getDate() + i);
    
    const isCurrentMonth = currentDate.getMonth() === currentMonth.value;
    const isToday = (
      currentDate.getDate() === today.getDate() &&
      currentDate.getMonth() === today.getMonth() &&
      currentDate.getFullYear() === today.getFullYear()
    );
    
    days.push({
      date: new Date(currentDate),
      dayOfMonth: currentDate.getDate(),
      isCurrentMonth,
      isToday
    });
  }
  
  return days;
});

// 判断日期是否被选中
const isSelected = (date: Date) => {
  return (
    date.getDate() === selectedDate.value.getDate() &&
    date.getMonth() === selectedDate.value.getMonth() &&
    date.getFullYear() === selectedDate.value.getFullYear()
  );
};

// 判断日期是否禁用
const isDisabled = (date: Date) => {
  if (!props.disableFutureDates) return false;
  
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  return date > today;
};

// 选择日期
const selectDate = (day: { date: Date, isCurrentMonth: boolean, isToday: boolean }) => {
  if (isDisabled(day.date)) return;
  
  selectedDate.value = new Date(day.date);
  emit('update:value', selectedDate.value);
};

// 上一个月
const prevMonth = () => {
  if (currentMonth.value === 0) {
    currentMonth.value = 11;
    currentYear.value -= 1;
  } else {
    currentMonth.value -= 1;
  }
};

// 下一个月
const nextMonth = () => {
  if (currentMonth.value === 11) {
    currentMonth.value = 0;
    currentYear.value += 1;
  } else {
    currentMonth.value += 1;
  }
};

onMounted(() => {
  // 确保初始日期正确
  currentMonth.value = props.value.getMonth();
  currentYear.value = props.value.getFullYear();
});
</script>

<style scoped>
.simple-calendar {
  width: 100%;
  background-color: white;
  border-radius: 8px;
  padding: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.calendar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  padding: 0 5px;
}

.nav-button {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 18px;
  color: #666;
  padding: 0 8px;
}

.month-year {
  font-weight: 500;
  font-size: 14px;
}

.weekday-header {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  text-align: center;
  font-size: 12px;
  font-weight: 500;
  color: #666;
  border-bottom: 1px solid #eee;
  padding-bottom: 5px;
  margin-bottom: 5px;
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  grid-template-rows: repeat(6, 1fr);
  gap: 2px;
}

.calendar-day {
  height: 28px;
  width: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  cursor: pointer;
  border-radius: 50%;
  margin: 1px auto;
}

.other-month {
  color: #ccc;
}

.selected {
  background-color: #8052da;
  color: white;
}

.disabled {
  color: #ddd;
  cursor: not-allowed;
}

/* 滑动条样式 */
.calendar-slider {
  margin-top: 10px;
  padding-top: 5px;
  position: relative;
  height: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.slider-track {
  width: 80%;
  height: 4px;
  background-color: #e0e0e0;
  border-radius: 2px;
  position: relative;
}

.slider-handle {
  position: absolute;
  top: 50%;
  left: 30%;
  transform: translate(-50%, -50%);
  width: 10px;
  height: 10px;
  background-color: #8052da;
  border-radius: 50%;
  cursor: pointer;
}

.slider-buttons {
  position: absolute;
  width: 100%;
  display: flex;
  justify-content: space-between;
  padding: 0 5px;
}

.slider-nav-btn {
  background: none;
  border: none;
  font-size: 14px;
  color: #999;
  cursor: pointer;
  padding: 0 5px;
}

@media (max-width: 480px) {
  .calendar-day {
    height: 24px;
    width: 24px;
    font-size: 11px;
  }
}
</style>