import _ from 'lodash';

const keyMap = {
  '类型': 'type',
  '标题': 'title',
  '截止时间': 'time',
  '原文链接': 'source',
  '关键词': 'keywords',
} as const;

const typeMap = {
  '比赛通知': 'competition',
  '学习资源': 'study',
  '校园资源': 'campus',
  '学业申请': 'academic',
  '学业相关政策': 'academicPolicy',
  '奖励、资助政策': 'rewardPolicy',
  '惩罚制度': 'punishmentPolicy',
  '校园安全': 'campusSafety',
  '讲座或分享会信息': 'lecture',
  '志愿活动': 'volunteer',
  '社会实践': 'socialPractice',
  '国际交流项目': 'internationalExchange',
  '社团消息': 'club',
  '问题活动': 'problematicActivity',
  '实践培训活动': 'trainingActivity',
  '作品征集': 'workCollection',
  '其他活动': 'otherActivity',
  '实习就业': 'internshipEmployment',
  '其他类型': 'otherType',
} as const;

const combinedMap = {...keyMap, ...typeMap} as const;
type Key = keyof typeof combinedMap;

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
    const newKey = key in combinedMap ? combinedMap[key as Key] : key;    
    // 递归处理嵌套对象
    result[newKey] = _.isObject(value) && !_.isNull(value) 
      ? convertKey(value) 
      : value;
    return result;
  }, {});
}