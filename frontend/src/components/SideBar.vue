<script setup lang="ts">
import { h, ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import type { Component } from 'vue'
// Import only the needed components from naive-ui
import { NLayoutSider } from 'naive-ui'
import { NMenu } from 'naive-ui'
import { NIcon } from 'naive-ui'
import { NButton } from 'naive-ui'

// Lazy load icon components only when needed
import { 
  BookOutline as BookIcon,
  HomeOutline as HomeIcon,
  InformationCircleOutline as InfoIcon,
  BarChartOutline as ChartIcon,
  MenuOutline as MenuIcon,
  ChevronBackOutline as ChevronBackIcon,
  SettingsOutline as SettingsIcon
} from '@vicons/ionicons5'
import sidebarText from '../resource/components/sidebar'
import { useSidebarStore } from '@/stores/sidebarStore';

const sidebarStore = useSidebarStore();

const router = useRouter()
const route = useRoute()

// 计算当前活动菜单项
const activeKey = computed(() => {
  const path = route.path
  if (path === '/') return 'home'
  // 去掉路径前面的斜杠
  return path.substring(1)
})

function renderIcon(icon: Component) {
  return () => h(NIcon, null, { default: () => h(icon) })
}

const menuOptions = [
  {
    label: sidebarText.menuItems.home,
    key: 'home',
    icon: renderIcon(HomeIcon)
  },
  {
    label: sidebarText.menuItems.dashboard,
    key: 'dashboard',
    icon: renderIcon(ChartIcon)
  },
  {
    label: sidebarText.menuItems.chat,
    key: 'chat',
    icon: renderIcon(BookIcon)
  },
  {
    label: sidebarText.menuItems.about,
    key: 'about',
    icon: renderIcon(InfoIcon)
  },
  {
    label: sidebarText.menuItems.settings,
    key: 'settings',
    icon: renderIcon(SettingsIcon)
  }
]

// 处理菜单选择事件
const handleMenuSelect = (key: string) => {
  router.push(`/${key === 'home' ? '' : key}`)
  // 在移动设备上选择菜单项后自动折叠侧边栏
  if (window.innerWidth < 768) {
    sidebarStore.collapsed = true
  }
}

// 切换侧边栏显示/隐藏
const toggleSidebar = () => {
  sidebarStore.collapsed = !sidebarStore.collapsed
}
</script>

<template>
  <div class="sidebar-container">
    <!-- 侧边栏切换按钮 -->
    <div class="sidebar-toggle" @click="toggleSidebar">
      <n-button circle>
        <template #icon>
          <n-icon>
            <MenuIcon v-if="sidebarStore.collapsed" />
            <ChevronBackIcon v-else />
          </n-icon>
        </template>
      </n-button>
    </div>
    
    <!-- 侧边栏遮罩层 -->
    <div 
      v-show="!sidebarStore.collapsed" 
      class="sidebar-overlay"
      @click="sidebarStore.collapsed = true"
    ></div>
    
    <!-- 侧边栏内容 -->
    <n-layout-sider
      bordered
      collapse-mode="width"
      :collapsed-width="0"
      :width="240"
      :collapsed="sidebarStore.collapsed"
      :native-scrollbar="false"
      class="sidebar"
      :class="{ 'sidebar-expanded': !sidebarStore.collapsed }"
    >
      <div class="logo-container">
        <img alt="Logo" class="logo" src="../assets/nju.svg" />
        <span v-if="!sidebarStore.collapsed" class="platform-title">{{ sidebarText.title }}</span>
      </div>
      <n-menu
        :collapsed-width="64"
        :collapsed-icon-size="22"
        :options="menuOptions"
        :value="activeKey"
        @update:value="handleMenuSelect"
      />
      <div v-if="!sidebarStore.collapsed" class="footer">
        <div class="version">{{ sidebarText.footer.version }} 2.0.0</div>
        <div class="copyright">{{ sidebarText.footer.copyright }}</div>
      </div>
    </n-layout-sider>
  </div>
</template>

<style scoped>
.sidebar-container {
  position: relative;
}

.sidebar-toggle {
  position: fixed;
  top: 20px;
  left: 20px;
  z-index: 200;
  transition: left 0.3s;
}

.sidebar {
  position: fixed;
  top: 0;
  left: 0;
  height: 100%;
  z-index: 150;
  background-color: #ffffff;
  color: #333333;
  border-right: 1px solid rgba(0, 0, 0, 0.08);
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
  transform: translateX(-100%);
}

.sidebar-expanded {
  transform: translateX(0);
}

.sidebar-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 120;
}

.logo-container {
  padding: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 40px; /* 为顶部菜单按钮留出空间 */
}

.platform-title {
  margin-left: 12px;
  font-size: 16px;
  font-weight: 600;
}

.logo {
  width: 40px;
  height: 40px;
}

.footer {
  position: absolute;
  bottom: 20px;
  left: 0;
  right: 0;
  padding: 0 16px;
  text-align: center;
  font-size: 12px;
  color: rgba(0, 0, 0, 0.45);
}

.version {
  margin-bottom: 4px;
}

/* 确保菜单项文本颜色为黑色 */
:deep(.n-menu-item-content) {
  color: rgba(0, 0, 0, 0.85);
}

:deep(.n-menu-item-content__icon) {
  color: rgba(0, 0, 0, 0.85);
}

:deep(.n-menu-item-content.n-menu-item-content--selected) {
  color: #2080f0;
}

/* 响应式调整 */
@media (min-width: 768px) {
  .sidebar-toggle {
    left: 350px; /* 调整按钮位置到侧边栏右侧 */
  }
}
</style>