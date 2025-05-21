<template>
  <div>
    <!-- 调试信息 -->
    <div class="debug-info" v-if="debugMode">
      <p>{{ dashboardText.debug.totalUsers }}: {{ summaryData?.totalUsers }}</p>
      <p>{{ dashboardText.debug.coursesCount }}: {{ tableData?.length }}</p>
      <p>{{ dashboardText.debug.newsCount }}: {{ ddlData?.length }}</p>
    </div>
    
    <n-spin :show="loading">      
      <n-grid :cols="12" :x-gap="16" :y-gap="16" class="dashboard-grid">
        <!-- 左侧区域 -->
        <n-grid-item :span="5">
          <!-- 今日消息 -->
          <base-card
            :title="dashboardText.todayMessages.title"
            :items="todayMessages"
            date-field="time"
            extra-field="source"
            :empty-text="dashboardText.todayMessages.noMessages"
            :view-more-text="dashboardText.todayMessages.viewMore"
            @view-more="handleViewMoreToday"
          />
          
          <!-- 历史消息 -->
          <base-card
            :title="dashboardText.historyMessages.title"
            :items="historyMessages"
            extra-field="views"
            :empty-text="dashboardText.historyMessages.noMessages"
            :view-more-text="dashboardText.historyMessages.viewMore"
            @view-more="handleViewMoreHistory"
          />
        </n-grid-item>
        
        <!-- 右侧区域 -->
        <n-grid-item :span="4">
          <!-- ddl提醒 -->
          <base-card
            :title="dashboardText.ddlNews.title"
            :items="ddlBySelectedDate"
            extra-field="description"
            :empty-text="dashboardText.todayMessages.noMessages"
            :view-more-text="dashboardText.ddlNews.viewMore"
            @view-more="handleViewMoreDdl"
          />
          
          <!-- 使用 BaseCard 组件显示日历 -->
          <base-card
            :title="dashboardText.calendar.title"
            :is-calendar-mode="true"
            calendar-footer-text="点击查看 DDL"
          >
            <template #calendar>
              <SimpleCalendar
                v-model:value="selectedDate"
                :disableFutureDates="true"
                @update:value="handleDateSelect"
              />
            </template>
          </base-card>
        </n-grid-item>
      </n-grid>
    </n-spin>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import {
  NGrid,
  NGridItem,
  NSpin,
  NCard,
  createDiscreteApi
} from 'naive-ui'
import SimpleCalendar from '../components/SimpleCalendar.vue'
import BaseCard from '../components/BaseCard.vue'
import { useDashboardData } from '../services/dataService'
import dashboardText from '../resource/dashboard'
import { useCalendarStore } from '@/stores/calendarStore.ts';

// 调试模式开关
const debugMode = ref(false)

// 获取数据
const { summaryData, tableData, ddlData, todayMessages, historyMessages } = useDashboardData()
const loading = ref(false)
const calendarStore = useCalendarStore();
const selectedDate = ref(new Date())

// 创建离散API，可以在组件外使用
const { message } = createDiscreteApi(['message'])

// 日期选择处理
function handleDateSelect(date: Date) {
  selectedDate.value = date
}

// 根据选中日期过滤 DDL 数据
const ddlBySelectedDate = computed(() => {
  const sd = selectedDate.value.toISOString().slice(0, 10) // YYYY-MM-DD
  return ddlData.value.filter(item => item.date === sd)
})

// 处理"查看更多"点击事件
function handleViewMoreToday() {
  message.info('查看更多今日消息')
}

function handleViewMoreHistory() {
  message.info('查看更多历史消息')
}

function handleViewMoreDdl() {
  message.info('查看更多DDL消息')
}

// 确保在页面加载后数据可用
onMounted(() => {
  console.log('Dashboard mounted, data available:', { 
    summaryData: summaryData.value,
    newsData: ddlData.value,
    todayMessages: todayMessages.value,
    historyMessages: historyMessages.value
  });
})
</script>

<style scoped>
.bordered-card {
  border: 1px solid rgba(0, 0, 0, 0.1);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  background-color: #ffffff;
  position: relative;
  overflow: hidden;
  color: #333333;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.dashboard-header h1 {
  color: #333333;
  font-size: 24px;
  margin: 0;
}

.summary-section {
  margin-bottom: 20px;
}

.summary-section h2 {
  font-size: 18px;
  margin-bottom: 12px;
  color: #333333;
}

.dashboard-grid {
  margin-top: 20px;
  width: 100%;
  max-width: 1600px; /* 适合现代显示器的宽度 */
  margin-left: 150px;
  margin-right: auto; /* 自动左右边距实现居中 */
  box-sizing: border-box; /* 确保padding不会增加总宽度 */
  display: flex;
  gap: 24px; /* 增加列间距 */
}

.debug-info {
  margin: 10px 0;
  padding: 10px;
  border: 1px solid #ddd;
  background-color: #f5f5f5;
  border-radius: 4px;
}

.calendar-card {
  margin-top: 20px;
  width: 100%;
}

.calendar-container {
  display: flex;
  flex-direction: column;
}

.calendar-footer {
  margin-top: 10px;
  text-align: center;
  font-size: 12px;
  color: #999999;
}

/* 移除固定定位，使用独立的布局方式防止抖动 */
.calendar-wrapper {
  /* 去掉 position: fixed */
  width: 100%;
}

/* 使DDL卡片有固定高度，防止内容变化导致日历位置抖动 */
:deep(.base-card) {
  min-height: 300px; /* 给DDL卡片固定最小高度 */
}
</style>