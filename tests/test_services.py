import pytest

from app import llm_client
from app import repositories as repo
from app import services


@pytest.fixture()
def sample_note(tmp_db):
    return repo.add_note("数据结构", "链表", "链表节点通过指针连接。")


def test_generate_for_note_missing(tmp_db):
    assert services.generate_for_note(999999, "flashcards") is None


def test_generate_for_note_fake(tmp_db, sample_note, monkeypatch):
    monkeypatch.setattr(services, "get_config", lambda: {"provider": "fake"})

    generation = services.generate_for_note(sample_note, "flashcards")
    assert generation is not None
    assert generation["note_id"] == sample_note
    assert generation["mode"] == "flashcards"
    assert generation["result"]["cards"][0]["question"] == "问题1"

    records = repo.list_generations(sample_note)
    assert len(records) == 1


def test_generate_for_note_real(tmp_db, sample_note, monkeypatch):
    monkeypatch.setattr(services, "get_config", lambda: {"provider": "real"})
    fake_result = {"cards": [{"question": "q", "answer": "a", "tag": "t"}]}
    monkeypatch.setattr(llm_client, "generate_real", lambda note, mode: fake_result)

    generation = services.generate_for_note(sample_note, "flashcards")
    assert generation is not None
    assert generation["result"] == fake_result


def test_generate_for_note_unsupported_mode(tmp_db, sample_note, monkeypatch):
    monkeypatch.setattr(services, "get_config", lambda: {"provider": "fake"})

    with pytest.raises(ValueError, match="不支持的模式"):
        services.generate_for_note(sample_note, "essay")
