import sqlite3
from pathlib import Path

# 数据库文件路径
DB_PATH = str(Path(__file__).resolve().parent.parent / "data" / "app.db")

def get_connection():
    # conn是一个连接对象，对数据库的操作都通过它
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS notes(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course TEXT DEFAULT '',
            title TEXT DEFAULT '',
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    columns = conn.execute("PRAGMA table_info(notes)").fetchall()
    column_names = [column[1] for column in columns]
    if "course" not in column_names:
        conn.execute("ALTER TABLE notes ADD COLUMN course TEXT DEFAULT ''")
    # 确认保存 将改动写入磁盘
    conn.commit()
    # 释放连接资源
    conn.close()
