import { defineStore } from "pinia";
import { convertKey } from "@/utils/convert";

// API URLs
const api_url = "http://localhost:5000/api/" as const;
const api_router = {
	today: `${api_url}news/today`,
	ddl: `${api_url}ddl-events`,
	docs: `${api_url}docs`,
	query: `${api_url}konwledge/query`,
} as const;

type ApiUrl = (typeof api_router)[keyof typeof api_router];

// Types
interface DdlOriginal {
	date: string;
	summary: Summary;
}

interface Summary {
	type: string;
	title: string;
	time: string;
	source: string;
}

export interface DdlItem {
	title: string;
	date: string; // 格式: "YYYY-MM-DD"
	time: string; // 格式: "HH:MM" 24小时制
}

export interface TodayMessage {
	title: string;
	time: string;
	source: string;
}

export interface HistoryMessage {
	title: string;
	date: string;
	views: number;
}

// State interface
interface DashboardState {
	ddlData: DdlItem[];
	todayMessages: TodayMessage[];
	historyMessages: HistoryMessage[];
	isLoading: boolean;
	error: string | null;
}

/**
 * 将时间格式化为 "HH:MM" 格式
 */
function formatTimeString(timeString: string): string {
	// 如果已经是 HH:MM 格式，直接返回
	if (/^([01]?[0-9]|2[0-3]):[0-5][0-9]$/.test(timeString)) {
		return timeString;
	}

	try {
		// 尝试解析时间
		const date = new Date(`1970-01-01T${timeString}`);
		if (!Number.isNaN(date.getTime())) {
			return `${String(date.getHours()).padStart(2, "0")}:${String(date.getMinutes()).padStart(2, "0")}`;
		}
	} catch (e) {
		console.warn("无法解析时间格式:", timeString);
	}

	return "00:00"; // 默认时间
}

// Dashboard Store
export const useDashboardStore = defineStore("dashboard", {
	// State
	state: (): DashboardState => ({
		ddlData: [],
		todayMessages: [],
		historyMessages: [],
		isLoading: false,
		error: null,
	}),

	// Getters
	getters: {
		getDdlByDate: (state) => (date: string) => {
			return state.ddlData.filter((item) => item.date === date);
		},

		getTodayDdl: (state) => {
			const today = new Date().toISOString().slice(0, 10);
			return state.ddlData.filter((item) => item.date === today);
		},

		getRecentDdl: (state) => {
			const today = new Date();
			const oneWeekLater = new Date(today);
			oneWeekLater.setDate(today.getDate() + 7);

			return state.ddlData.filter((item) => {
				const itemDate = new Date(item.date);
				return itemDate > today && itemDate <= oneWeekLater;
			});
		},
	},

	// Actions
	actions: {
		// 通用数据获取
		async fetchData<T>(url: ApiUrl): Promise<T> {
			try {
				this.isLoading = true;
				this.error = null;

				const response = await fetch(url);
				if (!response.ok) {
					throw new Error(`HTTP error! status: ${response.status}`);
				}

				const data = await response.json();
				return convertKey(data) as T;
			} catch (error) {
				const errorMessage =
					error instanceof Error ? error.message : String(error);
				this.error = errorMessage;
				console.error(`Error fetching data from ${url}:`, error);
				throw error;
			} finally {
				this.isLoading = false;
			}
		},

		// 获取DDL数据
		async fetchDdlData() {
			try {
				const data = await this.fetchData<{
					code: number;
					data: DdlOriginal[];
				}>(api_router.ddl);

				this.ddlData = data.data.map((item: DdlOriginal) => ({
					title: item.summary.title,
					date: item.date,
					time: formatTimeString(item.summary.time || "00:00"),
				}));
			} catch (error) {
				console.error("Failed to fetch DDL data:", error);
			}
		},

		// 获取今日消息
		async fetchTodayMessages() {
			try {
				const data = await this.fetchData<{ code: number; data: any[] }>(
					api_router.today,
				);

				if (data.code === 200) {
					this.todayMessages = data.data.map((item) => ({
						title: item.title,
						time: formatTimeString(item.time || "00:00"),
						source: item.source || "未知来源",
					}));
				}
			} catch (error) {
				console.error("Failed to fetch today messages:", error);
			}
		},

		// 初始化所有数据
		async initialize() {
			this.isLoading = true;
			try {
				await Promise.all([
					this.fetchDdlData(),
					this.fetchTodayMessages(),
					// 可以添加其他数据获取方法
				]);
			} catch (error) {
				console.error("Error initializing dashboard data:", error);
			} finally {
				this.isLoading = false;
			}
		},

		// 刷新所有数据
		async refreshAllData() {
			return this.initialize();
		},
	},
});

// 导出简化版本的 useDashboardData 以保持向后兼容
export function useDashboardData() {
	const store = useDashboardStore();

	// 初始化 store 数据
	if (store.ddlData.length === 0) {
		store.initialize();
	}

	return {
		ddlData: store.ddlData,
		todayMessages: store.todayMessages,
		historyMessages: store.historyMessages,
		refreshData: store.refreshAllData,
	};
}
