#!/usr/bin/env python3
"""
2M Code — Model-Agnostic Terminal AI Coding Assistant
======================================================
A powerful, model-agnostic terminal AI coding assistant with a gorgeous
Blue/White UI, 3-Layer architecture (Directive → Orchestration → Execution),
auto-correcting script execution, skill management, and universal model
provider support via LiteLLM.

Usage:
    2m setup          Run interactive setup wizard
    2m configure      Reconfigure model or skills
    2m chat           Start interactive AI chat session (default)
    2m run <prompt>   Execute a one-shot task
    2m skills         Manage active skills
    2m version        Show version and configuration info
    2m doctor         Diagnose environment and configuration
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import click
from rich.markdown import Markdown
from rich.text import Text
from rich.live import Live
from rich.spinner import Spinner

from core.config import AppConfig, load_config, save_config, CONFIG_DIR, CONFIG_FILE, get_api_key
from core.ui import console, make_panel, show_table, status_spinner, print_header
from core.model_provider import run_setup_wizard as model_setup_wizard, send_message_sync

from orchestrator import run_chat_loop, build_system_prompt, process_llm_response
from skill_sync import ensure_synced, select_skills_interactive, load_library, search_skills

__version__ = "2.0.0"
__author__ = "2M Code Team"


# ---------------------------------------------------------------------------
# Click CLI
# ---------------------------------------------------------------------------

@click.group(invoke_without_command=True)
@click.option("--version", is_flag=True, help="Show version and exit")
@click.pass_context
def cli(ctx: click.Context, version: bool) -> None:
    """2M Code — Model-Agnostic AI Coding Assistant"""
    if version:
        console.print(f"[bold cyan]2M Code[/bold cyan] [white]v{__version__}[/white]")
        console.print("[dim]Model-Agnostic • Auto-Correcting • Skill-Powered[/dim]")
        raise SystemExit(0)

    if ctx.invoked_subcommand is None:
        ctx.invoke(chat)


# ---------------------------------------------------------------------------
# Setup Command
# ---------------------------------------------------------------------------

@cli.command()
def setup() -> None:
    """Run the interactive setup wizard (model + skills)"""
    # Step 1: Model provider setup (prints its own header)
    cfg = model_setup_wizard()

    # Step 2: Skill selection
    console.print()
    console.print("[bold cyan]── Skill Configuration ──[/bold cyan]")
    console.print()
    ensure_synced()
    select_skills_interactive()

    console.print()
    console.print(make_panel(
        "[bold green]Setup complete![/bold green] Run [bold white]2m chat[/bold white] to start.\n"
        "Run [bold white]2m configure[/bold white] to change settings later.",
        title="All Set",
        border_style="green",
    ))


# ---------------------------------------------------------------------------
# Configure Command
# ---------------------------------------------------------------------------

@cli.command()
@click.option("--model", is_flag=True, help="Reconfigure model provider")
@click.option("--skills", is_flag=True, help="Re-select active skills")
def configure(model: bool, skills: bool) -> None:
    """Reconfigure 2M Code settings (model and/or skills)"""
    if not model and not skills:
        model = skills = True

    if model:
        model_setup_wizard()

    if skills:
        ensure_synced()
        select_skills_interactive()

    console.print("[green]Configuration updated.[/green]")


# ---------------------------------------------------------------------------
# Run Command (One-Shot)
# ---------------------------------------------------------------------------

@cli.command()
@click.argument("prompt", nargs=-1, required=False)
def run(prompt: tuple[str, ...]) -> None:
    """Execute a one-shot task with the AI"""
    if not prompt:
        console.print("[yellow]Usage: 2m run <your prompt>[/yellow]")
        console.print("[dim]Example: 2m run create a python script to fetch weather data[/dim]")
        raise SystemExit(1)

    user_text = " ".join(prompt)
    cfg = load_config()

    preview = user_text[:80] + "..." if len(user_text) > 80 else user_text
    console.print(make_panel(
        Text(preview, style="white"),
        title="One-Shot Task",
        border_style="cyan",
    ))

    system_prompt = build_system_prompt(cfg)
    messages: list[dict] = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_text},
    ]

    with Live(
        Spinner("dots", text="[cyan]Orchestrator processing..."),
        refresh_per_second=10,
        console=console,
    ):
        try:
            raw_response = send_message_sync(messages, cfg)
        except Exception as e:
            console.print(f"[red]Error:[/red] {e}")
            raise SystemExit(1)

    console.print()
    final_output = process_llm_response(raw_response, messages, cfg)

    if final_output and not final_output.startswith("__RETRY__"):
        md = Markdown(final_output)
        console.print(make_panel(md, title="2M Code Result", border_style="cyan"))


# ---------------------------------------------------------------------------
# Chat Command (Default)
# ---------------------------------------------------------------------------

@cli.command()
def chat() -> None:
    """Start interactive AI chat session (default command)"""
    cfg = load_config()

    # Show the gorgeous banner
    print_header()

    # Ensure API key is available
    if not cfg.model.api_key:
        key = get_api_key(cfg.model.provider)
        if not key:
            console.print("[yellow]No API key configured. Running setup...[/yellow]")
            cfg = model_setup_wizard()

    # Sync skills & prompt for selection if none active
    ensure_synced()
    if len(cfg.active_skills) == 0:
        select_skills_interactive()

    # Display session info
    model_name = f"{cfg.model.provider}/{cfg.model.model_name}"
    skills_str = ", ".join(cfg.active_skills) if cfg.active_skills else "(none)"

    console.print(make_panel(
        f"[bold white]Provider:[/bold white] [cyan]{model_name}[/cyan]\n"
        f"[bold white]Skills:[/bold white]   [cyan]{skills_str}[/cyan]",
        title="Session Info",
        border_style="cyan",
    ))

    # Launch the orchestrator chat loop
    run_chat_loop(cfg)


# ---------------------------------------------------------------------------
# Skills Command
# ---------------------------------------------------------------------------

@cli.command()
def skills() -> None:
    """Manage active skills interactively"""
    ensure_synced()
    select_skills_interactive()
    cfg = load_config()
    console.print(f"[green]Active skills:[/green] {', '.join(cfg.active_skills)}")


# ---------------------------------------------------------------------------
# Library Command
# ---------------------------------------------------------------------------

@cli.command(name="library")
def library_cmd() -> None:
    """Load and display all available library files with live progress"""
    result = load_library()
    if not result:
        console.print("[yellow]No libraries loaded.[/yellow]")
        return
    names = [s["name"] for s in result]
    console.print(f"[green]Libraries:[/green] {', '.join(names)}")


# ---------------------------------------------------------------------------
# Search Command
# ---------------------------------------------------------------------------

@cli.command()
@click.argument("query", nargs=-1, required=True)
def search(query: tuple[str, ...]) -> None:
    """Search through all library/skill files for matching content"""
    query_text = " ".join(query)
    search_skills(query_text)


# ---------------------------------------------------------------------------
# Version Command
# ---------------------------------------------------------------------------

@cli.command()
def version() -> None:
    """Show version and configuration information"""
    console.print(f"[bold cyan]2M Code[/bold cyan] [white]v{__version__}[/white]")
    console.print(f"[dim]Config: {CONFIG_DIR}[/dim]")
    cfg = load_config()
    console.print(f"[dim]Provider: {cfg.model.provider} | Model: {cfg.model.model_name}[/dim]")
    console.print(f"[dim]Active Skills: {', '.join(cfg.active_skills)}[/dim]")


# ---------------------------------------------------------------------------
# Doctor Command
# ---------------------------------------------------------------------------

@cli.command()
def doctor() -> None:
    """Diagnose environment and configuration"""
    console.print("[bold cyan]── 2M Code Doctor ──[/bold cyan]")
    console.print()

    config_exists = CONFIG_FILE.exists()
    skills_dir_exists = (CONFIG_DIR / "skills").exists()

    checks = [
        ("Python version", sys.version.split()[0], sys.version_info >= (3, 10)),
        ("Config file", str(CONFIG_FILE), config_exists),
        ("Skills cache", str(CONFIG_DIR / "skills"), skills_dir_exists),
    ]

    show_table(
        "System Check",
        ["Check", "Location", "Status"],
        [
            [c[0], c[1], "[green]✓[/green]" if c[2] else "[red]✗[/red]"]
            for c in checks
        ],
    )

    cfg = load_config()
    console.print()
    console.print(f"[bold]Provider:[/bold] {cfg.model.provider}")
    console.print(f"[bold]Model:[/bold] {cfg.model.model_name}")
    console.print(f"[bold]API Key Set:[/bold] {'[green]Yes[/green]' if cfg.model.api_key else '[yellow]No[/yellow]'}")
    console.print(f"[bold]Skills:[/bold] {', '.join(cfg.active_skills)}")
    console.print()

    if cfg.model.api_key:
        console.print("[green]All systems nominal.[/green]")
    else:
        console.print("[yellow]Run '2m setup' to configure API keys.[/yellow]")


# ---------------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    cli()
