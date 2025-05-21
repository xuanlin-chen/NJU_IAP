import { ref } from 'vue'

export interface SummaryData {
  totalUsers: number;
  activeUsers: number;
  completionRate: number;
  coursesCount: number;
}

export interface Course {
  rank: number;
  name: string;
  platform: string;
  students: number;
  satisfaction: number;
}

export interface DdlItem {
  title: string;
  date: string;
  group: number; // 0: 今天, 1: 昨天, 2: 更早
}

export interface PlatformData {
  name: string;
  percentage: number;
  color: string;
}

export interface TodayMessage {
  title: string;
  time: string;
  source: string;
}

export interface HistoryMessage {
  title: string;
  date: string;
  views: number;
}

// 初始数据
const summaryData = ref<SummaryData>({
  totalUsers: 3458,
  activeUsers: 2187,
  completionRate: 78.6,
  coursesCount: 124
})

const tableData = ref<Course[]>([
  {
    rank: 1,
    name: '人工智能导论',
    platform: '五大学堂',
    students: 1520,
    satisfaction: 96
  },
  {
    rank: 2,
    name: '大数据分析与应用',
    platform: '慕课',
    students: 1356,
    satisfaction: 94
  },
  {
    rank: 3,
    name: '计算机网络基础',
    platform: '学习通',
    students: 1245,
    satisfaction: 92
  },
  {
    rank: 4,
    name: '高级Java编程',
    platform: '五大学堂',
    students: 1120,
    satisfaction: 91
  },
  {
    rank: 5,
    name: 'Python数据分析',
    platform: '慕课',
    students: 986,
    satisfaction: 90
  }
])

const ddlData = ref<DdlItem[]>([
  { title: '提交人工智能课程作业', date: '2025-05-07', group: 0 },
  { title: '大数据分析项目报告截止', date: '2025-05-07', group: 0 },
  { title: '计算机网络实验报告提交', date: '2025-05-06', group: 1 },
  { title: '高级Java编程期末考试', date: '2025-05-05', group: 2 },
  { title: 'Python数据分析课程论文', date: '2025-05-01', group: 2 }
]);

let a = fetch('http://localhost:5000/api/ddl-events')
// 此处暂时需要使用http协议

console.log(a)

ddlData.value.push(
  { title: '提交人工智能课程作业', date: '2025-05-07', group: 0 },)

const platformData = ref<PlatformData[]>([
  { name: '五大学堂', percentage: 38, color: '#2080f0' },
  { name: '慕课', percentage: 32, color: '#18a058' },
  { name: '学习通', percentage: 24, color: '#d03050' },
  { name: '其他平台', percentage: 6, color: '#f0a020' },
])

// 添加今日消息数据
const todayMessages = ref<TodayMessage[]>([
  { title: '系统通知：第三学期选课系统已开放', time: '10:30', source: '教务系统' },
  { title: '南大举行2025年春季招聘会', time: '09:15', source: '就业中心' },
  { title: '今日下午14:00有学术讲座', time: '08:45', source: '学术办公室' },
  { title: '图书馆新增电子资源订阅', time: '08:00', source: '图书馆' }
])

// 添加历史消息数据
const historyMessages = ref<HistoryMessage[]>([
  { title: '计算机科学学院组织学生参观华为研发中心', date: '2025-05-03', views: 876 },
  { title: '南大学生在国际程序设计大赛中获得金奖', date: '2025-05-02', views: 1240 },
  { title: '2025年度奖学金评定工作开始', date: '2025-04-30', views: 982 },
  { title: '新学期教材领取通知', date: '2025-04-28', views: 1562 }
])

// 刷新数据的方法
export function refreshData() {
  // 在真实应用中，这里会调用后端API
  return new Promise<void>((resolve) => {
    setTimeout(() => {
      // 更新数据
      summaryData.value = {
        totalUsers: Math.floor(3000 + Math.random() * 1000),
        activeUsers: Math.floor(2000 + Math.random() * 500),
        completionRate: 75 + Math.random() * 10,
        coursesCount: 120 + Math.floor(Math.random() * 10)
      }
      
      // 更新表格数据（随机变化学习人数）
      tableData.value = tableData.value.map(item => ({
        ...item,
        students: item.students + Math.floor(Math.random() * 20) - 10
      })).sort((a, b) => b.students - a.students)
        .map((item, index) => ({...item, rank: index + 1}))
      
      // 更新今日消息（随机调整时间）
      todayMessages.value = todayMessages.value.map(message => {
        const hour = Math.floor(8 + Math.random() * 10);
        const minute = Math.floor(Math.random() * 60);
        return {
          ...message,
          time: `${hour.toString().padStart(2, '0')}:${minute.toString().padStart(2, '0')}`
        };
      });
      
      // 更新历史消息（随机调整浏览量）
      historyMessages.value = historyMessages.value.map(message => ({
        ...message,
        views: message.views + Math.floor(Math.random() * 100) - 30
      }));
      
      resolve()
    }, 1500)
  })
}

// 导出响应式数据
export function useDashboardData() {
  return {
    summaryData,
    tableData,
    ddlData,
    platformData,
    todayMessages,
    historyMessages,
    refreshData
  }
}