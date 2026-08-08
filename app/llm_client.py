# 接收一篇笔记 + 生成模式 -> 返回一份结构化的python字典
from openai import OpenAI,APIError
from openai.types.chat import ChatCompletionMessageParam
import json
from app.config import get_config

def generate(note: dict, mode: str) -> dict:
    if mode == "flashcards":
        return {
            "cards": [
                {
                    "question":"问题1",
                    "answer": "回答1",
                    "tag": "标签1",
                }
            ]
        }
    elif mode == "outline":
        return {
            "outline": [
                "第一个复习要点",
                "第二个复习要点",
                "第三个复习要点",
            ]
        }
    else:
        raise ValueError(f"不支持的模式{mode}")


def generate_real(note: dict, mode: str) -> dict:
    """调用真实 DeepSeek API,把笔记变成结构化问答卡/提纲"""
    if mode not in ("flashcards", "outline"):
        raise ValueError(f"不支持的模式{mode}")

    # 第一步：拿配置（密钥、服务器地址、模型名）
    cfg = get_config()

    # 第二步：建立连接 —— 带上密钥，找到 DeepSeek 服务器的大门
    client = OpenAI(
        api_key=cfg["api_key"],
        base_url=cfg["base_url"],
        timeout=30,
    )

    # 第三步：写"系统规则"——告诉模型你的身份、必须输出什么格式
    if mode == "flashcards":
        format_rule = '{"cards": [{"question": "问题", "answer": "答案", "tag": "知识点标签"}]}'
    else:
        format_rule = '{"outline": ["要点1", "要点2", "要点3"]}'

    system_prompt = (
        "你是学习助手，根据用户提供的笔记生成复习材料。\n"
        "只输出 JSON,不要输出任何其他文字,不要用 markdown 代码块。\n"
        "必须严格使用以下格式：\n" + format_rule
    )

    # 第四步：打包"对话记录"——一张纸条写规则，一张纸条写笔记
    messages: list[ChatCompletionMessageParam] = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": (
            f"课程：{note.get('course', '')}\n"
            f"标题：{note.get('title', '')}\n"
            f"笔记内容：\n{note['content']}"
        )},
    ]

    # 第五步：把纸条递过去，等服务器回复
    try:
        resp = client.chat.completions.create(
            model=cfg["model"],
            messages=messages,
        )
    except APIError as error:
        raise ValueError(f"调用大模型失败:{error}") from error

    # 第六步：从回复里抠出文本（模型说的话）
    text = resp.choices[0].message.content
    if text is None:
        raise ValueError("模型没有返回任何文本内容")

    # 第七步：把文本解析成 Python 字典，并检查形状对不对
    data = json.loads(text)
    expected = "cards" if mode == "flashcards" else "outline"
    if expected not in data:
        raise ValueError(f"模型返回的 JSON 里没有 {expected} 字段：{text[:200]}")

    return data
