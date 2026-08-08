import pytest

from app.config import get_config


def test_get_config_ok(monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "sk-test")
    monkeypatch.setenv("DEEPSEEK_BASE_URL", "https://example.com/v1")
    monkeypatch.setenv("DEEPSEEK_MODEL", "test-model")
    monkeypatch.setenv("LLM_PROVIDER", "real")

    cfg = get_config()
    assert cfg["api_key"] == "sk-test"
    assert cfg["base_url"] == "https://example.com/v1"
    assert cfg["model"] == "test-model"
    assert cfg["provider"] == "real"


def test_get_config_provider_defaults_to_fake(monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "sk-test")
    monkeypatch.setenv("DEEPSEEK_BASE_URL", "https://example.com/v1")
    monkeypatch.delenv("LLM_PROVIDER", raising=False)

    assert get_config()["provider"] == "fake"


def test_get_config_missing_api_key(monkeypatch):
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)
    monkeypatch.setenv("DEEPSEEK_BASE_URL", "https://example.com/v1")

    with pytest.raises(RuntimeError, match="DEEPSEEK_API_KEY"):
        get_config()


def test_get_config_missing_base_url(monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "sk-test")
    monkeypatch.delenv("DEEPSEEK_BASE_URL", raising=False)

    with pytest.raises(RuntimeError, match="DEEPSEEK_BASE_URL"):
        get_config()


def test_get_config_invalid_provider(monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "sk-test")
    monkeypatch.setenv("DEEPSEEK_BASE_URL", "https://example.com/v1")
    monkeypatch.setenv("LLM_PROVIDER", "reel")

    with pytest.raises(RuntimeError, match="fake 或 real"):
        get_config()
