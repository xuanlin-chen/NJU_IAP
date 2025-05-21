<script setup lang="ts">
import { NCard } from 'naive-ui'
import newsText from '../resource/components/latestNews'
import { computed } from 'vue' // Import computed

interface NewsItem {
  title: string;
  date: string;
  group: number;
}

const props = defineProps<{ // Store props in a variable
  newsData: NewsItem[];
}>();

// Computed property to check if news items are overflowing
const isNewsOverflowing = computed(() => {
  return props.newsData && props.newsData.length > 6; // Show "View more" if more than 6 items
});
</script>

<template>
  <n-card :title="newsText.title" class="news-card bordered-card">
    <div v-if="newsData && newsData.length > 0">
      <div v-for="(news, index) in newsData" :key="index" class="news-item">
        <div class="news-title">{{ news.title }}</div>
        <div class="news-footer">
          <span>{{ news.date }}</span>
        </div>
      </div>
      <div v-if="isNewsOverflowing" class="view-more"> <!-- Conditionally display view-more -->
        <a href="#">{{ newsText.viewMore }}</a>
      </div>
    </div>
    <div v-else class="no-data">
      {{ newsText.noNews }}
    </div>
  </n-card>
</template>

<style scoped>
.bordered-card {
  border: 1px solid rgba(0, 0, 0, 0.1);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  background-color: #ffffff;
  position: relative;
  overflow: hidden;
  color: #333333;
}

.news-card {
  margin-top: 16px;
  height: 400px; /* 固定高度 */
  width: 100%;
}

.news-item {
  padding: 10px 0;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
}

.news-item:last-child {
  border-bottom: none;
}

.news-title {
  font-size: 14px;
  color: #333333;
  margin-bottom: 6px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.news-footer {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: rgba(0, 0, 0, 0.6);
}

.view-more {
  text-align: center;
  margin-top: 10px;
  font-size: 14px;
}

.view-more a {
  color: #2080f0;
  text-decoration: none;
}

.no-data {
  text-align: center;
  padding: 20px;
  color: rgba(0, 0, 0, 0.45);
}

/* 确保卡片标题为黑色 */
:deep(.n-card-header__main) {
  color: #333333;
}
</style>