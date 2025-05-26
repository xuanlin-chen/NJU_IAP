import { defineStore } from "pinia";
import { convertKey } from "@/utils/convert";
import dayjs from "dayjs";
type Dayjs = dayjs.Dayjs;

// API URLs
const api_url = "http://localhost:5000/api/" as const;
const api_router = {
	today: `${api_url}news/today`,
	ddl: `${api_url}ddl-events`,
	docs: `${api_url}docs`,
	query: `${api_url}konwledge/query`,
} as const;

type ApiUrl = (typeof api_router)[keyof typeof api_router];
type Summary = ddlSummary | newsSummary;

// Types
interface original {
	date: string;
	summary: Summary;
	abstract?: string;
}

interface newsSummary {
	type: string;
	title: string;
	keywords: string[];
	source: URL;
}

interface ddlSummary {
	type: string;
	title: string;
	time: Dayjs; // 格式: "HH:MM" 24小时制
	source: URL;
}

export interface DdlItem {
	title: string;
	date: Dayjs; // 格式: "YYYY-MM-DD"
	time: Dayjs; // 格式: "HH:MM" 24小时制
}

export interface Message {
	title: string;
	time: string;
	source: URL;
  type: string; // 添加类型字段
}

// State interface
interface DashboardState {
	ddlData: DdlItem[];
	todayMessages: Message[];
	historyMessages: Message[];
	isLoading: boolean;
	error: string | null;
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
					data: original[];
				}>(api_router.ddl);

				this.ddlData = data.data.map((item: original) => ({
					title: item.summary.title,
					date: dayjs(item.date),
					time: dayjs((item.summary as ddlSummary).time || "00:00", "HH:mm"),
				}));
			} catch (error) {
				console.error("Failed to fetch DDL data:", error);
			}
		},

		// 获取今日消息
		async fetchTodayMessages() {
			try {
				const data = await this.fetchData<{ code: number; data: original[] }>(
					api_router.today,
				);

				this.todayMessages = data.data.map((item: original) => ({
          title: item.summary.title,
          time: dayjs(item.date).format("YYYY-MM-DD HH:mm"),
          source: new URL(item.summary.source.toString()),
          type: item.summary.type, // 添加类型字段
        }));
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
export async function useDashboardData() {
	const store = useDashboardStore();

	// 初始化 store 数据
	if (store.ddlData.length === 0) {
		await store.initialize();
	}

	return {
		ddlData: store.ddlData,
		Messages: store.todayMessages,
		refreshData: store.refreshAllData,
	};
}
