<template>
  <div style="position: relative">
    <base-card
      :title="dashboardText.ddlNews.title"
      :item-groups="formattedDdlItems"
      extra-field="description"
      :empty-text="dashboardText.dayMessages.noMessages"
      :view-more-text="dashboardText.ddlNews.viewMore"
      :show-delete-button="true"
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
import { computed, inject } from "vue";
import { NFloatButton } from "naive-ui";
import BaseCard from "../../components/BaseCard.vue";
import dashboardText from "../../resource/dashboard";
import AddIcon from "@/components/icons/AddIcon.vue";
import type { CardItem } from "../../components/BaseCard.vue";
import type { DdlItem } from "../../stores/dashboardStore";
import { useUserStore } from "@/stores/userStore";

// 注入共享状态
const dashboardState = inject("dashboardState") as {
  ddlData: { value: DdlItem[] };
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
    type: string;
    source: string;
  }};
  toggleAddDdlModal: (show: boolean) => void;
};

// 解构以便更容易使用
const { ddlData, selectedDate, loading, message, showAddDdlModal, newDdl } = dashboardState;

// 格式化 DDL 数据为 CardItem 类型
const formattedDdlItems = computed(() => {
  console.debug("Formatting DDLs for date:", selectedDate.value);
  
  // 检查是否有 DDL 数据
  if (!ddlData.value || ddlData.value.length === 0) {
    return [];
  }  
  // 过滤并转换 DDL 数据
  const filteredItems = ddlData.value
    .filter(item => {
      // 确保 item.date 存在并且有 format 方法
      if (!item.date || typeof item.date.format !== 'function') return false;
      
      // 比较日期字符串
      return item.date.format('YYYY-MM-DD') ;
    })
    .map(item => {
      // 处理 source 字段
      let sourceStr = "";
      if (item.source) {
        if (typeof item.source === "string") {
          sourceStr = item.source;
        } else {
          // 是 URL 对象
          sourceStr = item.source.href;
        }
      }

      // 创建显示在卡片中的描述文本，现在包含类型信息
      let description = item.time ? `${item.time.format("HH:mm")}` : "";
      if (item.type) {
        description = description ? `${description} | ${item.type}` : item.type;
      }

      return {
        title: item.title || "",
        date: item.date ? item.date.format("YYYY-MM-DD") : "",
        time: item.time ? item.time.format("HH:mm") : "",
        description: description,
        source: sourceStr,
        type: item.type, // 添加类型字段
      };
    });
  
  console.debug("Filtered DDL Items:", filteredItems);
  return [
    {
      groupTitle: "DDL",
      items: filteredItems,
    }
  ];
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
    type: "用户自定义", // 设置默认类型
  };
  // 显示对话框
  showAddDdlModal.value = true;
}

// 处理删除DDL项目
async function handleDeleteDdl(item: CardItem, index: number) {
  try {
    // 确认是否要删除
    if (!window.confirm("确定要删除这个DDL吗？")) {
      return;
    }

    loading.value = true;

    // 根据标题和日期匹配
    const ddlIndex = ddlData.value.findIndex(
      (ddlItem) =>
        ddlItem.title === item.title &&
        ddlItem.date.format("YYYY-MM-DD") === item.date
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
