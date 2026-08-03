from html import escape

from fastapi import FastAPI,Form,HTTPException
from fastapi.responses import HTMLResponse
from app.note_validation import validate_note
import app.repositories as repo
from app.database import init_db

app=FastAPI()

init_db()

@app.get("/")
def home():
    html_content = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>AI 问答卡助手</title>
</head>
<body>
    <h1>AI 问答卡助手</h1>
    <p>欢迎使用。这个页面由Python的FastAPI提供。</p>
<form action="/api/notes" method="post">
    <input name="course" placeholder="课程（可选，例如：数据结构）">
    <input name="title" placeholder="标题（可选）">
    <textarea name="content" placeholder="在此输入笔记内容"></textarea>
    <button type="submit">提交笔记</button>
</form>
</body>
</html>"""
    return HTMLResponse(html_content)

@app.post("/api/notes")
def create_note(course:str = Form(default = ""), title:str = Form(default=""),content: str = Form()):
    cleaned_content= validate_note(content)
    if not cleaned_content:
        return HTMLResponse("<p>错误：笔记不能为空。</p>", status_code=400)
    cleaned_course = course.strip()
    cleaned_title = title.strip()
    note_id = repo.add_note(cleaned_course, cleaned_title, cleaned_content)
    display_course = escape(cleaned_course or '(未分类)')
    display_title = escape(cleaned_title or '(无标题)')
    display_content = escape(cleaned_content)
    return HTMLResponse(
        f"<h1>笔记已提交</h1>"
        f"<p>编号：{note_id}</p>"
        f"<h2>{display_course}</h2>"
        f"<h3>{display_title}</h3>"
        f"<p>{display_content}</p>"
        f'<a href="/">返回首页</a>'
    )

@app.get("/api/notes")
def view_notes():
    notes = repo.list_notes()
    if not notes:
        return HTMLResponse("<p>尚无笔记。</p>")
    html_parts = ["<h1>笔记列表</h1>"]
    for note in notes:
        display_course = escape(note['course'] or '(未分类)')
        display_title = escape(note['title'] or '(无标题)')
        display_content = escape(note['content'])
        html_parts.append(
            f"<div>"
            f"<h2>{display_course}</h2>"
            f"<h3>{display_title}</h3>"
            f"<p>{display_content}</p>"
            f"<small>{escape(note['created_at'])}</small>"
            f"</div><hr>"
        )
    html_parts.append('<a href="/">返回首页</a>')
    return HTMLResponse("".join(html_parts))

@app.get("/api/notes/{note_id}")
def view_note(note_id : int):
    note = repo.get_note(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="笔记不存在")

    html_parts = ["<h1>找到的笔记</h1>"]
    display_course = escape(note['course'] or '(未分类)')
    display_title = escape(note['title'] or '(无标题)')
    display_content = escape(note['content'])
    html_parts.append(
                f"<div>"
                f"<h2>{display_course}</h2>"
                f"<h3>{display_title}</h3>"
                f"<p>{display_content}</p>"
                f"<small>{escape(note['created_at'])}</small>"
                f"</div><hr>"
            )
    html_parts.append('<a href="/">返回首页</a>')
    return HTMLResponse("".join(html_parts))