<template>
  <n-notification-provider>
    <div>
      <n-spin :show="loading">
        <n-grid :cols="12" :x-gap="16" :y-gap="16" class="dashboard-grid">
          <!-- 左侧区域 -->
          <n-grid-item :span="5">
            <!-- 消息 -->
            <base-card
              :title="dashboardText.dayMessages.title"
              :item-groups="itemGroups"
              date-field="time"
              extra-field="source"
              :empty-text="dashboardText.dayMessages.noMessages"
              :view-more-text="dashboardText.dayMessages.viewMore"
              @view-more="handleViewMoreToday"
            />
          </n-grid-item>

          <!-- 右侧区域 -->
          <n-grid-item :span="4">
            <!-- ddl提醒 -->
            <base-card
              :title="dashboardText.ddlNews.title"
              :items="formattedDdlItems"
              extra-field="description"
              :empty-text="dashboardText.dayMessages.noMessages"
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
  </n-notification-provider>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, onBeforeUnmount, h } from "vue";
import {
  NGrid,
  NGridItem,
  NSpin,
  NNotificationProvider,
  createDiscreteApi,
} from "naive-ui";
import SimpleCalendar from "../components/SimpleCalendar.vue";
import BaseCard from "../components/BaseCard.vue";
import dashboardText from "../resource/dashboard";
import { useDashboardData } from "../stores/dashboardStore";
import dayjs from "dayjs";
import type { CardItem, ItemGroup } from "../components/BaseCard.vue";

// 调试模式开关
const debugMode = ref(false);

// 从dashboardStore.ts导入类型
import type { DdlItem, Message } from "../stores/dashboardStore";

// 事件类型的集合
const eventTypes = [
  "比赛通知",
  "学习资源",
  "校园资源",
  "学业申请",
  "学业相关政策",
  "奖励资助政策",
  "惩罚制度",
  "校园安全",
  "讲座分享会信息",
  "志愿活动",
  "社会实践",
  "国际交流项目",
  "社团消息",
  "问题活动",
  "实践培训活动",
  "作品征集",
  "其他活动",
  "实习就业",
  "其他类型",
];

// 准备数据容器
const ddlData = ref<DdlItem[]>([]);
const Messages = ref<Message[]>([]);
const loading = ref(true); // 初始设置为加载中状态
const selectedDate = ref(new Date()); // 选中的日期
let refreshData: (() => Promise<void>) | null = null;

// 在组件挂载时异步加载数据
onMounted(async () => {
  try {
    // 异步获取数据
    const dashboardData = await useDashboardData();
    ddlData.value = dashboardData.ddlData;
    Messages.value = dashboardData.Messages;
    refreshData = dashboardData.refreshData;
  } catch (error) {
    console.error("Failed to load dashboard data:", error);
  } finally {
    loading.value = false;
  }
});

// 转换 Messages 为 CardItem 类型
const formattedMessages = computed(() => {
  if (!Messages.value || Messages.value.length === 0) return [];
  return Messages.value.map((message: Message) => ({
    title: message.title || "",
    time: message.time || "",
    abstract: message.abstract || "",
    type: message.type || "",
    source: message.source || "",
  }));
});

// 事件组
const itemGroups = computed(() => {
  const groups: ItemGroup[] = [];

  console.log("formattedMessages:", formattedMessages.value);
  for (const type of eventTypes) {
    const filteredItems = formattedMessages.value.filter(
      (item: CardItem) => item.type === type
    );

    if (filteredItems.length > 0) {
      groups.push({
        groupTitle: type,
        items: filteredItems,
      });
    }
  }

  console.log("itemGroups:", groups);
  return groups;
});

// 创建离散API，可以在组件外使用
const { message } = createDiscreteApi([
  "message",
  "notification",
]);

// 日期选择处理
function handleDateSelect(date: Date) {
  selectedDate.value = date;
}

// 根据选中日期过滤 DDL 数据
const ddlBySelectedDate = computed(() => {
  if (!ddlData.value || ddlData.value.length === 0) return [];
  const sd = dayjs(selectedDate.value).format("YYYY-MM-DD");
  return ddlData.value.filter(
    (item: DdlItem) => item.date && item.date.format("YYYY-MM-DD") === sd
  );
});

// 格式化 DDL 数据为 CardItem 类型
const formattedDdlItems = computed(() => {
  if (!ddlBySelectedDate.value || ddlBySelectedDate.value.length === 0)
    return [];
  return ddlBySelectedDate.value.map((item) => ({
    title: item.title || "",
    date: item.date ? item.date.format("YYYY-MM-DD") : "",
    time: item.time ? item.time.format("HH:mm") : "",
    description: item.time ? `${item.time.format("HH:mm")}` : "",
  }));
});

// 处理"查看更多"点击事件
function handleViewMoreToday() {
  message.info("查看更多今日消息");
}

function handleViewMoreDdl() {
  message.info("查看更多DDL消息");
}

// 组件销毁前的清理工作
onBeforeUnmount(() => {
  debugMode.value = false;
  loading.value = false;
  // 如果有其他事件监听器或计时器，这里也应该清理它们
});

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
  max-width: 1600px;
  /* 适合现代显示器的宽度 */
  margin-right: auto;
  /* 自动左右边距实现居中 */
  box-sizing: border-box;
  /* 确保padding不会增加总宽度 */
  display: flex;
  gap: 24px;
  /* 增加列间距 */
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
  min-height: 300px;
  /* 给DDL卡片固定最小高度 */
}
</style>
