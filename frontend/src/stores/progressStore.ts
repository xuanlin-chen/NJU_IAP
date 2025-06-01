import { defineStore } from "pinia";
import { ref } from "vue";

// API路由
const api_router = {
    queryProgress: (queryId: string) => `/api/query-progress/${queryId}`,
};

// API响应接口
interface ApiResponse {
    code: number;
    data: {
        status: string;
        message: string;
        progress: number;
        completed: boolean;
    };
    message: string;
    errors?: string;
}

export const useProgressStore = defineStore("progress", () => {
    const isPolling = ref(false);
    const progressMessage = ref("");
    const progress = ref(0);
    const error = ref<string | null>(null);
    const completed = ref(false);
    const pollingInterval = ref<number | null>(null);

  // 开始轮询
    const startPolling = (queryId: string, resetProgress: boolean = true) => {
        if (isPolling.value) return;
        
        isPolling.value = true;
        completed.value = false;
        
        if (resetProgress) {
            progressMessage.value = "正在处理您的请求...";
            progress.value = 0;
        }

        error.value = null;
        
        // 设置轮询间隔
        pollingInterval.value = window.setInterval(() => {
            checkProgress(queryId);
        }, 1000);
    };

  // 停止轮询
    const stopPolling = () => {
        if (pollingInterval.value) {
            window.clearInterval(pollingInterval.value);
            pollingInterval.value = null;
        }
        isPolling.value = false;
    };

  // 检查进度
    const checkProgress = async (queryId: string) => {
        try {
        const response = await fetch(api_router.queryProgress(queryId));
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result: ApiResponse = await response.json();
        
        // 检查API响应
        if (result.code !== 200) {
            throw new Error(result.message || "获取进度信息失败");
        }
        
        // 更新进度信息
        progressMessage.value = result.data.message || "处理中...";
        progress.value = result.data.progress || 0;
        
        // 如果完成，停止轮询
        if (result.data.completed) {
            completed.value = true;
            stopPolling();
        }
        } catch (e) {
        error.value = e instanceof Error ? e.message : "获取进度信息失败，请稍后重试";
        stopPolling();
        }
    };

    return {
        isPolling,
        progressMessage,
        progress,
        error,
        completed,
        startPolling,
        stopPolling,
    };
    });