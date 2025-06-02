import { defineStore } from "pinia";
import { ref } from "vue";
import type { DdlEvent } from "./dashboardStore";

const api_router = {
	login: () => "/api/login",
	register: () => "/api/register",
	customDdl: () => "/api/custom-ddl",
	unsubscribedAccounts: () => "/api/unsubscribed-accounts",
	removeCustomDdl: (index: number) => `/api/custom-ddl/${index}`,
};

// 用户接口定义
interface User {
	id: number;
	username: string;
	custom_ddls?: string[];
	unsubscribed_accounts?: string[];
}

// API响应接口
interface ApiResponse {
	code: number;
	// biome-ignore lint/suspicious/noExplicitAny: <explanation>
	data: any;
	message: string;
	errors?: string;
}

export const useUserStore = defineStore("user", () => {
	const user = ref<User | null>(null);
	const isLoggedIn = ref(false);
	const loading = ref(false);
	const error = ref<string | null>(null);

	// 登录方法
	const login = async (username: string, password: string) => {
		loading.value = true;
		error.value = null;

		try {
			const response = await fetch(api_router.login(), {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				credentials: 'include',
				body: JSON.stringify({ username, password }),
			});

			const result: ApiResponse = await response.json();

			// 检查API响应中的状态码，而不仅仅是HTTP状态码
			if (response.ok && result.code === 200) {
				// 登录成功，保存用户信息
				user.value = result.data;
				isLoggedIn.value = true;

				return { success: true, message: result.message || "登录成功" };
			}
			// 登录失败，设置错误信息
			throw new Error(result.message || "登录失败");
		} catch (e) {
			error.value = e instanceof Error ? e.message : "登录失败，请稍后重试";
			return { success: false, error: error.value };
		} finally {
			loading.value = false;
		}
	};

	// 注册方法
	const register = async (username: string, password: string) => {
		loading.value = true;
		error.value = null;

		try {
			const response = await fetch(api_router.register(), {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				credentials: 'include',
				body: JSON.stringify({ username, password }),
			});

			const result: ApiResponse = await response.json();

			// 检查API响应中的状态码，而不仅仅是HTTP状态码
			if (response.ok && result.code === 200) {
				// 注册成功，保存用户信息
				user.value = result.data;
				isLoggedIn.value = true;

				return { success: true, message: result.message || "注册成功" };
			}
			// 注册失败，设置错误信息
			throw new Error(result.message || "注册失败");
		} catch (e) {
			error.value = e instanceof Error ? e.message : "注册失败，请稍后重试";
			return { success: false, error: error.value };
		} finally {
			loading.value = false;
		}
	};

	// 登出方法
	const logout = async () => {
		try {
			const response = await fetch('/api/logout', {
				method: 'POST',
				credentials: 'include'
			});
			
			// 无论后端响应如何，都清除前端状态
			user.value = null;
			isLoggedIn.value = false;
			
			if (!response.ok) {
				throw new Error('登出失败');
			}
		} catch (e) {
			console.error('登出失败:', e);
			// 即使发生错误，也确保清除前端状态
			user.value = null;
			isLoggedIn.value = false;
		}
	};

	// 添加自定义DDL
	const addCustomDdl = async (content: DdlEvent) => {
		if (!user.value?.id) {
			error.value = "请先登录";
			return { success: false, error: "请先登录" };
		}

		loading.value = true;
		error.value = null;

		try {
			const response = await fetch(api_router.customDdl(), {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				credentials: 'include',
				body: JSON.stringify({
					content: content.summary.title,
					date: content.summary.time?.format("YYYY-MM-DD HH:mm:ss"),
				}),
			});

			const result: ApiResponse = await response.json();

			if (result.code === 200) {
				// 添加成功，更新用户信息
				user.value = result.data;

				return {
					success: true,
					message: result.message || "添加自定义DDL成功",
				};
			}
			// 添加失败
			throw new Error(result.message || "添加自定义DDL失败");
		} catch (e) {
			error.value =
				e instanceof Error ? e.message : "添加自定义DDL失败，请稍后重试";
			return { success: false, error: error.value };
		} finally {
			loading.value = false;
		}
	};

	// 删除自定义DDL
	const removeCustomDdl = async (index: number) => {
		if (!user.value?.id) {
			error.value = "请先登录";
			return { success: false, error: "请先登录" };
		}

		loading.value = true;
		error.value = null;

		try {
			const response = await fetch(api_router.removeCustomDdl(index), {
				method: "DELETE",
				credentials: 'include',
			});

			const result: ApiResponse = await response.json();

			if (result.code === 200) {
				// 删除成功，更新用户信息
				user.value = result.data;

				return {
					success: true,
					message: result.message || "删除自定义DDL成功",
				};
			}
			// 删除失败
			throw new Error(result.message || "删除自定义DDL失败");
		} catch (e) {
			error.value =
				e instanceof Error ? e.message : "删除自定义DDL失败，请稍后重试";
			return { success: false, error: error.value };
		} finally {
			loading.value = false;
		}
	};

	// 更新未订阅公众号列表
	const updateUnsubscribedAccounts = async (accounts: string[]) => {
		if (!user.value?.id) {
			error.value = "请先登录";
			return { success: false, error: "请先登录" };
		}

		loading.value = true;
		error.value = null;

		try {
			const response = await fetch(api_router.unsubscribedAccounts(), {
				method: "PUT",
				headers: {
					"Content-Type": "application/json",
				},
				credentials: 'include',
				body: JSON.stringify({ accounts }),
			});

			const result: ApiResponse = await response.json();

			// 检查API响应中的状态码，而不仅仅是HTTP状态码
			if (response.ok && result.code === 200) {
				// 更新成功，更新用户信息
				user.value = result.data;

				return {
					success: true,
					message: result.message || "更新未订阅公众号列表成功",
				};
			}
			// 更新失败
			throw new Error(result.message || "更新未订阅公众号列表失败");
		} catch (e) {
			error.value =
				e instanceof Error ? e.message : "更新未订阅公众号列表失败，请稍后重试";
			return { success: false, error: error.value };
		} finally {
			loading.value = false;
		}
	};

	return {
		user,
		isLoggedIn,
		loading,
		error,
		login,
		register,
		logout,
		addCustomDdl,
		removeCustomDdl,
		updateUnsubscribedAccounts,
	};
});
