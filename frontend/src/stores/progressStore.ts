import { defineStore } from "pinia";
import { ref } from "vue";

const api_router = {
    queryProgress: (queryId: string) => `/api/query-progress/${queryId}`,
};

interface ApiResponse {
    code: number;
    data: {
        status: string;
        message: string;
        progress: number;
        completed: boolean;
        recommendation?: string;
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

    const startPolling = (queryId: string, resetProgress: boolean = true, keepRun = false) => {
        if (isPolling.value && !keepRun) return;
        
        isPolling.value = true;
        completed.value = false;
        
        if (resetProgress) {
            progressMessage.value = "正在处理您的请求...";
            progress.value = 0;
        }

        error.value = null;
        
        pollingInterval.value = window.setInterval(() => {
            checkProgress(queryId);
        }, 1000);
    };

    const stopPolling = (keepRun: boolean = false) => {
        if (pollingInterval.value) {
            window.clearInterval(pollingInterval.value);
            pollingInterval.value = null;
        }
            isPolling.value = keepRun;
    };

    const checkProgress = async (queryId: string) => {
        try {
            const response = await fetch(api_router.queryProgress(queryId), {
                credentials: 'include'
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const result: ApiResponse = await response.json();
            
            if (result.code !== 200) {
                throw new Error(result.message || "获取进度信息失败");
            }
            
            progressMessage.value = result.data.message || "处理中...";
            progress.value = result.data.progress || 0;
            
            // 如果检索完成，停止轮询并更新聊天消息
            if (result.data.completed) {
                completed.value = true;
                stopPolling();
                
                // 如果有返回结果，更新到聊天消息
                if (result.data.recommendation) {
                    // 这里需要访问chatStore来更新消息
                    // 选择通过事件总线或其他方式通知chatStore
                    const event = new CustomEvent('mcp-result-ready', { 
                        detail: { recommendation: result.data.recommendation }
                    });
                    window.dispatchEvent(event);
                }
            }
        } catch (e) {
            error.value = e instanceof Error ? e.message : "获取进度信息失败，请稍后重试";
            stopPolling();
        }
    };

    const getQueryProgress = async (queryId: string) => {
        try {
            const response = await fetch(api_router.queryProgress(queryId), {
                credentials: 'include'
            });
            const result: ApiResponse = await response.json();
            return result;
        } catch (error) {
            console.error('获取查询进度失败:', error);
            throw error;
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
        getQueryProgress,
    };
});