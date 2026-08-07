# 接收一篇笔记 + 生成模式 -> 返回一份结构化的python字典

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