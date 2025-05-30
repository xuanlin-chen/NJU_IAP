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
	date?: string; // 可能是 "YYYY-MM-DD" 格式
	summary?: {
		截止时间?: string; // 如 "2025-05-27"
		标题?: string; // 如 "天池"
		类型?: string; // 如 "用户自定义"
		原文链接?: string; // 原文链接
	};
	// 保留原来的字段以保持向后兼容
	title?: string;
	deadline?: string;
	source?: string;
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
	type: string; // 如 "用户自定义"
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
				// 硬编码的DDL数据
				const hardcodedDdlEvents: Record<string, DdlEvent[]> = {
					"2025-05-19": [
						{
							date: "2025-05-19",
							summary: {
								原文链接: "https://jw.nju.edu.cn/",
								截止时间: "2025-05-21 23:59:00",
								标题: "南京大学期中考试安排",
								类型: "学业安排"
							}
						},
						{
							date: "2025-05-19",
							summary: {
								原文链接: "https://www.nju.edu.cn/",
								截止时间: "2025-05-19 17:30:00",
								标题: "教育部交流生项目申请截止",
								类型: "学业申请"
							}
						}
					],
					"2025-05-20": [
						{
							date: "2025-05-20",
							summary: {
								原文链接: "https://jw.nju.edu.cn/a0/85/c26263a761989/page.htm",
								截止时间: "2025-06-22 23:59:00",
								标题: "仙林校区通宵自习教室开放通知",
								类型: "校园通知"
							}
						},
						{
							date: "2025-05-20",
							summary: {
								原文链接: "http://mp.weixin.qq.com/s?__biz=MzAxODAzMjQ1NQ==&mid=2707705645&idx=1&sn=71e92d5423e7eb0e5553caf642e71a2b&chksm=bf4c9d05883b1413e026efe94ae10936bcd14b66a2d9ef6722612f4159cfcb1223c91ee0eb3f#rd",
								截止时间: "2025-05-22 11:00:00",
								标题: "南京大学123周年校庆及互动福利活动",
								类型: "校园通知"
							}
						},
						{
							date: "2025-05-20",
							summary: {
								原文链接: "http://mp.weixin.qq.com/s?__biz=MzI4MTY1MjkyOA==&mid=2247489127&idx=1&sn=c536df734027b065ea4acf5d1c50d9d6&chksm=eba4adc8dcd324de9844e4cc4e4c70edc78417b366867e3861e2b65b8a7099387a65be709f3e#rd",
								截止时间: "2025-05-22 23:59:00",
								标题: "第五十二场新生午餐会特别策划：教授请吃饭第二季",
								类型: "校园通知"
							}
						},
						{
							date: "2025-05-20",
							summary: {
								原文链接: "http://mp.weixin.qq.com/s?__biz=MzA3NzczMTI5MA==&mid=2650896194&idx=1&sn=533b8db3e075c3d17872dee63a65d1f4&chksm=84b853f7b3cfdae10927d33cbe35a5829afb5cf7e66f0fa3192c26ceafb4903b33fa57b5c688#rd",
								截止时间: "2025-05-22 12:00:00",
								标题: "南京大学台港澳青年端午访学活动",
								类型: "社会实践"
							}
						},
						{
							date: "2025-05-21",
							summary: {
								原文链接: "http://mp.weixin.qq.com/s?__biz=Mzg5MTU0NDIzOQ==&mid=2247501687&idx=1&sn=14a2505424170f3beb6533dbbd312e71&chksm=cfc930b7f8beb9a1f1a1256f748d7e25e1e19bb9a2f5db20b4ab034332a163b3ce010c659efd#rd",
								截止时间: "2025-05-28 23:59:00",
								标题: "南京大学毓琇书院团学联主席团换届竞选通知",
								类型: "学业申请"
							}
						},
						{
							date: "2025-05-21",
							summary: {
								原文链接: "http://mp.weixin.qq.com/s?__biz=MzI4MTY1MjkyOA==&mid=2247489137&idx=1&sn=6987757e9da0a6fa3a267de88cd213ad&chksm=eba4addedcd324c89d8d1a13a5ff35dbafdb0a3474021bf66cd7c6b520357669f3b473cbbdeb#rd",
								截止时间: "2025-05-22 12:30:00",
								标题: "高研院新生午餐会：我们为什么要重视信息健康",
								类型: "讲座或分享会信息"
							}
						},
						{
							date: "2025-05-21",
							summary: {
								原文链接: "http://mp.weixin.qq.com/s?__biz=MzkwNDE4ODYyMg==&mid=2247497549&idx=1&sn=9fd6fe0fd7c92818903aa8d6136a27c8&chksm=c08870ecf7fff9fa380101c90b7560b7d1dc2fc2a2aea760f8199d802057301cee3b0447818f#rd",
								截止时间: "2025-05-22 13:30:00",
								标题: "南京大学第三届新生戏剧节第二、三场展演",
								类型: "文体活动"
							}
						},
						{
							date: "2025-05-22",
							summary: {
								原文链接: "http://mp.weixin.qq.com/s?__biz=MzkwNDE4ODYyMg==&mid=2247497604&idx=2&sn=cdd00eeecbb848d717e07d7a6cb8d355&chksm=c0887025f7fff933582e9848728ac758236a0f964ce862bf33ba0602215e3a3215b2e6893516#rd",
								截止时间: "2025-05-21 20:20:00",
								标题: "南京大学123周年校庆教授请吃饭活动",
								类型: "文体活动"
							}
						},
						{
							date: "2025-05-23",
							summary: {
								原文链接: "http://mp.weixin.qq.com/s?__biz=MjM5NTE5Mjk1Mg==&mid=2650159900&idx=1&sn=4fcb0f804b96fed58e360c4074dca2af&chksm=befed20b89895b1dadc726d89ea7998dff22483beb2b1928b0b9ae43537b9f78c4eb38275fbe#rd",
								截止时间: "2025-05-24 12:00:00",
								标题: "仙林图书馆停电维修通知",
								类型: "校园通知"
							}
						},
						{
							date: "2025-05-23",
							summary: {
								原文链接: "http://mp.weixin.qq.com/s?__biz=Mzk0MDE5MTk3Mw==&mid=2247507085&idx=2&sn=6f90a2eb226c46e837f00f58dff12b23&chksm=c2e7e507f5906c111271b5adc3cdfead67369f279725d21ce323c0c9dc0f12637891f42f0da4#rd",
								截止时间: "2025-05-24 23:59:00",
								标题: "全国大学生数学建模竞赛经验分享",
								类型: "讲座或分享会信息"
							}
						},
						{
							date: "2025-05-23",
							summary: {
								原文链接: "http://mp.weixin.qq.com/s?__biz=MzkwODQwMDEzNg==&mid=2247494932&idx=1&sn=7c65529dcf1aff6c2098130039b102a9&chksm=c0c82e73f7bfa76587cacce640459c24b7269d9e195444bf85b19c3f58276698ce797bdeabff#rd",
								截止时间: "2025-05-28 23:59:00",
								标题: "健雄书院第五期文明宿舍评选",
								类型: "文体活动"
							}
						},
						{
							date: "2025-05-24",
							summary: {
								原文链接: "http://mp.weixin.qq.com/s?__biz=MzkwNDE4ODYyMg==&mid=2247497709&idx=1&sn=6d2648cd0b9aaebc075460b7008dc289&chksm=c088704cf7fff95a1cfa7ef0f0297f3712827b02bad13c3c7ce8c896f373ce415899697da25a#rd",
								截止时间: "2025-05-24 17:20:00",
								标题: "南京大学敦煌文化新生主题式通识科考与科研训练",
								类型: "讲座或分享会信息"
							}
						},
						{
							date: "2025-05-24",
							summary: {
								原文链接: "http://mp.weixin.qq.com/s?__biz=MzkzMTE5MDM1MA==&mid=2247520203&idx=2&sn=635800c85c97d7ca61ad1e71e571a0f5&chksm=c26c0ceaf51b85fc4d7e94829c1ed4ebb50a979e6fcd46f1a8ccd53be3d10d0b371213954345#rd",
								截止时间: "2025-05-25 09:00:00",
								标题: "2025年春季学期新生午餐读书会第七场旁听报名",
								类型: "讲座或分享会信息"
							}
						},
						{
							date: "2025-05-25",
							summary: {
								原文链接: "http://mp.weixin.qq.com/s?__biz=Mzk0MDE5MTk3Mw==&mid=2247507119&idx=1&sn=4c1be72753184c3611e7d78fa62aac22&chksm=c2e7e525f5906c33e3946f1c6697f47c94e0ef55278783d0a0f955e7e36c41a203dcc688d9f5#rd",
								截止时间: "2025-05-28 22:00:00",
								标题: "南京大学有训书院2025-2026学年团学班宿主席团、部长团换届竞选通知",
								类型: "学业申请"
							}
						}
					]
				};

				// 检查是否有硬编码数据
				if (date && hardcodedDdlEvents[date as string]) {
					console.log(`Using hardcoded DDL events for date ${date}`);
					this.ddlData = hardcodedDdlEvents[date as string].map((item: DdlEvent) => {
						// 处理URL，确保有效性
						let sourceUrl: URL | string;
						try {
							// 从summary获取原文链接
							const sourceStr = item.summary?.原文链接 || "";
							sourceUrl = sourceStr ? new URL(sourceStr) : "";
						} catch (e) {
							sourceUrl = item.summary?.原文链接 || "";
							console.warn(`Invalid URL in DDL: ${item.summary?.原文链接}`);
						}

						// 处理日期和时间
						const deadline = dayjs(item.summary?.截止时间 || "");

						return {
							title: item.summary?.标题 || "",
							date: deadline,
							time: deadline,
							source: sourceUrl,
							type: item.summary?.类型 || ""
						};
					});
				} else {
					// 如果没有硬编码数据，则使用API数据
					const response = await this.fetchData<ApiResponse>(
						api_router.dateQuery(date),
					);

					if (response.code === 200) {
						console.log(`Fetched ddl for date ${date}:`, response.data);
						this.Messages = response.data.news.map((item:NewsItem) => {
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
				}
			} catch (error) {
				console.error(`Failed to fetch messages for date ${date}:`, error);
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
				// 获取当前日期，如果当前日期为5月19日或5月20日，则使用硬编码数据
				// 否则使用当前日期
				const today = dayjs().format("YYYY-MM-DD");
				const testDate = (today === "2025-05-19" || today === "2025-05-20") 
					? today 
					: (dayjs("2025-05-19").format("YYYY-MM-DD")); // 测试用，使用5月19日的数据
				
				await Promise.all([
					this.fetchDdlData(testDate as DateString),
					this.fetchMessages(testDate as DateString),
				]);
				
				console.log("Dashboard initialized with data for date:", testDate);
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
