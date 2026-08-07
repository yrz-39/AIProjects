from dotenv import load_dotenv
import os

load_dotenv()  # 把 .env 里的变量加载进 os.environ

def get_config() -> dict:
    api_key = os.environ.get("DEEPSEEK_API_KEY", "")
    base_url = os.environ.get("DEEPSEEK_BASE_URL", "")
    model = os.environ.get("DEEPSEEK_MODEL", "")
    provider = os.environ.get("LLM_PROVIDER", "fake")

    if not api_key:
        raise RuntimeError("缺少 DEEPSEEK_API_KEY,请在项目根目录的 .env 中配置")

    if not base_url:
        raise RuntimeError("缺少 DEEPSEEK_BASE_URL,请在 .env 中配置中转站地址")

    return {
        "api_key": api_key,
        "base_url": base_url,
        "model": model or "deepseek-v4-flash",  # 模型名可以给默认值
        "provider": provider,
    }