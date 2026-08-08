import json

import httpx
import pytest
from openai import APIError

from app import llm_client

# ---------- 可控的假 OpenAI client ----------


class FakeMessage:
    def __init__(self, content):
        self.content = content


class FakeChoice:
    def __init__(self, content):
        self.message = FakeMessage(content)


class FakeResponse:
    def __init__(self, content):
        self.choices = [FakeChoice(content)]


class FakeCompletions:
    def __init__(self, result):
        self.result = result  # str | None | Exception

    def create(self, **kwargs):
        if isinstance(self.result, Exception):
            raise self.result
        return FakeResponse(self.result)


class FakeChat:
    def __init__(self, result):
        self.completions = FakeCompletions(result)


class FakeOpenAI:
    def __init__(self, result=None, **kwargs):
        self._result = result

    def set_result(self, result):
        self._result = result

    @property
    def chat(self):
        return FakeChat(self._result)


@pytest.fixture()
def fake_client(monkeypatch):
    """替换 OpenAI client 与配置，全程离线、不花钱"""
    fake = FakeOpenAI()
    monkeypatch.setattr(llm_client, "OpenAI", lambda **kwargs: fake)
    monkeypatch.setattr(
        llm_client,
        "get_config",
        lambda: {"api_key": "x", "base_url": "http://x", "model": "m"},
    )
    return fake


NOTE = {"course": "数据结构", "title": "链表", "content": "链表通过指针连接。"}

# ---------- 假 LLM ----------


def test_generate_fake_flashcards():
    result = llm_client.generate(NOTE, "flashcards")
    assert result["cards"][0]["question"] == "问题1"


def test_generate_fake_outline():
    result = llm_client.generate(NOTE, "outline")
    assert len(result["outline"]) == 3


def test_generate_fake_unsupported_mode():
    with pytest.raises(ValueError, match="不支持的模式"):
        llm_client.generate(NOTE, "essay")


# ---------- 真实 client（假连接） ----------


def test_generate_real_happy(fake_client):
    fake_client.set_result(json.dumps({"cards": [{"question": "q", "answer": "a", "tag": "t"}]}))
    result = llm_client.generate_real(NOTE, "flashcards")
    assert result["cards"][0]["question"] == "q"


def test_generate_real_outline_happy(fake_client):
    fake_client.set_result(json.dumps({"outline": ["a", "b"]}))
    result = llm_client.generate_real(NOTE, "outline")
    assert result["outline"] == ["a", "b"]


def test_generate_real_none_content(fake_client):
    fake_client.set_result(None)
    with pytest.raises(ValueError, match="没有返回任何文本"):
        llm_client.generate_real(NOTE, "flashcards")


def test_generate_real_bad_json(fake_client):
    fake_client.set_result("抱歉，我不能帮你生成。")
    with pytest.raises(json.JSONDecodeError):
        llm_client.generate_real(NOTE, "flashcards")


def test_generate_real_missing_key(fake_client):
    fake_client.set_result(json.dumps({"foo": 1}))
    with pytest.raises(ValueError, match="cards"):
        llm_client.generate_real(NOTE, "flashcards")


def test_generate_real_api_error_translated(fake_client):
    fake_client.set_result(
        APIError("模拟网络故障", request=httpx.Request("POST", "http://x"), body=None)
    )
    with pytest.raises(ValueError, match="调用大模型失败"):
        llm_client.generate_real(NOTE, "flashcards")


def test_generate_real_unsupported_mode(fake_client):
    with pytest.raises(ValueError, match="不支持的模式"):
        llm_client.generate_real(NOTE, "essay")
