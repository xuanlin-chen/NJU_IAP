export type ValidUrl = string & { readonly __brand: unique symbol };

/**
 * 验证并创建安全的URL类型
 * @param url 要验证的URL字符串
 * @returns 验证后的URL或抛出错误
 */
export function createValidUrl(url: string): ValidUrl {
  try {
    // 使用URL构造函数进行验证
    new URL(url)
    return url as ValidUrl
  } catch (error) {
    throw new Error(`Invalid URL: ${url}`)
  }
}

/**
 * 类型守卫：检查字符串是否为有效URL
 */
export function isValidUrl(url: string): url is ValidUrl {
  try {
    new URL(url)
    return true
  } catch {
    return false
  }
}