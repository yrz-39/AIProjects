from app.database import get_connection
import json

def add_note(course:str, title:str,content:str)->int | None:
    """保存一篇笔记,返回ID"""
    conn = get_connection()
    try:
        cursor = conn.execute(
            "INSERT INTO notes (course, title, content) VALUES (?, ?, ?)",
            (course, title, content)
        )# 注意参数化查询规则 学一下SQL注入攻击
        conn.commit()
        return cursor.lastrowid
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def list_notes()->list[dict]:
    """返回所有笔记的列表"""
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT id, course, title, content, created_at FROM notes ORDER BY id DESC"
        ).fetchall()
        # 把row对象转换为字典 与前面conn.row_factory = sqlite3.Row联系起来
        return [dict(row) for row in rows]
    finally:
        conn.close()

def get_note(note_id : int) -> dict | None:
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT id, course, title, content, created_at FROM notes WHERE id = ?",
            (note_id,),
        ).fetchone()
        if not row:
            return None
        return dict(row)
    finally:
        conn.close()


def add_generation(note_id: int, mode: str, result:dict) -> int |None:
    content_json = json.dumps(result, ensure_ascii=False)
    conn = get_connection()
    try:
        cursor = conn.execute(
            "INSERT INTO generations (note_id, mode, content_json) VALUES (?, ?, ?)",
            (note_id, mode, content_json)
        )
        conn.commit()
        return cursor.lastrowid
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def list_generations(note_id: int) -> list[dict]:
    conn = get_connection()
    try:
        rows = conn.execute("SELECT id, note_id, mode, content_json, created_at FROM generations WHERE note_id = ? ORDER BY id DESC",
                    (note_id,),
        ).fetchall()
        generations = []
        for row in rows:
            generation = dict(row)
            content_json = generation.pop("content_json")
            generation["result"] = json.loads(content_json)
            generations.append(generation)
        return generations
    finally:
        conn.close()
