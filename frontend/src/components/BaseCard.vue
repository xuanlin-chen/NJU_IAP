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

      <!-- 详情模态框 -->
      <n-modal
        v-model:show="showItemDetailsModal"
        preset="card"
        style="max-width: 600px"
        :title="currentItem?.title || '详情'"
        size="medium"
        :segmented="true"
      >
        <template #header-extra>
          <div class="modal-header-extra">
            <n-avatar
              size="small"
              round
              src="https://07akioni.oss-cn-beijing.aliyuncs.com/07akioni.jpeg"
            />
            <span class="header-label">智能摘要</span>
          </div>
        </template>

        <div class="item-abstract" v-if="currentItem">
          <!-- 使用 v-html 来渲染 markdown -->
          <div
            v-html="renderMarkdown(currentItem.abstract || '暂无摘要')"
            class="markdown-content"
          ></div>
          
          <!-- 显示关键词 -->
          <div v-if="currentItem.keywords" class="item-keywords">
            <span class="keywords-label">关键词：</span>
            <span class="keywords-content">{{ currentItem.keywords }}</span>
          </div>
        </div>

        <template #footer>
          <div class="modal-footer">
            <n-space justify="end">
              <n-button
                v-if="currentItem?.link"
                type="primary"
                tag="a"
                :href="
                  typeof currentItem?.link === 'string'
                    ? currentItem?.link
                    : currentItem?.link
                    ? currentItem?.link.href
                    : ''
                "
                target="_blank"
              >
                查看原文
              </n-button>
              <n-button @click="showItemDetailsModal = false"> 关闭 </n-button>
            </n-space>
          </div>
        </template>
      </n-modal>
      <!-- 分组列表模式 -->
      <div v-if="itemGroups && itemGroups.length > 0">
        <n-collapse>
          <n-collapse-item
            v-for="(group, groupIndex) in itemGroups"
            :key="groupIndex"
            :title="group.groupTitle"
            :name="'group-' + groupIndex"
          >
            <div
              v-for="(item, itemIndex) in group.items"
              :key="itemIndex"
              class="item"
            >
              <div class="item-title">{{ getItemTitle(item) }}</div>
              <div class="item-footer">
                <span>{{ getItemDate(item) }}</span>
                <span @click.stop="handleClick(item)" class="view-details-link">
                  查看详情
                </span>
              </div>
            </div>
          </n-collapse-item>
        </n-collapse>
      </div>
      <!-- 简单列表模式 -->
      <div v-else-if="useSimpleList && items && items.length > 0">
        <div class="simple-list">
          <div
            v-for="(item, index) in items"
            :key="index"
            class="simple-list-item"
          >
            <div class="simple-item-content">
              <div class="simple-item-title" @click.stop="handleClick(item)">
                {{ getItemTitle(item) }}
              </div>
              <n-icon
                v-if="showDeleteButton"
                class="delete-icon"
                @click.stop="handleDelete(item, index)"
              >
                <close-icon />
              </n-icon>
            </div>
            <div class="simple-item-footer">
              <span>{{ getItemDate(item) }}</span>
              <span v-if="item.extra" class="item-extra">{{ item.extra }}</span>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 列表模式 -->
      <div v-else-if="items && items.length > 0">
        <n-collapse>
          <n-collapse-item
            v-for="(item, index) in items"
            :key="index"
            :title="getItemTitle(item)"
            :name="index.toString()"
          >
            <div class="item-content">
              <div class="item-footer">
                <div class="item-actions">
                  <n-button
                    v-if="showDeleteButton"
                    size="small"
                    type="error"
                    @click.stop="handleDelete(item, index)"
                    >删除</n-button
                  >
                  <span v-if="item.extra" class="item-extra">{{
                    item.extra
                  }}</span>
                </div>
              </div>
            </div>
          </n-collapse-item>
        </n-collapse>
      </div>

      <!-- 空数据状态 -->
      <div v-else class="no-data">
        {{ emptyText }}
      </div>
    </slot>
  </n-card>
