<template>
  <div class="user-settings">
    <h2>用户设置</h2>
    
    <!-- 自定义DDL管理 -->
    <div class="settings-section">
      <h3>自定义DDL管理</h3>
      
      <!-- 添加新DDL -->
      <div class="add-ddl">
        <n-input
          v-model:value="newDdlContent"
          type="text"
          placeholder="输入新的DDL内容"
          :disabled="userStore.loading"
          class="ddl-content-input"
        />
        <n-date-picker
          v-model:value="newDdlTime"
          type="datetime"
          clearable
          placeholder="选择DDL日期和时间"
          :disabled="userStore.loading"
          class="ddl-time-picker"
        />
        <n-button
          @click="handleAddDdl"
          type="primary"
          :loading="userStore.loading"
          :disabled="!newDdlContent || !newDdlTime"
        >
          添加
        </n-button>
      </div>
      
      <!-- DDL列表 -->
      <div class="ddl-list" v-if="userStore.user?.custom_ddls?.length">
        <n-list>
          <n-list-item v-for="(ddl, index) in userStore.user.custom_ddls" :key="index">
            <div class="ddl-item">
              <span>{{ ddl }}</span>
              <n-button 
                @click="handleRemoveDdl(index)" 
                quaternary 
                circle 
                type="error"
                :loading="loadingIndices[index]"
              >
                <n-icon><trash-icon /></n-icon>
              </n-button>
            </div>
          </n-list-item>
        </n-list>
      </div>
      <div v-else class="empty-tip">
        暂无自定义DDL
      </div>
    </div>
    
    <!-- 公众号订阅管理 -->
    <div class="settings-section">
      <h3>公众号订阅管理</h3>
      
      <div class="accounts-selection">
        <n-transfer
          v-model:value="unsubscribedAccounts"
          :options="accountOptions"
          source-title="所有公众号"
          target-title="不想看的公众号"
        />
        
        <div class="action-buttons">
          <n-button 
            @click="handleSaveAccounts" 
            type="primary" 
            :loading="userStore.loading"
          >
            保存设置
          </n-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { 
  NInput, 
  NButton, 
  NList, 
  NListItem, 
  NIcon,
  NTransfer,
  useMessage,
  NDatePicker // Add NDatePicker import
} from 'naive-ui';
import { useUserStore } from '@/stores/userStore';
import { TrashOutline as TrashIcon } from '@vicons/ionicons5';
import dayjs from 'dayjs';

const userStore = useUserStore();
const message = useMessage();

// DDL部分
const newDdlContent = ref('');
const newDdlTime = ref<number | null>(null); // Store timestamp
const loadingIndices = ref<Record<number, boolean>>({});

// 添加自定义DDL
const handleAddDdl = async () => {
  if (!newDdlContent.value.trim() || !newDdlTime.value) return;

  const ddlEvent = {
    summary: {
      title: newDdlContent.value,
      time: dayjs(newDdlTime.value) // Convert timestamp to dayjs object
    },
    content: newDdlContent.value // Keep content for now, though it might be redundant
  };
  
  const result = await userStore.addCustomDdl(ddlEvent);
  if (result.success) {
    message.success('添加成功');
    newDdlContent.value = '';
    newDdlTime.value = null; // Clear selected time
  } else {
    message.error(result.error || '添加失败');
  }
};

// 删除自定义DDL
const handleRemoveDdl = async (index: number) => {
  loadingIndices.value[index] = true;
  
  const result = await userStore.removeCustomDdl(index);
  if (result.success) {
    message.success('删除成功');
  } else {
    message.error(result.error || '删除失败');
  }
  
  loadingIndices.value[index] = false;
};

// 公众号部分
// 模拟的公众号列表数据，实际应该从API获取
const availableAccounts = [
  '南京大学新生学院',
  '南京大学',
  '南京大学图书馆',
  '南大全球交流',
  '南青科创',
  '南大社团',
  '南大体育',
  '南大港澳台交流',
  '南大高研院',
  '南商满天星',
  '南京大学安邦书院',
  '南京大学行知书院',
  '南京大学健雄书院',
  '南京大学有训书院',
  '南京大学开甲书院',
  '南京大学秉文书院',
  '南京大学毓琇书院'
];

const unsubscribedAccounts = ref<string[]>([]);

// 初始化不想看的公众号
onMounted(() => {
  if (userStore.user?.unsubscribed_accounts) {
    unsubscribedAccounts.value = [...userStore.user.unsubscribed_accounts];
  }
});

// 转换为Transfer组件需要的格式
const accountOptions = computed(() => {
  return availableAccounts.map(account => ({
    label: account,
    value: account
  }));
});

// 保存公众号设置
const handleSaveAccounts = async () => {
  const result = await userStore.updateUnsubscribedAccounts(unsubscribedAccounts.value);
  if (result.success) {
    message.success('保存成功');
  } else {
    message.error(result.error || '保存失败');
  }
};
</script>

<style scoped>
.user-settings {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.settings-section {
  margin-bottom: 40px;
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
}

h2 {
  margin-bottom: 24px;
  color: #333;
}

h3 {
  margin-bottom: 16px;
  color: #444;
  border-bottom: 1px solid #eee;
  padding-bottom: 8px;
}

.add-ddl {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.ddl-content-input {
  flex-grow: 1;
}

.ddl-time-picker {
  width: 200px; /* Adjust width as needed */
}

.ddl-list {
  margin-top: 16px;
}

.ddl-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.empty-tip {
  color: #999;
  font-style: italic;
  margin: 20px 0;
  text-align: center;
}

.accounts-selection {
  margin-top: 20px;
}

.action-buttons {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>
