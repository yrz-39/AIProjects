import pytest

from app import database


@pytest.fixture()
def tmp_db(tmp_path, monkeypatch):
    """把 SQLite 指向临时文件，隔离正式数据库，测试结束自动清理"""
    db_file = tmp_path / "test.db"
    monkeypatch.setattr(database, "DB_PATH", str(db_file))
    database.init_db()
    return str(db_file)
