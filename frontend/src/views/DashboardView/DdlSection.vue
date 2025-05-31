<template>
  <div style="position: relative">
    <base-card
      :title="dashboardText.ddlNews.title"
      :items="formattedDdlItems"
      extra-field="description"
      :empty-text="dashboardText.dayMessages.noMessages"
      :view-more-text="dashboardText.ddlNews.viewMore"
      :show-delete-button="true"
      :use-simple-list="true"
      @view-more="handleViewMoreDdl"
      @delete-item="handleDeleteDdl"
    />

    <!-- 添加浮动按钮用于添加DDL -->
    <n-float-button
      type="default"
      position="absolute"
      style="right: 16px; top: 16px"
      @click="handleAddDdl"
    >
      <AddIcon />
    </n-float-button>
  </div>
</template>

<script setup lang="ts">
import { computed, inject, ref } from "vue";
import { NFloatButton } from "naive-ui";
import BaseCard from "../../components/BaseCard.vue";
import dashboardText from "../../resource/dashboard";
import dayjs from "dayjs";
import AddIcon from "@/components/icons/AddIcon.vue";
import type { CardItem } from "../../components/BaseCard.vue";
import type { DdlEvent } from "../../stores/dashboardStore";
import { useUserStore } from "@/stores/userStore";

// 注入共享状态
const dashboardState = inject("dashboardState") as {
  ddlData: { value: DdlEvent[] };
  selectedDate: { value: Date };
  loading: { value: boolean };
  message: {
    success: (text: string) => void;
    error: (text: string) => void;
    info: (text: string) => void;
    warning: (text: string) => void;
  };
  showAddDdlModal: { value: boolean };
  newDdl: { value: {
    title: string;
    dateTimestamp: number | null;
    timeTimestamp: number | null;
    source: string;
  }};
  toggleAddDdlModal: (show: boolean) => void;
};

// 解构以便更容易使用
const { ddlData, selectedDate, loading, message, showAddDdlModal, newDdl } = dashboardState;

// 格式化 DDL 数据为 CardItem 类型
const formattedDdlItems = computed(() => {
  if (!ddlData.value || ddlData.value.length === 0) return [];
  console.log("Formatted DDL items:", ddlData.value);
  return ddlData.value.map((item) => {
    const timeStr = item.summary.time
      ? dayjs(item.summary.time).format("YYYY-MM-DD HH:mm")
      : "";
    return {
      title: item.summary.title || "未命名DDL",
      date: timeStr,
      description: item.summary.source || "",
      abstract: item.summary.title || "", // 保存完整内容以便在详情中查看
    } as CardItem;
  });
});

function handleViewMoreDdl() {
  message.info("查看更多DDL消息");
}

// 处理添加DDL按钮点击事件
function handleAddDdl() {
  // 重置表单
  newDdl.value = {
    title: "",
    dateTimestamp: selectedDate.value.getTime(), // 预设为当前选中日期
    timeTimestamp: null,
    source: "",
  };
  // 显示对话框
  showAddDdlModal.value = true;
}

// 处理删除DDL项目
async function handleDeleteDdl(item: CardItem, index: number) {
  try {
    // 使用Naive UI的message组件进行确认
    if (!window.confirm(`确定要删除"${item.title}"吗？`)) {
      return;
    }

    loading.value = true;

    // 根据标题和日期匹配
    const ddlIndex = ddlData.value.findIndex(
      (ddlItem) =>
        ddlItem.summary.title === item.title
    );

    if (ddlIndex === -1) {
      message.error("无法找到要删除的DDL项目");
      return;
    }

    // 调用后端API删除DDL
    const result = await useUserStore().removeCustomDdl(ddlIndex);

    if (result) {
      message.success("DDL删除成功");

      // 从本地数据中删除
      ddlData.value.splice(ddlIndex, 1);
    } else {
      message.error("DDL删除失败");
    }
  } catch (error) {
    console.error("删除DDL失败:", error);
    message.error("删除DDL失败");
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
/* DDL部分的特定样式 */
</style>
