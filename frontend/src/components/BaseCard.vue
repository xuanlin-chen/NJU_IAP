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
                <span @click.stop="handleClick(item)"> 查看详情 </span>
              </div>
            </div>
          </n-collapse-item>
        </n-collapse>
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
              <div class="item-footer"></div>
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
import { computed, h } from "vue";
import {
  NCard,
  NCollapse,
  NCollapseItem,
  NAvatar,
  createDiscreteApi,
} from "naive-ui";
import { marked } from "marked";

const { notification } = createDiscreteApi(["notification"]);

export interface CardItem {
  title?: string;
  date?: string;
  time?: string;
  type?: string;
  abstract?: string;
  description?: string;
  source?: string | URL;
  views?: number;
  [key: string]: any;
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
}>();

defineEmits<{
  (event: "view-more"): void;
  (event: "item-click", item: CardItem): void;
}>();

const showViewMore = computed(() => {
  return props.maxItems && props.items && props.items.length > props.maxItems;
});

const getItemTitle = (item: CardItem): string => {
  return props.titleField ? item[props.titleField] : item.title || "";
};

const getItemDate = (item: CardItem): string => {
  return props.dateField ? item[props.dateField] : item.date || item.time || "";
};

function handleClick(item: CardItem) {
  notification.create({
    title: item.title || "详情",
    description: () =>
      h(
        "div",
        {
          style:
            "display: flex; justify-content: space-between; align-items: center;",
        },
        [
          h("span", {}, "智能摘要"),
          item.source
            ? h(
                "a",
                {
                  href: typeof item.source === 'string' ? item.source : item.source.href,
                  target: "_blank",
                  style: {
                    fontSize: "12px",
                    color: "var(--primary-color)",
                    textDecoration: "none",
                  },
                  onClick: (e: Event) => {
                    e.stopPropagation();
                  },
                },
                "查看原文"
              )
            : null,
        ]
      ),
    content: () =>
      h("div", {
        innerHTML: marked(item.abstract || "暂无摘要"),
      }),
    avatar: () =>
      h(NAvatar, {
        size: "small",
        round: true,
        src: "https://07akioni.oss-cn-beijing.aliyuncs.com/07akioni.jpeg",
      }),
    action: () =>
      h("div", [
        h(
          "a",
          {
            href: typeof item.source === 'string' ? item.source : (item.source ? item.source.href : ''),
            target: item.source ? "_blank" : undefined,
            style: {
              marginRight: "10px",
              color: "var(--primary-color)",
            },
          },
          "查看原文"
        ),
      ]),
  });
}
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
  min-height: 300px;
  /* 保持卡片高度一致，防止抖动 */
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
</style>
