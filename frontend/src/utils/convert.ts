import _ from 'lodash';

const keyMap = {
  '类型': 'type',
  '标题': 'title',
  '截止时间': 'time',
  '原文链接': 'source',
  '关键词': 'keywords',
} as const;

// biome-ignore lint/suspicious/noExplicitAny: this is a common convention in JS
export function convertKey(obj: any): any {
  if (!obj || typeof obj !== 'object') {
    return obj;
  }

  if (Array.isArray(obj)) {
    return _.map(obj, convertKey);
  }

  // biome-ignore lint/suspicious/noExplicitAny: common pattern
  return _.reduce(obj, (result: Record<string, any>, value, key) => {
    // 将中文键名转换为英文键名
    const newKey = keyMap[key as keyof typeof keyMap] || key;
    
    // 递归处理嵌套对象
    result[newKey] = _.isObject(value) && !_.isNull(value) 
      ? convertKey(value) 
      : value;
    return result;
  }, {});
}