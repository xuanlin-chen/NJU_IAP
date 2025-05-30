import { defineStore } from "pinia";
import { convertKey } from "@/utils/convert";
import type { DateString } from "@/utils/DateString";
import dayjs from "dayjs";

type Dayjs = dayjs.Dayjs;

const api_router = {
	dateQuery: (date: DateString) => `/api/date-query?date=${date}`,
};

// API response interfaces
interface ApiResponse {
	code: number;
	data: ApiData;
	message: string;
}

interface ApiData {
	date: string;
	ddl_events: DdlEvent[];
	news: NewsItem[];
}

interface DdlEvent {
	title: string;
	deadline: string; // 格式预计为 "YYYY-MM-DD HH:MM"
	source?: string; // 可能为空，需要处理
}

interface NewsItem {
	title?: string;
	time?: string;
	date?: string;
	source?: string;
	abstract?: string;
	type?: string;
	summary?: {
		keywords?: string;
		source?: string;
		title?: string;
		type?: string;
	};
}

// Output interfaces for the store
export interface DdlItem {
	title: string;
	date: Dayjs; // 格式: "YYYY-MM-DD"
	time: Dayjs; // 格式: "HH:MM" 24小时制
	source: URL | string;
}

export interface Message {
	title: string;
	time: string;
	source: URL | string;
	abstract: string;
	type: string;
}

// State interface
interface DashboardState {
	ddlData: DdlItem[];
	Messages: Message[];
	historyMessages: Message[];
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
		async fetchDdlData(date: DateString) {
			try {
				const response = await this.fetchData<ApiResponse>(
					api_router.dateQuery(date),
				);

				if (response.code === 200 && response.data.ddl_events) {
					this.ddlData = response.data.ddl_events.map((event: DdlEvent) => {
						const dateTime = dayjs(event.deadline);
						// 处理URL，确保有效性
						let sourceUrl: URL | string = "";
						try {
							// 确保source不是undefined
							const sourceStr = event.source || "";
							sourceUrl = sourceStr ? new URL(sourceStr) : "";
						} catch (e) {
							sourceUrl = event.source || "";
							console.warn(`Invalid URL in DDL: ${event.source}`);
						}

						return {
							title: event.title,
							date: dateTime, // 提取日期部分
							time: dateTime, // 提取时间部分
							source: sourceUrl,
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

				if (response.code === 200) {
					console.log(`Fetched messages for date ${date}:`, response.data.news);
					this.Messages = response.data.news.map((item: NewsItem) => {
						// 处理URL，确保有效性
						let sourceUrl: URL | string;
						try {
							// 尝试从summary获取source，如果没有则使用直接的source
							const sourceStr = item.summary?.source || item.source || "";
							sourceUrl = sourceStr ? new URL(sourceStr) : "";
						} catch (e) {
							sourceUrl = item.summary?.source || item.source || "";
							console.warn(
								`Invalid URL in Message: ${item.summary?.source || item.source}`,
							);
						}

						return {
							// 从summary获取标题，如果没有则使用直接的标题
							title: item.summary?.title || item.title || "",
							// 使用时间信息，提供备选
							time: item.time || item.date || "",
							source: sourceUrl,
							abstract: item.abstract || "",
							// 从summary获取类型，如果没有则使用直接的类型
							type: item.summary?.type || item.type || "news",
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
