# 这段代码用于筛选信息
import os
import requests
import json

# 配置参数
API_KEY = "sk-***********************************************"
API_URL = "https://api.siliconflow.cn/v1/chat/completions" # 我用的硅基流动的deepseek api, 阿里云比赛应选用通义AI

ARTICLE_TYPES = [
    "比赛通知", "学习资源", "校园通知", "学业申请", "学业相关政策",
    "奖励_资助政策", "惩罚制度", "校园安全", "讲座_分享会信息",
    "志愿活动", "国际交流项目", "社团消息", "文体活动",
    "实践培训活动", "作品征集", "其他活动", "实习就业", "其他类型"
]

def load_prompt(type_name):
    """加载对应类型的prompt文件"""

    prompt_path = os.path.join("prompts", f"{type_name}.txt")
    try:
        with open(prompt_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"未找到类型 {type_name} 的prompt文件")
        return None

def analyze_and_classify_article(content):
    """分析文章是否有用，如果有用则返回其类型"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""你是一个高校信息过滤助手，你需要完成的任务是判断文章含有信息对本科生是否有用。请按照以下步骤进行判断：
1. 内容分析：提取关键要素（核心内容/时间/对象）
2. 有用性判断：
  ○ 学业影响（课程通知、考试安排、选课信息等）
  ○ 生活必需（宿舍调整、校园活动、安全提醒等）
  ○ 发展机会（竞赛通知、实习机会、学术讲座等）
3. 学生参与度判断（若有且对象为本科生，直接判断为"有用"）：
  ○ 需要学生采取具体行动
  ○ 影响学业进度或生活安排
  ○ 涉及资格/机会的获取条件
4. 需排除的内容（直接判断为"无用"）：
  ○ 纯工作部署类会议报道
  ○ 未落地的规划方案讨论
  ○ 无具体实施路径的政策宣导
  ○ 无本科生参与机制的教研活动
5. 思考判断：若将文章判断为"无用"，请再次谨慎思考是否真的"无用"，以保证不遗漏信息
6. 最终结论：如果为有用，就将其分为以下18类中的一类：
{', '.join(ARTICLE_TYPES)}

重要提醒：如果有用，你输出的只能是这18类中的一类名字，不要输出任何其他内容，主要只要类型名字；如果无用，则什么都不输出

文章内容如下：
{content}"""

    payload = {
        "model": "deepseek-ai/DeepSeek-V3",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1,
        "max_tokens": 50
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()['choices'][0]['message']['content'].strip()
        
        # 如果返回空字符串，说明文章无用
        if not result:
            return None
            
        # 检查返回的类型是否在预定义类型中
        if result in ARTICLE_TYPES:
            return result
        else:
            print(f"返回的类型不在预定义范围内: {result}")
            return None
            
    except Exception as e:
        print(f"API调用失败: {str(e)}")
        return None

def structure_article(content, article_type):
    """将文章内容结构化"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = load_prompt(article_type)
    if not prompt:
        return None

    prompt = prompt.replace("{article}", content)

    payload = {
        "model": "deepseek-ai/DeepSeek-V3",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1,
        "max_tokens": 2000
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()['choices'][0]['message']['content'].strip()
        return json.loads(result)
    except Exception as e:
        print(f"结构化API调用失败: {str(e)}")
        return None

def process_single_article(content):
    """处理单篇文章内容"""
    try:
        # 1. 分析文章是否有用并获取类型
        article_type = analyze_and_classify_article(content)
        if not article_type:
            print("文章被判定为无用")
            return None

        # 2. 根据类型进行结构化
        structured_data = structure_article(content, article_type)
        if not structured_data:
            print(f"文章结构化失败")
            return None

        return structured_data

    except Exception as e:
        print(f"处理文章时出错: {str(e)}")
        return None

