#!/usr/bin/env python3
"""
2M Code — Model-Agnostic Terminal AI Coding Assistant

A powerful, model-agnostic terminal AI coding assistant with a gorgeous
Blue/White UI, 3-Layer architecture, auto-correcting script execution,
skill management, and universal model provider support.

Usage:
    2m setup          Run interactive setup wizard
    2m configure      Reconfigure model or skills
    2m chat           Start interactive chat session
    2m run <prompt>   Execute a one-shot task
    2m --version      Show version info
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import click

from core.ui import console, make_panel
from core.config import load_config, CONFIG_DIR, CONFIG_FILE
from core.model_provider import run_setup_wizard
from core.skill_manager import interactive_skill_selection, ensure_synced
from skill_sync import load_library, search_skills
from orchestrator import run_chat_loop

__version__ = "2.0.0"
__author__ = "2M Code Team"


@click.group(invoke_without_command=True)
@click.option("--version", is_flag=True, help="Show version and exit")
@click.pass_context
def cli(ctx: click.Context, version: bool) -> None:
    if version:
        console.print(f"[bold cyan]2M Code[/bold cyan] [white]v{__version__}[/white]")
        console.print("[dim]Model-Agnostic Terminal AI Coding Assistant[/dim]")
        raise SystemExit(0)

    if ctx.invoked_subcommand is None:
        ctx.invoke(chat)


@cli.command()
def setup() -> None:
    """Run interactive setup wizard (model + skills)"""
    cfg = run_setup_wizard()

    console.print()
    console.print("[bold cyan]── Skill Configuration ──[/bold cyan]")
    console.print()

    ensure_synced()
    interactive_skill_selection()

    console.print()
    console.print(make_panel(
        "[bold green]Setup complete![/bold green] Run [bold white]2m chat[/bold white] to start.\n"
        "Run [bold white]2m configure[/bold white] to change settings later.",
        title="All Set",
        border_style="green",
    ))


@cli.command()
@click.option("--model", is_flag=True, help="Reconfigure model provider")
@click.option("--skills", is_flag=True, help="Re-select active skills")
def configure(model: bool, skills: bool) -> None:
    """Reconfigure 2M Code settings"""
    if not model and not skills:
        model = skills = True

    if model:
        run_setup_wizard()

    if skills:
        ensure_synced()
        interactive_skill_selection()

    console.print("[green]Configuration updated.[/green]")


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

    prompt_display = user_text[:80] + "..." if len(user_text) > 80 else user_text
    console.print(make_panel(
        f"[white]{prompt_display}[/white]",
        title="One-Shot Task",
        border_style="cyan",
    ))

    from orchestrator import build_system_prompt, process_llm_response
    from core.model_provider import send_message_sync

    system_prompt = build_system_prompt(cfg)
    messages: list[dict] = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_text},
    ]

    from rich.spinner import Spinner
    from rich.live import Live

    with Live(Spinner("dots", text="[cyan]Orchestrator processing..."), refresh_per_second=10, console=console):
        try:
            raw_response = send_message_sync(messages, cfg)
        except Exception as e:
            console.print(f"[red]Error:[/red] {e}")
            raise SystemExit(1)

    console.print()
    final_output = process_llm_response(raw_response, messages, cfg)

    if final_output:
        from rich.markdown import Markdown
        md = Markdown(final_output)
        console.print(make_panel(md, title="2M Code Result", border_style="cyan"))


@cli.command()
def chat() -> None:
    """Start interactive AI chat session"""
    cfg = load_config()

    header = make_panel(
        "[bold cyan]2M Code[/bold cyan] [white]v" + __version__ + "[/white]\n"
        "[dim]Model-Agnostic • Auto-Correcting • Skill-Powered[/dim]",
        border_style="cyan",
    )
    console.print(header)

    if not cfg.model.api_key:
        from core.model_provider import get_api_key
        key = get_api_key(cfg.model.provider)
        if not key:
            console.print("[yellow]No API key configured. Running setup...[/yellow]")
            cfg = run_setup_wizard()

    ensure_synced()

    has_skills = len(cfg.active_skills) > 0
    if not has_skills:
        interactive_skill_selection()

    console.print()
    info = make_panel(
        f"[bold white]Provider:[/bold white] [cyan]{cfg.model.provider}[/cyan]\n"
        f"[bold white]Model:[/bold white] [cyan]{cfg.model.model_name}[/cyan]\n"
        f"[bold white]Skills:[/bold white] [cyan]{', '.join(cfg.active_skills)}[/cyan]",
        title="Session Info",
        border_style="cyan",
    )
    console.print(info)

    run_chat_loop(cfg)


@cli.command()
def skills() -> None:
    """Manage active skills interactively"""
    ensure_synced()
    interactive_skill_selection()


@cli.command(name="library")
def library_cmd() -> None:
    """Load and display all available library files with live progress"""
    result = load_library()
    if not result:
        console.print("[yellow]No libraries loaded.[/yellow]")
        return
    names = [s["name"] for s in result]
    console.print(f"[green]Libraries:[/green] {', '.join(names)}")


@cli.command()
@click.argument("query", nargs=-1, required=True)
def search(query: tuple[str, ...]) -> None:
    """Search through all library/skill files for matching content"""
    query_text = " ".join(query)
    search_skills(query_text)


@cli.command()
def version() -> None:
    """Show version information"""
    console.print(f"[bold cyan]2M Code[/bold cyan] [white]v{__version__}[/white]")
    console.print(f"[dim]Config: {CONFIG_DIR}[/dim]")
    cfg = load_config()
    console.print(f"[dim]Provider: {cfg.model.provider} | Model: {cfg.model.model_name}[/dim]")
    console.print(f"[dim]Active Skills: {', '.join(cfg.active_skills)}[/dim]")


@cli.command()
def doctor() -> None:
    """Diagnose environment and configuration"""
    console.print("[bold cyan]── 2M Code Doctor ──[/bold cyan]")
    console.print()

    checks = [
        ("Python version", sys.version.split()[0], sys.version_info >= (3, 10)),
        ("Config file exists", str(CONFIG_FILE.exists()), CONFIG_FILE.exists()),
        ("Skills directory", str(CONFIG_DIR.exists()), CONFIG_DIR.exists()),
    ]

    from core.ui import show_table
    show_table(
        "System Check",
        ["Check", "Status", "OK?"],
        [[c[0], c[1], "[green]✓[/green]" if c[2] else "[red]✗[/red]"] for c in checks],
    )

    cfg = load_config()
    console.print()
    console.print(f"[bold]Provider:[/bold] {cfg.model.provider}")
    console.print(f"[bold]Model:[/bold] {cfg.model.model_name}")
    console.print(f"[bold]Skills:[/bold] {', '.join(cfg.active_skills)}")
    console.print(f"[bold]API Key Set:[/bold] {'[green]Yes[/green]' if cfg.model.api_key else '[yellow]No[/yellow]'}")
    console.print()

    if cfg.model.api_key:
        console.print("[green]All systems nominal.[/green]")
    else:
        console.print("[yellow]Run '2m setup' to configure API keys.[/yellow]")


if __name__ == "__main__":
    cli()
