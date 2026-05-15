#!/usr/bin/env python3
"""
2M Code — Orchestrator Engine
3-Layer Architecture: Directive → Orchestration → Execution
Auto-correcting loop with tool-based Python script execution.

This is the consolidated flat-file orchestrator. It implements the full
3-Layer system prompt, processes LLM responses, executes Python scripts,
and auto-corrects on failure (up to MAX_RETRIES attempts).
"""

from __future__ import annotations

import json
import os
import re
import textwrap
from pathlib import Path
from typing import Optional

from rich.live import Live
from rich.markdown import Markdown
from rich.spinner import Spinner
from rich.syntax import Syntax
from rich.text import Text

from core.config import AppConfig, load_config, save_config
from core.ui import console, make_panel, status_spinner, print_separator
from core.model_provider import send_message_sync, run_setup_wizard
from core.skill_manager import get_active_skill_contents
from execution.runner import run_python_code, extract_code_blocks

# ---------------------------------------------------------------------------
# Layer 1: The Directive — System Prompt (3-Layer Architecture)
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = textwrap.dedent("""\
You are 2M Code, an expert Staff AI Engineer operating within a strict 3-Layer Architecture.

============================================================
LAYER 1 — DIRECTIVE LAYER
============================================================
Follow standard operating procedures from `directives/`. Active Skills
are appended below — treat each as a specialized directive for that domain.

============================================================
LAYER 2 — ORCHESTRATION LAYER (YOU ARE HERE)
============================================================
1. ANALYZE — Break requests into actionable steps
2. DELEGATE — Call Python scripts via Layer 3 for ALL work
3. NEVER SIMULATE — Every action goes through real code execution
4. AUTO-ANNEAL — Up to 3 retries on script failure
5. COMMUNICATE — Explain actions and results clearly

Available tools:
  \u2022 execute_python(code, desc) — Write & run an isolated script
  \u2022 read_file(path)             — Read any workspace file
  \u2022 write_file(path, content)   — Write any workspace file
  \u2022 update_config(key, value)   — Change model/settings on the fly
  \u2022 finish(summary)             — Mark task complete

============================================================
LAYER 3 — EXECUTION LAYER
============================================================
- Include ALL imports at the top of every script
- Use pathlib for files, try/except for errors
- Print results to stdout (captured and returned)
- Store deliverables in workspace, temp data in .tmp/
- Never hardcode secrets; use env vars

============================================================
RULES
============================================================
1. ALWAYS use execute_python for computation \u2014 never simulate.
2. If a script fails, fix the code and retry (up to 3 attempts).
3. Call finish() when the entire task is done.
""")

MAX_RETRIES: int = 3


# ---------------------------------------------------------------------------
# System Prompt Builder
# ---------------------------------------------------------------------------

def build_system_prompt(cfg: AppConfig) -> str:
    """Build the full system prompt with skills and directives injected."""
    prompt = SYSTEM_PROMPT

    skills = get_active_skill_contents()
    if skills:
        prompt += "\n\n## Active Skills\n"
        for skill in skills:
            content = skill["content"][:2000]
            prompt += f"\n### Skill: {skill['name']}\n{content}\n---\n"

    directives_dir = Path.cwd() / "directives"
    if directives_dir.exists():
        prompt += "\n\n## Active Directives\n"
        for md_file in sorted(directives_dir.glob("*.md")):
            content = md_file.read_text(encoding="utf-8", errors="replace")
            prompt += f"\n### {md_file.stem}\n{content}\n---\n"

    return prompt


# ---------------------------------------------------------------------------
# Response Processing & Auto-Correction Loop
# ---------------------------------------------------------------------------

def process_llm_response(
    raw_response: str,
    messages: list[dict],
    cfg: AppConfig,
) -> str:
    """
    Extract and execute code blocks from the LLM response.
    Auto-corrects on failure (up to MAX_RETRIES).
    Returns the final text response or a __RETRY__ signal.
    """
    blocks = extract_code_blocks(raw_response)
    if not blocks:
        return raw_response

    console.print("[dim]\u2501\u2501\u2501 Execution Phase \u2501\u2501\u2501[/dim]")

    attempt = 0
    for i, block in enumerate(blocks):
        code = block["code"]

        console.print(make_panel(
            Syntax(code, "python", theme="monokai", line_numbers=True),
            title=f"Script {i + 1}/{len(blocks)}",
            border_style="cyan",
        ))

        result = run_python_code(code)

        if result.success:
            output = result.output[:500] if result.output.strip() else "(no output)"
            console.print(make_panel(
                Text(output, style="white"),
                title=f"Output {i + 1}",
                border_style="green",
            ))
            messages.append({
                "role": "user",
                "content": f"Script {i + 1} succeeded.\nOutput:\n```\n{result.output[:3000]}\n```",
            })
        else:
            console.print(make_panel(
                Syntax((result.error or "Unknown")[:600], "python", theme="monokai"),
                title=f"Error {i + 1}",
                border_style="red",
            ))

            attempt += 1
            if attempt <= MAX_RETRIES:
                console.print(f"[yellow]\u26a0 Auto-correcting ({attempt}/{MAX_RETRIES})...[/yellow]")
                messages.append({
                    "role": "user",
                    "content": (
                        f"Script {i + 1} failed. Error:\n"
                        f"```\n{result.error[:2000]}\n```\n\n"
                        f"Fix the script. Attempt {attempt}/{MAX_RETRIES}."
                    ),
                })
                return f"__RETRY__:{attempt}"

            console.print(f"[red]Failed after {MAX_RETRIES} retries.[/red]")
            messages.append({
                "role": "user",
                "content": (
                    f"Script failed after {MAX_RETRIES} attempts. "
                    f"Last error:\n```\n{result.error[:1000]}\n```\n"
                    f"Explain and suggest alternatives."
                ),
            })

    # After all scripts executed, get final summary from the LLM
    final = send_message_sync(messages, cfg)
    return final or "(No response)"