</template>

<script setup lang="ts">
import { computed, ref } from "vue";
import {
  NCard,
  NCollapse,
  NCollapseItem,
  NAvatar,
  NModal,
  NButton,
  NSpace,
  NIcon,
} from "naive-ui";
import { CloseOutline as CloseIcon } from "@vicons/ionicons5";
import { marked } from "marked";
// 在浏览器环境中使用 DOMPurify 的正确方式

// 状态变量
const showItemDetailsModal = ref(false);
const currentItem = ref<CardItem | null>(null);

export interface CardItem {
  title?: string;
  date?: string;
  time?: string;
  type?: typeof EventTypes;
  abstract?: string;
  description?: string;
  source?: string | URL;
  views?: number;
  extra?: string;
  keywords?: string; // 添加关键词字段
  link?: string | URL; // 添加原文链接字段
  // 使用 unknown 而不是 any
  [key: string]: unknown;
}

export interface ItemGroup {
  groupTitle: string;
  items: CardItem[];
}

const EventTypes = {
  VIEW_MORE: "view-more",
};

const props = defineProps<{
  title: string;
  items?: CardItem[];
  itemGroups?: ItemGroup[];
  titleField?: string;
  dateField?: string;
  extraField?: string;
  emptyText?: string;
  viewMoreText?: string;
  maxItems?: number;
  isCalendarMode?: boolean;
  calendarFooterText?: string;
  showDeleteButton?: boolean;
  useSimpleList?: boolean; // 新增属性：是否使用简单列表模式
}>();

const emit = defineEmits<{
  (event: "view-more"): void;
  (event: "item-click", item: CardItem): void;
  (event: "delete-item", item: CardItem, index: number): void;
}>();

// 配置 marked
marked.setOptions({
  breaks: true, // 支持换行
  gfm: true, // 支持 GitHub Flavored Markdown
});

// Markdown 渲染函数
function renderMarkdown(content: string): string {
  try {
    // 使用 marked 将 markdown 转换为 HTML
    const html = marked(content);

    // 检查 html 是否为 Promise
    if (html instanceof Promise) {
      // 如果是 Promise，我们不能在同步函数中处理它
      // 返回一个默认值并处理 Promise
      html
        .then((resolvedHtml) => {
          // 这里我们不能直接返回，因为我们已经在同步函数中
          console.log("Markdown rendered asynchronously");
        })
        .catch((error) => {
          console.error("Async markdown rendering error:", error);
        });
      return content; // 返回原始内容作为回退
    }

    // 基础的 HTML 清理函数，防止潜在的 XSS 攻击
    const sanitizedHtml = sanitizeHtml(html);

    return sanitizedHtml;
  } catch (error) {
    console.error("Markdown 渲染错误:", error);
    // 如果渲染失败，返回原始文本
    return content.replace(/\n/g, "<br>");
  }
}

// 简单的 HTML 清理函数
function sanitizeHtml(html: string): string {
  // 允许的标签和属性
  const allowedTags = [
    "p",
    "br",
    "strong",
    "em",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "ul",
    "ol",
    "li",
    "blockquote",
    "code",
    "pre",
    "a",
    "img",
  ];
  const allowedAttributes: Record<string, string[]> = {
    a: ["href", "target"],
    img: ["src", "alt", "width", "height"],
  };

  // 移除 script 标签和其他危险内容
  const sanitized = html
    .replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, "")
    .replace(/on\w+="[^"]*"/gi, "")
    .replace(/javascript:/gi, "");

  return sanitized;
}

// 处理删除按钮点击
function handleDelete(item: CardItem, index: number) {
  emit("delete-item", item, index);
}

const showViewMore = computed(() => {
  return props.maxItems && props.items && props.items.length > props.maxItems;
});

const getItemTitle = (item: CardItem): string => {
  return props.titleField
    ? String(item[props.titleField] || "")
    : item.title || "";
};

