import { defineStore } from "pinia";
import { convertKey } from "@/utils/convert";
import type { DateString } from "@/utils/DateString";
import dayjs from "dayjs";
import type { eventTypes } from '../resource/map';

const api_router = {
	dateQuery: (date: DateString) => `/api/date-query?date=${date}`,
};

interface ApiResponse {
	code: number;
	data: ApiData;
	message: string;
}

interface ApiData {
	ddl_events?: DdlEvent[];
	news?: NewsItem[];
}

export interface DdlEvent {
	summary: {
		time?: dayjs.Dayjs; // 可选摘要时间
		source?: string; // 可选摘要来源
		type?: string; // 可选摘要类型
		title?: string; // 可选摘要标题
	};
}

export interface NewsItem {
	date?: string; // 可选日期
	summary?: {
		title?: string; // 可选摘要标题
		source?: string; // 可选摘要来源
		type?: typeof eventTypes; // 可选摘要类型
		keywords?: string; // 可选摘要关键词
	};
	abstract?: string; // 可选摘要内容
}

interface DashboardState {
	ddlData: DdlEvent[];
	Messages: NewsItem[];
	historyMessages: NewsItem[];
	isLoading: boolean;
	error: string | null;
}

// Dashboard Store
export const useDashboardStore = defineStore("dashboard", {
	// State
	state: (): DashboardState => ({
		ddlData: [],
		Messages: [],
		historyMessages: [],
		isLoading: false,
		error: null,
	}),

	// Actions
	actions: {
		// 通用数据获取
		async fetchData<T>(url: string): Promise<T> {
			try {
				this.isLoading = true;
				this.error = null;

				const response = await fetch(url, {
					credentials: 'include'
				});
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
		async fetchDdlData(date: DateString) {
			try {
				const response = await this.fetchData<ApiResponse>(
					api_router.dateQuery(date),
				);

				if (response.code === 200 && response.data.ddl_events) {
					this.ddlData = response.data.ddl_events.map((event: DdlEvent) => {
						return {
							summary: {
								time: event.summary?.time,
								source: event.summary?.source,
								type: event.summary?.type,
								title: event.summary?.title,
							},
						};
					});
				}
			} catch (error) {
				console.error("Failed to fetch DDL data:", error);
			}
		},

		// 获取消息
		async fetchMessages(date: DateString) {
			try {
				const response = await this.fetchData<ApiResponse>(
					api_router.dateQuery(date),
				);

				if (response.code === 200 && response.data.news) {
					this.Messages = response.data.news.map((item: NewsItem) => {
						return {
				date: item.date,
				summary: {
					title: item.summary?.title,
					source: item.summary?.source,
					type: item.summary?.type || [],
					keywords: item.summary?.keywords,
				},
				abstract: item.abstract,
							};
						});
					}
			} catch (error) {
				console.error(`Failed to fetch messages for date ${date}:`, error);
			}
		},

		// 初始化所有数据
		async initialize() {
			this.isLoading = true;
			try {
				await Promise.all([
					this.fetchDdlData(dayjs().format("YYYY-MM-DD") as DateString),
					this.fetchMessages(dayjs().format("YYYY-MM-DD") as DateString),
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
		Messages: store.Messages,
		refreshData: store.refreshAllData,
	};
}