# ---------------------------------------------------------------------------
# Chat Loop
# ---------------------------------------------------------------------------

def run_chat_loop(cfg: Optional[AppConfig] = None) -> None:
    """
    Main interactive chat loop with auto-correction.
    Handles user input, model communication, script execution, and retries.
    """
    if cfg is None:
        cfg = load_config()

    system_prompt = build_system_prompt(cfg)
    messages: list[dict] = [{"role": "system", "content": system_prompt}]

    model_str = f"{cfg.model.provider} / {cfg.model.model_name}"
    skills_str = ", ".join(cfg.active_skills) if cfg.active_skills else "(none)"
    info_lines = [
        f"[bold white]Model:[/bold white]  [cyan]{model_str}[/cyan]",
        f"[bold white]Skills:[/bold white] [cyan]{skills_str}[/cyan]",
    ]
    console.print(make_panel(
        "\n".join(info_lines),
        title="2M Code Orchestrator",
        border_style="cyan",
    ))
    console.print("[dim]Type a task, /help for commands, exit to quit.[/dim]\n")

    while True:
        try:
            from prompt_toolkit import prompt as pt_prompt
            from prompt_toolkit.history import FileHistory
            from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

            history_path = Path.home() / ".2mcode_history"
            user_input = pt_prompt(
                "2m> ",
                history=FileHistory(str(history_path)),
                auto_suggest=AutoSuggestFromHistory(),
            ).strip()
        except (KeyboardInterrupt, EOFError):
            console.print("\n[yellow]Goodbye![/yellow]")
            break

        if not user_input:
            continue

        # ── Slash Commands ──
        if user_input.startswith("/"):
            parts = user_input.split(maxsplit=1)
            slash_cmd = parts[0].lower()
            args = parts[1] if len(parts) > 1 else ""

            if slash_cmd == "/connect":
                console.print("[yellow]Launching model setup wizard...[/yellow]")
                cfg = run_setup_wizard(show_header=False)
                system_prompt = build_system_prompt(cfg)
                messages = [{"role": "system", "content": system_prompt}]
                from core.model_provider import PROVIDERS
                p = PROVIDERS.get(cfg.model.provider, {})
                console.print(make_panel(
                    f"[bold green]Configuration hot-reloaded![/bold green]\n"
                    f"[white]Provider:[/white] [cyan]{cfg.model.provider}[/cyan]\n"
                    f"[white]Model:[/white] [cyan]{cfg.model.model_name}[/cyan]",
                    title="Connected",
                    border_style="green",
                ))
                continue

            elif slash_cmd == "/model":
                if args:
                    cfg.model.model_name = args
                    save_config(cfg)
                    system_prompt = build_system_prompt(cfg)
                    messages = [{"role": "system", "content": system_prompt}]
                    console.print(f"[green]Model switched to [bold white]{args}[/bold white] and saved.[/green]")
                else:
                    console.print("[yellow]Usage: /model <model_name>  (e.g. /model gpt-4o)[/yellow]")
                continue

            elif slash_cmd == "/clear":
                messages = [{"role": "system", "content": system_prompt}]
                console.clear()
                console.print("[green]Screen and context cleared.[/green]")
                continue

            elif slash_cmd == "/help":
                print_separator()
                console.print("[bold cyan]Available Commands[/bold cyan]")
                print_separator()
                commands = [
                    ("/connect", "Launch model setup wizard (hot-reload config)"),
                    ("/model <name>", "Switch AI model instantly & persist"),
                    ("/clear", "Clear terminal screen & chat history"),
                    ("/help", "Show this help menu"),
                    ("reset", "Reset conversation context only"),
                    ("exit / quit / q", "Exit 2M Code"),
                ]
                for cmd_name, desc in commands:
                    console.print(f"  [bold cyan]{cmd_name:<20}[/bold cyan] [white]{desc}[/white]")
                print_separator()
                continue

            else:
                console.print(f"[yellow]Unknown command: {slash_cmd}. Type /help for available commands.[/yellow]")
                continue

        # ── Standard exit / reset commands ──
        cmd = user_input.lower()
        if cmd in ("exit", "quit", "q"):
            console.print("[cyan]Shutting down 2M Code. Goodbye![/cyan]")
            break
        if cmd == "reset":
            messages = [{"role": "system", "content": system_prompt}]
            console.print("[yellow]Context reset. Ready for new session.[/yellow]")
            continue

        messages.append({"role": "user", "content": user_input})

        while True:
            with Live(
                Spinner("dots", text="[cyan]Orchestrator thinking..."),
                refresh_per_second=10,
                console=console,
            ):
                try:
                    raw_response = send_message_sync(messages, cfg)
                except Exception as e:
                    console.print(f"[red]Model error:[/red] {e}")
                    messages.pop()
                    break

            if not raw_response:
                console.print("[red]Empty response from model.[/red]")
                messages.pop()
                break

            result = process_llm_response(raw_response, messages, cfg)

            if result.startswith("__RETRY__"):
                continue

            if result.strip():
                md = Markdown(result)
                console.print(make_panel(md, title="2M Code", border_style="cyan"))

            break
