import dayjs from "dayjs";

// 创建 DateString 类型和相关函数
// -----------------------------
/**
 * 表示 YYYY-MM-DD 格式的日期字符串
 * 使用 branded type 技术创建类型安全的字符串
 */
export type DateString = string & { __dateString: true };

/**
 * 验证字符串是否为有效的日期格式 (YYYY-MM-DD)
 */
function isValidDateFormat(date: string): boolean {
  return /^\d{4}-\d{2}-\d{2}$/.test(date) && dayjs(date).isValid();
}

/**
 * 将字符串转换为类型安全的 DateString
 * @throws {Error} 如果日期格式无效
 */
function asDateString(date: string): DateString {
  if (!isValidDateFormat(date)) {
    throw new Error(`Invalid date format: ${date}. Expected YYYY-MM-DD`);
  }
  return date as DateString;
}

/**
 * 安全创建 DateString，如果无效则返回今天的日期
 */
export function toDateString(date?: string): DateString {
  if (!date) return asDateString(dayjs().format("YYYY-MM-DD"));
  
  try {
    return asDateString(date);
  } catch (e) {
    console.warn(`Invalid date: ${date}, using today's date instead`);
    return asDateString(dayjs().format("YYYY-MM-DD"));
  }
}
