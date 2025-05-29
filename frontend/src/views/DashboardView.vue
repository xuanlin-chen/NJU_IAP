<script>
import { defineComponent } from "vue"
import DashboardView from "./DashboardView/index.vue"

export default defineComponent({
  name: "DashboardViewRedirect",
  extends: DashboardView
})
</script>

<template>
  <!-- 此组件已被拆分，现由 DashboardView/index.vue 导入并重定向 -->
  <DashboardView />
</template>
