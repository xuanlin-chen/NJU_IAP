# AI服务，用于OpenAI交互
import json
import openai
from ..settings import OPENAI_API_KEY

# 配置OpenAI API密钥
openai.api_key = OPENAI_API_KEY

def extract_tags_with_ai(question) -> list:
    """使用AI提取查询标签"""
    prompt = f"请从以下问题中提取关键词和实体，以JSON数组格式返回，每个元素应包含'key'和'value'字段，例如[{{'key':'type', 'value':'会议通知'}}]：{question}"
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    try:
        # 解析AI返回的JSON
        content = response.choices[0].message.content
        if not content:
            return []
        extracted_tags = json.loads(content)
        
        # 验证格式
        validated_tags = []
        for tag in extracted_tags:
            if isinstance(tag, dict) and 'key' in tag and 'value' in tag:
                validated_tags.append(tag)
            elif isinstance(tag, str):
                # 兼容旧格式，将字符串转换为键值格式
                validated_tags.append({'key': 'keyword', 'value': tag})
        
        return validated_tags
    except:
        return []

def generate_answer_with_ai(question, results) -> str|None:
    """使用AI生成最终答案"""
    # 格式化结果数据供AI理解
    formatted_results = []
    for res in results:
        # 提取标签和内容
        tags = res.get('tags', {})
        content = res.get('content', {})
        message_type = res.get('message_type', '未知类型')
        
        # 格式化时间信息
        time_info = ""
        if 'time' in tags and isinstance(tags['time'], dict):
            time = tags['time']
            if all(k in time for k in ['year', 'month', 'day']):
                time_info = f"{time.get('year', 0)}-{time.get('month', 0):02d}-{time.get('day', 0):02d}"
        
        # 构建格式化结果
        formatted_result = {
            'id': res.get('id'),
            'type': message_type,
            'time': time_info,
            'tags': {k: v for k, v in tags.items() if k != 'time'},  # 排除时间字段，已单独处理
            'content': content
        }
        formatted_results.append(formatted_result)
    
    # 将格式化结果转换为JSON字符串
    context = json.dumps(formatted_results, ensure_ascii=False, indent=2)
    
    # 构建提示语
    prompt = f"根据以下数据回答问题：{question}\n\n数据：\n{context}\n\n请提供详细、准确的回答，并引用相关信息来源。"
    
    # 调用AI生成答案
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content