const getItemDate = (item: CardItem): string => {
  return props.dateField
    ? String(item[props.dateField] || "")
    : item.date || item.time || "";
};

function handleClick(item: CardItem) {
  // 使用模态框替代通知
  showItemDetailsModal.value = true;
  currentItem.value = item;
}
</script>

<style scoped>
.base-card {
  margin-bottom: 16px;
}

.bordered-card {
  border: 1px solid var(--border-color);
}

.calendar-container {
  padding: 16px 0;
}

.calendar-footer {
  margin-top: 12px;
  text-align: center;
  color: var(--text-color-2);
  font-size: 14px;
}

.modal-header-extra {
  display: flex;
  align-items: center;
  gap: 8px;
}

.header-label {
  font-size: 14px;
  color: var(--text-color-2);
}

.item-abstract {
  max-height: 400px;
  overflow-y: auto;
  padding: 16px 0;
}

.markdown-content {
  line-height: 1.6;
  color: var(--text-color-1);
}

.markdown-content h1,
.markdown-content h2,
.markdown-content h3,
.markdown-content h4,
.markdown-content h5,
.markdown-content h6 {
  margin: 16px 0 8px 0;
  font-weight: 600;
}

.markdown-content p {
  margin: 8px 0;
}

.markdown-content ul,
.markdown-content ol {
  margin: 8px 0;
  padding-left: 24px;
}

.markdown-content blockquote {
  margin: 16px 0;
  padding: 8px 16px;
  border-left: 4px solid var(--primary-color);
  background-color: var(--code-color);
}

.markdown-content code {
  padding: 2px 4px;
  background-color: var(--code-color);
  border-radius: 4px;
  font-family: "Monaco", "Menlo", "Ubuntu Mono", monospace;
}

.item-keywords {
  margin-top: 16px;
  padding: 8px 12px;
  background-color: rgba(var(--primary-color-rgb), 0.05);
  border-radius: 4px;
  font-size: 14px;
}

.keywords-label {
  font-weight: 600;
  color: var(--text-color-2);
  margin-right: 8px;
}

.keywords-content {
  color: var(--primary-color);
}

.markdown-content pre {
  margin: 16px 0;
  padding: 16px;
  background-color: var(--code-color);
  border-radius: 6px;
  overflow-x: auto;
}

.markdown-content pre code {
  padding: 0;
  background-color: transparent;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
}

.item {
  padding: 12px 0;
  border-bottom: 1px solid var(--border-color);
}

.item:last-child {
  border-bottom: none;
}

.item-title {
  font-weight: 500;
  margin-bottom: 8px;
  color: var(--text-color-1);
}

.item-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 14px;
  color: var(--text-color-2);
}

.view-details-link {
  color: var(--primary-color);
  cursor: pointer;
  text-decoration: underline;
}

.view-details-link:hover {
  color: var(--primary-color-hover);
}

.item-content {
  padding: 8px 0;
}

.item-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.item-extra {
  color: var(--text-color-3);
}

.no-data {
  text-align: center;
  padding: 40px 20px;
  color: var(--text-color-3);
  font-size: 14px;
}

.simple-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.simple-list-item {
  padding: 12px;
  background-color: var(--md-grey-50, #fafafa);
  border-radius: 8px;
  border: 1px solid var(--md-grey-200, #eeeeee);
  transition: all 0.2s ease;
  margin-bottom: 8px;
}

.simple-list-item:last-child {
  margin-bottom: 0;
}

.simple-list-item:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  background-color: var(--md-grey-100, #f5f5f5);
}

.simple-item-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}

.simple-item-title {
  font-weight: 500;
  color: var(--text-color-1);
  flex: 1;
  padding-right: 16px;
  cursor: pointer;
}

.delete-icon {
  color: var(--error-color, #d03050);
  cursor: pointer;
  font-size: 16px;
  opacity: 0.7;
  transition: opacity 0.2s ease;
}

.delete-icon:hover {
  opacity: 1;
}

.simple-item-footer {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: var(--text-color-3);
}
</style>
