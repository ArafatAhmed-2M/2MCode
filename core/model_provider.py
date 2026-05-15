from __future__ import annotations

import os
from typing import Optional, AsyncGenerator, Any

import litellm
from litellm import completion, acompletion

from rich.prompt import Prompt, IntPrompt
from rich.text import Text

from core.config import (
    AppConfig,
    ModelConfig,
    load_config,
    save_config,
    update_model_config,
    get_api_key,
)
from core.ui import console, make_panel, status_spinner, print_header

PROVIDERS = {
    "anthropic": {
        "label": "Anthropic (Claude)",
        "models": [
            "claude-sonnet-4-20250514",
            "claude-3-5-sonnet-20241022",
            "claude-3-opus-20240229",
            "claude-3-haiku-20240307",
        ],
        "default": "claude-sonnet-4-20250514",
        "env_key": "ANTHROPIC_API_KEY",
    },
    "openai": {
        "label": "OpenAI (GPT-4o / o-series)",
        "models": [
            "gpt-4o",
            "gpt-4o-mini",
            "gpt-4-turbo",
            "o1",
            "o3-mini",
        ],
        "default": "gpt-4o",
        "env_key": "OPENAI_API_KEY",
    },
    "google": {
        "label": "Google (Gemini)",
        "models": [
            "gemini/gemini-2.0-flash-exp",
            "gemini/gemini-1.5-pro",
            "gemini/gemini-1.5-flash",
        ],
        "default": "gemini/gemini-2.0-flash-exp",
        "env_key": "GEMINI_API_KEY",
    },
    "groq": {
        "label": "Groq (Fast Open-Source)",
        "models": [
            "groq/llama3-70b-8192",
            "groq/llama3-8b-8192",
            "groq/mixtral-8x7b-32768",
        ],
        "default": "groq/llama3-70b-8192",
        "env_key": "GROQ_API_KEY",
    },
    "openrouter": {
        "label": "OpenRouter (Multi-Model Gateway)",
        "models": [
            "openrouter/anthropic/claude-sonnet-4-20250514",
            "openrouter/openai/gpt-4o",
            "openrouter/google/gemini-2.0-flash-exp",
            "openrouter/meta-llama/llama-3.3-70b-instruct",
            "openrouter/deepseek/deepseek-chat",
        ],
        "default": "openrouter/anthropic/claude-sonnet-4-20250514",
        "env_key": "OPENROUTER_API_KEY",
        "api_base": "https://openrouter.ai/api/v1",
    },
    "deepseek": {
        "label": "DeepSeek",
        "models": [
            "deepseek/deepseek-chat",
            "deepseek/deepseek-reasoner",
        ],
        "default": "deepseek/deepseek-chat",
        "env_key": "DEEPSEEK_API_KEY",
    },
    "together": {
        "label": "Together AI",
        "models": [
            "together_ai/meta-llama/Llama-3.3-70B-Instruct-Turbo",
            "together_ai/mistralai/Mixtral-8x22B-Instruct-v0.1",
            "together_ai/deepseek-ai/deepseek-chat",
            "together_ai/Qwen/Qwen2.5-Coder-32B-Instruct",
        ],
        "default": "together_ai/meta-llama/Llama-3.3-70B-Instruct-Turbo",
        "env_key": "TOGETHER_API_KEY",
    },
    "mistral": {
        "label": "Mistral AI",
        "models": [
            "mistral/mistral-large-latest",
            "mistral/mistral-medium-latest",
            "mistral/mistral-small-latest",
            "mistral/codestral-latest",
        ],
        "default": "mistral/mistral-large-latest",
        "env_key": "MISTRAL_API_KEY",
    },
}


