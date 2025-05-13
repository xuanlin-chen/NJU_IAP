import os
import re

def clean_filename(filename):
    """清理文件名，移除特殊字符"""
    # 替换特殊字符为下划线
    filename = re.sub(r'[\\/:*?"<>|]', '_', filename)
    # 替换空格为下划线
    filename = filename.replace(' ', '_')
    return filename

def split_prompts():
    # 读取原始prompt文件
    with open('prompt_information_structing.txt', 'r', encoding='utf-8') as f:
        content = f.read()

    # 创建prompts目录
    os.makedirs('prompts', exist_ok=True)

    # 使用正则表达式分割不同类型的prompt
    pattern = r'(\d+)\.\s+([^：]+)：([^j]+)json模版：\s*({[^}]+})'
    matches = re.finditer(pattern, content)

    for match in matches:
        number = match.group(1)
        type_name = match.group(2).strip()
        description = match.group(3).strip()
        json_template = match.group(4).strip()

        # 创建prompt文件
        prompt_content = f"""你是一个文章信息处理助手，现在需要处理{type_name}类型的文章。

文章类型说明：{description}

json模版：
{json_template}

你的处理步骤：
1. 首先，明确判断你获得的文章是否属于{type_name}类型。
2. 然后，严格按照json模版中所列的各个键的定义，仔细处理文章内容，提取相关信息并进行填充。
3. 最后，确保生成并输出一个完整、准确且格式正确的填充完毕的json文件。

处理规定：
1. 对于标签"标题"，如果原标题太长可提炼标题关键信息。
2. 对于所有标签，如果原文章信息有缺失，则填"无"。
3. 一些标签有多个键值时，以数组形式填入。比如参赛资格可能有本科生，大一年级两个元素，则填入：["本科生", "大一年级"]。
4. 不要把原始文章存入标签"原文信息"中，“原文信息”保留空就可以。
5. 总结全文的关键词，填入标签"关键词"中。
6. 文章链接会附在文末，请把它填入标签"原文链接"中。
7. 五育认定类型分为"德育""智育""体育""美育""劳育"，会在文中明确提到。如"活动录入"敦行成绩单"【劳育】项目"。

输出规定：
只输出处理好的json文件，除此之外不要输出任何文本

请处理如下文章：
{{article}}
"""

        # 清理文件名并保存prompt文件
        clean_type_name = clean_filename(type_name)
        with open(f'prompts/{clean_type_name}.txt', 'w', encoding='utf-8') as f:
            f.write(prompt_content)

if __name__ == "__main__":
    split_prompts() 