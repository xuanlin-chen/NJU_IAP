# AI services for OpenAI interaction
import json
import openai
from ..config.settings import OPENAI_API_KEY

# Configure OpenAI API key
openai.api_key = OPENAI_API_KEY

def extract_tags_with_ai(question):
    """Use AI to extract query tags"""
    prompt = f"请从以下问题中提取关键词和实体，以JSON数组格式返回，每个元素应包含'key'和'value'字段，例如[{{'key':'type', 'value':'会议通知'}}]：{question}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    try:
        # Parse AI returned JSON
        extracted_tags = json.loads(response.choices[0].message['content'])
        
        # Validate format
        validated_tags = []
        for tag in extracted_tags:
            if isinstance(tag, dict) and 'key' in tag and 'value' in tag:
                validated_tags.append(tag)
            elif isinstance(tag, str):
                # Compatible with old format, convert string to key-value format
                validated_tags.append({'key': 'keyword', 'value': tag})
        
        return validated_tags
    except:
        return []

def generate_answer_with_ai(question, results):
    """Use AI to generate final answer"""
    # Format result data for AI to understand
    formatted_results = []
    for res in results:
        # Extract tags and content
        tags = res.get('tags', {})
        content = res.get('content', {})
        message_type = res.get('message_type', 'Unknown type')
        
        # Format time information
        time_info = ""
        if 'time' in tags and isinstance(tags['time'], dict):
            time = tags['time']
            if all(k in time for k in ['year', 'month', 'day']):
                time_info = f"{time.get('year', 0)}-{time.get('month', 0):02d}-{time.get('day', 0):02d}"
        
        # Build formatted result
        formatted_result = {
            'id': res.get('id'),
            'type': message_type,
            'time': time_info,
            'tags': {k: v for k, v in tags.items() if k != 'time'},  # Exclude time field, already processed
            'content': content
        }
        formatted_results.append(formatted_result)
    
    # Convert formatted results to JSON string
    context = json.dumps(formatted_results, ensure_ascii=False, indent=2)
    
    # Build prompt
    prompt = f"根据以下数据回答问题：{question}\n\n数据：\n{context}\n\n请提供详细、准确的回答，并引用相关信息来源。"
    
    # Call AI to generate answer
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message['content']