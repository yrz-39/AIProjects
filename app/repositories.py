from app.database import get_connection

def add_note(course:str, title:str,content:str)->int | None:
    """保存一篇笔记,返回ID"""
    conn = get_connection()
    cursor = conn.execute(
        "INSERT INTO notes (course, title, content) VALUES (?, ?, ?)",
        (course, title, content)
    )# 注意参数化查询规则 学一下SQL注入攻击
    conn.commit()
    note_id = cursor.lastrowid
    conn.close()
    return note_id

def list_notes()->list[dict]:
    """返回所有笔记的列表"""
    conn = get_connection()
    rows = conn.execute(
        "SELECT id, course, title, content, created_at FROM notes ORDER BY id DESC"
    ).fetchall()
    conn.close()
    # 把row对象转换为字典 与前面conn.row_factory = sqlite3.Row联系起来
    return [dict(row) for row in rows]

def get_note(note_id : int) -> dict | None:
    conn = get_connection()
    row = conn.execute(
        "SELECT id, course, title, content, created_at FROM notes WHERE id = ?",
        (note_id,),
    ).fetchone()
    conn.close()
    if not row:
        return None
    return dict(row)
