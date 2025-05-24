<template>
  <div>
    <!-- 调试信息 -->
    <div class="debug-info" v-if="debugMode">
      <p>{{ dashboardText.debug.newsCount }}: {{ ddlData?.length }}</p>
    </div>
    
    <n-spin :show="loading">      
      <n-grid :cols="12" :x-gap="16" :y-gap="16" class="dashboard-grid">
        <!-- 左侧区域 -->
        <n-grid-item :span="5">
          <!-- 今日消息 -->
          <base-card
            :title="dashboardText.todayMessages.title"
            :items="formattedTodayMessages"
            date-field="time"
            extra-field="source"
            :empty-text="dashboardText.todayMessages.noMessages"
            :view-more-text="dashboardText.todayMessages.viewMore"
            @view-more="handleViewMoreToday"
          />
          
          <!-- 历史消息
          <base-card
            :title="dashboardText.historyMessages.title"
            :items="formattedHistoryMessages"
            extra-field="views"
            :empty-text="dashboardText.historyMessages.noMessages"
            :view-more-text="dashboardText.historyMessages.viewMore"
            @view-more="handleViewMoreHistory"
          /> -->
        </n-grid-item>
        
        <!-- 右侧区域 -->
        <n-grid-item :span="4">
          <!-- ddl提醒 -->
          <base-card
            :title="dashboardText.ddlNews.title"
            :items="formattedDdlItems"
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
import { ref, onMounted, computed, onBeforeUnmount } from 'vue'
import {
  NGrid,
  NGridItem,
  NSpin,
  createDiscreteApi
} from 'naive-ui'
import SimpleCalendar from '../components/SimpleCalendar.vue'
import BaseCard from '../components/BaseCard.vue'
import dashboardText from '../resource/dashboard'
import { useDashboardData } from '../stores/dashboardStore';
import dayjs from 'dayjs';

// 调试模式开关
const debugMode = ref(false)

// 从dashboardStore.ts导入类型
import type { DdlItem, Message } from '../stores/dashboardStore';

// 准备数据容器
const ddlData = ref<DdlItem[]>([])
const todayMessages = ref<Message[]>([])
const loading = ref(true) // 初始设置为加载中状态
const selectedDate = ref(new Date()) // 选中的日期
let refreshData: (() => Promise<void>) | null = null

// 在组件挂载时异步加载数据
onMounted(async () => {
  try {
    // 异步获取数据
    const dashboardData = await useDashboardData()
    ddlData.value = dashboardData.ddlData
    todayMessages.value = dashboardData.todayMessages
    refreshData = dashboardData.refreshData
    
    console.log('Data loaded:', {
      ddlData: ddlData.value,
      todayMessages: todayMessages.value
    })
  } catch (error) {
    console.error('Failed to load dashboard data:', error)
  } finally {
    loading.value = false
  }
})

// 转换 todayMessages 为 CardItem 类型
const formattedTodayMessages = computed(() => {
  if (!todayMessages.value || todayMessages.value.length === 0) return [];
  console.log('link', todayMessages.value.map((message:Message) => message.source))
  return todayMessages.value.map((message: Message) => ({
    title: message.title || '',
    time: message.time || '',
    source: ''
  }))
})

// // 转换 historyMessages 为 CardItem 类型
// const formattedHistoryMessages = computed(() => {
//   if (!historyMessages || historyMessages.length === 0) return [];
//   return historyMessages.map(message => ({
//     title: message.title,
//     time: message.time,
//     source: message.source?.toString() || '' // 添加可选链和默认值
//   }))
// })

// 创建离散API，可以在组件外使用
const { message } = createDiscreteApi(['message'])

// 日期选择处理
function handleDateSelect(date: Date) {
  selectedDate.value = date
}

// 根据选中日期过滤 DDL 数据
const ddlBySelectedDate = computed(() => {
  if (!ddlData.value || ddlData.value.length === 0) return []
  const sd = dayjs(selectedDate.value).format('YYYY-MM-DD')
  return ddlData.value.filter((item: DdlItem) => item.date && item.date.format('YYYY-MM-DD') === sd)
})

// 格式化 DDL 数据为 CardItem 类型
const formattedDdlItems = computed(() => {
  if (!ddlBySelectedDate.value || ddlBySelectedDate.value.length === 0) return []
  return ddlBySelectedDate.value.map(item => ({
    title: item.title || '',
    date: item.date ? item.date.format('YYYY-MM-DD') : '',
    time: item.time ? item.time.format('HH:mm') : '',
    description: item.time ? `${item.time.format('HH:mm')}` : ''
  }))
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

// 注意：数据加载已经在上面的 onMounted 中处理，这里不需要重复加载

// 组件销毁前的清理工作
onBeforeUnmount(() => {
  // 清理所有可能导致内存泄漏或错误的引用
  // 这有助于防止 "message port closed" 错误
  debugMode.value = false
  loading.value = false
  // 如果有其他事件监听器或计时器，这里也应该清理它们
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