def run_setup_wizard(show_header: bool = True) -> AppConfig:
    if show_header:
        print_header()

    provider_choices = [
        ("anthropic", PROVIDERS["anthropic"]["label"]),
        ("openai", PROVIDERS["openai"]["label"]),
        ("google", PROVIDERS["google"]["label"]),
        ("groq", PROVIDERS["groq"]["label"]),
        ("openrouter", PROVIDERS["openrouter"]["label"]),
        ("deepseek", PROVIDERS["deepseek"]["label"]),
        ("together", PROVIDERS["together"]["label"]),
        ("mistral", PROVIDERS["mistral"]["label"]),
        ("custom", "Custom Endpoint (Local / Open Source / Ollama / vLLM / HuggingFace)"),
    ]

    console.print(make_panel(
        "[bold white]Choose your AI model provider:[/bold white]",
        title="2M Code — Model Provider Selection",
        border_style="cyan",
    ))
    console.print()
    for idx, (_, label) in enumerate(provider_choices, 1):
        console.print(f"  [bold cyan]{idx}.[/bold cyan] [white]{label}[/white]")
    console.print()
    choice = IntPrompt.ask("[bold white]Enter your choice", default=1)

    if choice < 1 or choice > len(provider_choices):
        console.print("[red]Invalid choice.[/red]")
        raise SystemExit(1)

    provider = provider_choices[choice - 1][0]
    api_key = ""
    api_base = None
    model_name = ""

    if provider == "custom":
        # ---- Custom provider flow - completely isolated from standard env mapping ----
        env_key_name = Prompt.ask(
            "[bold white]API Name/Env Key to use[/bold white]",
            default="NVIDIA_API_KEY",
        )
        api_key = Prompt.ask(
            "[bold white]Enter your API key (leave blank if not required)[/bold white]",
            default="",
        )
        api_base = Prompt.ask(
            "[bold white]Custom API Base URL[/bold white]",
            default="http://localhost:11434/v1",
        )
        if not api_base:
            console.print("[red]API base URL is required for custom endpoints.[/red]")
            raise SystemExit(1)
        model_name = Prompt.ask(
            "[bold white]Model name (e.g. ollama/qwen2.5-coder, open-mixtral-8x7b)[/bold white]",
            default="ollama/qwen2.5-coder",
        )
        if not model_name:
            console.print("[red]Model name is required.[/red]")
            raise SystemExit(1)

        if api_key:
            os.environ[env_key_name] = api_key
            os.environ["CUSTOM_API_KEY"] = api_key
    else:
        # ---- Standard provider flow - safe to access PROVIDERS dict ----
        info = PROVIDERS[provider]

        api_key = Prompt.ask(
            f"[bold white]Paste your {info['label']} API key[/bold white]",
            default="",
        )
        if not api_key:
            console.print("[yellow]No API key provided. Check .env file or configure later.[/yellow]")

        console.print()
        console.print("[bold white]Choose which model to use:[/bold white]")
        for idx, m in enumerate(info["models"], 1):
            console.print(f"  [bold cyan]{idx}.[/bold cyan] [white]{m}[/white]")
        console.print()
        model_choice = IntPrompt.ask("[bold white]Enter your choice", default=1)
        if 1 <= model_choice <= len(info["models"]):
            model_name = info["models"][model_choice - 1]
        else:
            model_name = info["default"]

        if api_key:
            os.environ[info["env_key"]] = api_key

    cfg = load_config()
    cfg.model.provider = provider
    cfg.model.model_name = model_name
    cfg.model.api_key = api_key
    cfg.model.api_base = api_base
    save_config(cfg)

    console.print()
    panel_text = Text()
    panel_text.append(f"Provider : ", style="cyan")
    panel_text.append(f"{provider}\n", style="bold white")
    panel_text.append(f"Model    : ", style="cyan")
    panel_text.append(f"{model_name}\n", style="bold white")
    if api_base:
        panel_text.append(f"Endpoint : ", style="cyan")
        panel_text.append(f"{api_base}\n", style="bold white")
    console.print(make_panel(panel_text, title="[bold green]Configuration Complete", border_style="green"))

    return cfg


def list_available_models() -> dict:
    return {k: v["models"] for k, v in PROVIDERS.items()}


def get_litellm_kwargs(cfg: Optional[AppConfig] = None) -> dict:
    if cfg is None:
        cfg = load_config()
    mc = cfg.model
    kwargs: dict = {
        "model": mc.model_name,
        "temperature": mc.temperature,
        "max_tokens": mc.max_tokens,
    }
    key = mc.api_key or get_api_key(mc.provider)
    if key:
        kwargs["api_key"] = key
    if mc.api_base:
        kwargs["api_base"] = mc.api_base
    return kwargs


def send_message(
    messages: list[dict],
    cfg: Optional[AppConfig] = None,
    stream: bool = True,
) -> str | AsyncGenerator[str, None]:
    if cfg is None:
        cfg = load_config()
    kwargs = get_litellm_kwargs(cfg)
    kwargs["messages"] = messages
    kwargs["stream"] = stream

    try:
        if stream:
            return _stream_completion(kwargs)
        response = completion(**kwargs)
        return response.choices[0].message.content or ""
    except Exception as e:
        console.print(f"[red]API Error:[/red] {e}")
        raise


async def _stream_completion(kwargs: dict) -> AsyncGenerator[str, None]:
    response = await acompletion(**kwargs)
    async for chunk in response:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content


def send_message_sync(messages: list[dict], cfg: Optional[AppConfig] = None) -> str:
    if cfg is None:
        cfg = load_config()
    kwargs = get_litellm_kwargs(cfg)
    kwargs["messages"] = messages
    kwargs["stream"] = False

    try:
        response = completion(**kwargs)
        return response.choices[0].message.content or ""
    except Exception as e:
        console.print(f"[red]API Error:[/red] {e}")
        raise
