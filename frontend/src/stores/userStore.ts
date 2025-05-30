import { defineStore } from "pinia";
import { ref } from "vue";

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

export const useUserStore = defineStore('user', () => {
  const user = ref<User | null>(null);
  const isLoggedIn = ref(false);
  const loading = ref(false);
  const error = ref<string | null>(null);

  // 登录方法
  const login = async (username: string, password: string) => {
    loading.value = true;
    error.value = null;
    
    try {
      const response = await fetch('/api/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      });
      
      const result: ApiResponse = await response.json();
      
      if (!response.ok) {
        throw new Error(result.message || '登录失败');
      }
      
      // 保存用户信息
      user.value = result.data;
      isLoggedIn.value = true;
      
      return { success: true };
    } catch (e) {
      error.value = e instanceof Error ? e.message : '登录失败，请稍后重试';
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
      const response = await fetch('/api/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      });
      
      const result: ApiResponse = await response.json();
      
      if (!response.ok) {
        throw new Error(result.message || '注册失败');
      }
      
      // 保存用户信息
      user.value = result.data;
      isLoggedIn.value = true;
      
      return { success: true };
    } catch (e) {
      error.value = e instanceof Error ? e.message : '注册失败，请稍后重试';
      return { success: false, error: error.value };
    } finally {
      loading.value = false;
    }
  };
  
  // 登出方法
  const logout = () => {
    user.value = null;
    isLoggedIn.value = false;
  };

  // 添加自定义DDL
  const addCustomDdl = async (content: string) => {
    if (!user.value?.id) {
      error.value = '请先登录';
      return { success: false, error: '请先登录' };
    }

    loading.value = true;
    error.value = null;
    
    try {
      const response = await fetch('/api/custom-ddl', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ content }),
      });
      
      const result: ApiResponse = await response.json();
      
      if (!response.ok) {
        throw new Error(result.message || '添加自定义DDL失败');
      }
      
      // 更新用户信息
      user.value = result.data;
      
      return { success: true };
    } catch (e) {
      error.value = e instanceof Error ? e.message : '添加自定义DDL失败，请稍后重试';
      return { success: false, error: error.value };
    } finally {
      loading.value = false;
    }
  };
  
  // 删除自定义DDL
  const removeCustomDdl = async (index: number) => {
    if (!user.value?.id) {
      error.value = '请先登录';
      return { success: false, error: '请先登录' };
    }

    loading.value = true;
    error.value = null;
    
    try {
      const response = await fetch(`/api/custom-ddl/${index}`, {
        method: 'DELETE',
      });
      
      const result: ApiResponse = await response.json();
      
      if (!response.ok) {
        throw new Error(result.message || '删除自定义DDL失败');
      }
      
      // 更新用户信息
      user.value = result.data;
      
      return { success: true };
    } catch (e) {
      error.value = e instanceof Error ? e.message : '删除自定义DDL失败，请稍后重试';
      return { success: false, error: error.value };
    } finally {
      loading.value = false;
    }
  };
  
  // 更新未订阅公众号列表
  const updateUnsubscribedAccounts = async (accounts: string[]) => {
    if (!user.value?.id) {
      error.value = '请先登录';
      return { success: false, error: '请先登录' };
    }

    loading.value = true;
    error.value = null;
    
    try {
      const response = await fetch('/api/unsubscribed-accounts', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ accounts }),
      });
      
      const result: ApiResponse = await response.json();
      
      if (!response.ok) {
        throw new Error(result.message || '更新未订阅公众号列表失败');
      }
      
      // 更新用户信息
      user.value = result.data;
      
      return { success: true };
    } catch (e) {
      error.value = e instanceof Error ? e.message : '更新未订阅公众号列表失败，请稍后重试';
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
    updateUnsubscribedAccounts
  };
});

