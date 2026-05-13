import json
import os
from pathlib import Path
from typing import Optional, Literal
from pydantic import BaseModel, Field
from platformdirs import user_config_dir

APP_NAME = "2mcode"
CONFIG_DIR = Path(user_config_dir(APP_NAME, ensure_exists=True))
CONFIG_FILE = CONFIG_DIR / "config.json"


class ModelConfig(BaseModel):
    provider: Literal["anthropic", "openai", "google", "groq", "custom"] = "anthropic"
    model_name: str = "claude-sonnet-4-20250514"
    api_key: str = ""
    api_base: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 8192
    max_retries: int = 3


class UIConfig(BaseModel):
    theme: Literal["blue-white", "dark"] = "blue-white"
    stream: bool = True
    animation_speed: Literal["fast", "normal", "relaxed"] = "normal"


class AppConfig(BaseModel):
    model: ModelConfig = Field(default_factory=ModelConfig)
    ui: UIConfig = Field(default_factory=UIConfig)
    active_skills: list[str] = Field(default_factory=lambda: ["skill-creator"])
    max_active_skills: int = 3
    workspace_dir: str = ""


def load_config() -> AppConfig:
    if CONFIG_FILE.exists():
        data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        return AppConfig(**data)
    cfg = AppConfig()
    save_config(cfg)
    return cfg


def save_config(cfg: AppConfig) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(cfg.model_dump_json(indent=2), encoding="utf-8")


def update_model_config(**kwargs) -> AppConfig:
    cfg = load_config()
    for key, val in kwargs.items():
        if hasattr(cfg.model, key):
            setattr(cfg.model, key, val)
    save_config(cfg)
    return cfg


def get_api_key(provider: str) -> str:
    env_map = {
        "anthropic": "ANTHROPIC_API_KEY",
        "openai": "OPENAI_API_KEY",
        "google": "GEMINI_API_KEY",
        "groq": "GROQ_API_KEY",
        "custom": "CUSTOM_API_KEY",
    }
    env_var = env_map.get(provider, "")
    return os.environ.get(env_var, "")
