from __future__ import annotations

import os
from typing import Optional, AsyncGenerator, Any

import litellm
from litellm import completion, acompletion
from prompt_toolkit.shortcuts import radiolist_dialog, input_dialog, message_dialog

from core.config import (
    AppConfig,
    ModelConfig,
    load_config,
    save_config,
    update_model_config,
    get_api_key,
)
from core.ui import console, make_panel, status_spinner, print_header
from rich.text import Text

PROVIDERS = {
    "anthropic": {
        "label": "Anthropic (Claude 3.5 Sonnet)",
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
        "label": "OpenAI (GPT-4o)",
        "models": [
            "gpt-4o",
            "gpt-4o-mini",
            "gpt-4-turbo",
            "o1",
        ],
        "default": "gpt-4o",
        "env_key": "OPENAI_API_KEY",
    },
    "google": {
        "label": "Google (Gemini Pro)",
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
}


def run_setup_wizard() -> AppConfig:
    print_header()

    provider_choices = [
        ("anthropic", PROVIDERS["anthropic"]["label"]),
        ("openai", PROVIDERS["openai"]["label"]),
        ("google", PROVIDERS["google"]["label"]),
        ("groq", PROVIDERS["groq"]["label"]),
        ("custom", "Custom Endpoint (Local / Open Source / Ollama / vLLM / HuggingFace)"),
    ]

    result = radiolist_dialog(
        title="2M Code — Model Provider Selection",
        text="Choose your AI model provider:",
        values=provider_choices,
    ).run()

    if result is None:
        console.print("[yellow]Setup cancelled.[/yellow]")
        raise SystemExit(0)

    provider = result
    info = PROVIDERS.get(provider)
    api_key = ""
    api_base = None
    model_name = ""

    if provider == "custom":
        api_base = input_dialog(
            title="Custom Endpoint",
            text="Enter your API base URL:\n(e.g. http://localhost:11434/v1 or https://your-endpoint.com/v1)",
        ).run()
        if not api_base:
            console.print("[red]API base URL is required for custom endpoints.[/red]")
            raise SystemExit(1)
        api_key = input_dialog(
            title="Custom API Key",
            text="Enter your API key (leave blank if not required):",
        ).run() or ""
        model_name = input_dialog(
            title="Custom Model Name",
            text="Enter the model name:\n(e.g. ollama/qwen2.5-coder, openmixtral, etc.)",
        ).run()
        if not model_name:
            console.print("[red]Model name is required.[/red]")
            raise SystemExit(1)
        message_dialog(
            title="Custom Provider Configured",
            text=f"Base URL: {api_base}\nModel: {model_name}\n\nYou can change these later with '2m configure'.",
        ).run()
    else:
        api_key = input_dialog(
            title=f"{info['label']} — API Key",
            text=f"Paste your {info['label']} API key:",
        ).run()
        if not api_key:
            console.print("[yellow]No API key provided. Check .env file or configure later.[/yellow]")
        model_choices = [(m, m) for m in info["models"]]
        model_result = radiolist_dialog(
            title="Select Model",
            text="Choose which model to use:",
            values=model_choices,
        ).run()
        model_name = model_result or info["default"]

    os.environ[info["env_key"]] = api_key if provider != "custom" else ""
    if provider == "custom" and api_key:
        os.environ["CUSTOM_API_KEY"] = api_key

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
