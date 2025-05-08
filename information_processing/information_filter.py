# 这段代码用于筛选信息
import os
import requests

# 配置参数
API_KEY = "sk-***********************************************"
API_URL = "https://api.siliconflow.cn/v1/chat/completions" # 我用的硅基流动的deepseek api, 阿里云比赛应选用通义AI
MARKDOWN_PATH = "./files" # 文件夹地址，假设文件夹里文件是markdown格式的


def analyze_article(content):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    # 提示词
    prompt = f"""你是一个高校信息过滤助手，你需要完成的任务是判断文章含有信息对本科生是否有用。请按照以下步骤进行判断：
1. 内容分析：提取关键要素（核心内容/时间/对象）
2. 有用性判断：
  ○ 学业影响（课程通知、考试安排、选课信息等）
  ○ 生活必需（宿舍调整、校园活动、安全提醒等）
  ○ 发展机会（竞赛通知、实习机会、学术讲座等）
3. 学生参与度判断（若有且对象为本科生，直接判断为“有用”）：
  ○ 需要学生采取具体行动
  ○ 影响学业进度或生活安排
  ○ 涉及资格/机会的获取条件
4. 需排除的内容（直接判断为“无用”）：
  ○ 纯工作部署类会议报道
  ○ 未落地的规划方案讨论
  ○ 无具体实施路径的政策宣导
  ○ 无本科生参与机制的教研活动
5. 思考判断：若将文章判断为“无用”，请再次谨慎思考是否真的“无用”，以保证不遗漏信息
6. 最终结论：仅输出“有用”或者“无用”
重要提醒：
除输出“有用”或者“无用”外不要输出其他任何文字

文章内容如下：
{content}"""

    payload = {
        "model": "deepseek-ai/DeepSeek-V3",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1,
        "max_tokens": 10
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()['choices'][0]['message']['content'].strip()
        return result.lower() == "有用"
    except Exception as e:
        print(f"API调用失败: {str(e)}")
        return True  # 失败时默认视为有用


def process_files():
    # 处理文章
    for filename in os.listdir(MARKDOWN_PATH):
        if filename.endswith(".md"):
            filepath = os.path.join(MARKDOWN_PATH, filename)

            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                if analyze_article(content):
                    print("1")
                    # 进一步处理 分类，结构化，存储等等

            except Exception as e:
                print(f"处理文件 {filename} 时出错: {str(e)}")


if __name__ == "__main__":
    process_files()
