<template>
  <n-card :title="title" class="base-card bordered-card">
    <!-- 添加默认插槽 -->
    <slot name="default">
      <!-- 日历模式 -->
      <div v-if="isCalendarMode" class="calendar-container">
        <slot name="calendar"></slot>
        <div v-if="calendarFooterText" class="calendar-footer">
          <span>{{ calendarFooterText }}</span>
        </div>
      </div>
      
      <!-- 列表模式 -->
      <div v-else-if="items && items.length > 0">
        <div v-for="(item, index) in items" :key="index" class="item">
          <div class="item-title">{{ getItemTitle(item) }}</div>
          <div class="item-footer">
            <span>{{ getItemDate(item) }}</span>
            <span v-if="getItemExtra(item)">{{ getItemExtra(item) }}</span>
          </div>
        </div>
        <div v-if="showViewMore" class="view-more">
          <a href="#" @click.prevent="$emit('view-more')">{{ viewMoreText }}</a>
        </div>
      </div>
      
      <!-- 空数据状态 -->
      <div v-else class="no-data">
        {{ emptyText }}
      </div>
    </slot>
  </n-card>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { NCard } from 'naive-ui';

interface CardItem {
  title?: string;
  date?: string;
  time?: string;
  description?: string;
  source?: string;
  views?: number;
  [key: string]: any;
}

const props = defineProps<{
  title: string;
  items?: CardItem[];
  titleField?: string;
  dateField?: string;
  extraField?: string;
  emptyText?: string;
  viewMoreText?: string;
  maxItems?: number;
  isCalendarMode?: boolean;
  calendarFooterText?: string;
}>();

defineEmits<{
  (event: 'view-more'): void;
}>();

const showViewMore = computed(() => {
  return props.maxItems && props.items && props.items.length > props.maxItems;
});

const getItemTitle = (item: CardItem): string => {
  return props.titleField ? item[props.titleField] : item.title || '';
};

const getItemDate = (item: CardItem): string => {
  return props.dateField ? item[props.dateField] : (item.date || item.time || '');
};

const getItemExtra = (item: CardItem): string => {
  if (props.extraField) {
    return item[props.extraField] || '';
  }
  
  if (item.source) return item.source;
  if (item.description) return item.description;
  if (item.views !== undefined) return `${item.views} 浏览`;
  
  return '';
};
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

.base-card {
  margin-bottom: 16px;
  width: 100%;
  min-height: 300px; /* 保持卡片高度一致，防止抖动 */
}

.item {
  padding: 10px 0;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.item:last-child {
  border-bottom: none;
}

.item-title {
  font-size: 14px;
  font-weight: 500;
  color: #333333;
  margin-bottom: 6px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.item-footer {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #999999;
}

.view-more {
  text-align: right;
  margin-top: 10px;
  font-size: 14px;
}

.view-more a {
  color: #8052da;
  text-decoration: none;
}

.no-data {
  text-align: center;
  padding: 15px 0;
  color: #999999;
}

/* 日历容器样式 */
.calendar-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 10px 0;
}

.calendar-footer {
  margin-top: 10px;
  text-align: center;
  font-size: 12px;
  color: #999999;
}

/* 确保卡片标题为黑色 */
:deep(.n-card-header__main) {
  color: #333333;
}
</style>