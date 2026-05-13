from __future__ import annotations

import sys
import time
from contextlib import contextmanager
from typing import Generator, Optional

from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.style import Style
from rich.table import Table
from rich.text import Text
from rich.theme import Theme
from rich.tree import Tree
from rich.syntax import Syntax
from rich import box

BLUE_THEME = Theme({
    "info": "bold white on blue",
    "warn": "bold yellow",
    "error": "bold white on red",
    "debug": "bright_cyan",
    "success": "bold green",
    "title": "bold white",
    "subtitle": "cyan",
    "path": "bright_cyan",
    "code": "cyan on grey11",
    "dim": "grey58",
    "accent": "cyan",
    "highlight": "bold cyan",
    "border": "cyan",
})

console = Console(theme=BLUE_THEME, highlight=False)


def make_panel(content, title="", border_style="cyan", subtitle="") -> Panel:
    return Panel(
        content,
        title=title,
        subtitle=subtitle,
        border_style=border_style,
        box=box.ROUNDED,
        padding=(1, 2),
    )


def print_header() -> None:
    title = Text()
    title.append("  ██╗    ███╗   ███╗     ██████╗ ██████╗ ██████╗ ███████╗  \n", style="cyan")
    title.append("  ██║    ████╗ ████║    ██╔════╝██╔═══██╗██╔══██╗██╔════╝  \n", style="bright_cyan")
    title.append("  ██║ █╗ ██╔████╔██║    ██║     ██║   ██║██║  ██║█████╗    \n", style="cyan")
    title.append("  ██║███╗██║╚██╔╝██║    ██║     ██║   ██║██║  ██║██╔══╝    \n", style="bright_cyan")
    title.append("  ╚███╔███╔╝ ╚═╝ ╚═╝    ╚██████╗╚██████╔╝██████╔╝███████╗  \n", style="cyan")
    title.append("   ╚══╝╚══╝              ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝  \n", style="cyan")
    title.append("  ═══════════════════════  AI  ═══════════════════════════  \n", style="bright_cyan")
    subtitle = Text("Model-Agnostic Terminal AI Coding Assistant", style="bold white")
    console.print(Panel(title, box=box.DOUBLE_EDGE, border_style="cyan"))
    console.print()


def show_status(message: str) -> None:
    with Progress(
        SpinnerColumn("dots", style="cyan"),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True,
    ) as progress:
        progress.add_task(f"[cyan]{message}", total=None)
        time.sleep(0.3)


@contextmanager
def status_spinner(message: str) -> Generator:
    with Progress(
        SpinnerColumn("dots", style="cyan"),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True,
    ) as progress:
        task = progress.add_task(f"[cyan]{message}", total=None)
        try:
            yield
        finally:
            progress.remove_task(task)


def show_table(title: str, columns: list[str], rows: list[list[str]]) -> None:
    table = Table(
        title=title,
        border_style="cyan",
        header_style="bold cyan",
        box=box.ROUNDED,
        title_style="bold white",
    )
    for col in columns:
        table.add_column(col)
    for row in rows:
        table.add_row(*row)
    console.print(table)


def show_traceback(tb_text: str) -> None:
    syntax = Syntax(tb_text, "python", theme="monokai", line_numbers=True)
    console.print(make_panel(syntax, title="[error]Traceback", border_style="red"))


def show_result(text: str, title: str = "Result") -> None:
    console.print(make_panel(Text(text, style="white"), title=title, border_style="cyan"))


def show_skill_header(name: str, content_preview: str) -> None:
    from rich.markdown import Markdown
    md = Markdown(content_preview[:200] + "...")
    console.print(make_panel(md, title=f"[bold cyan]Skill: {name}", border_style="cyan"))


def stream_text(text: str, speed: float = 0.008) -> None:
    for char in text:
        console.print(char, end="", style="white")
        time.sleep(speed)
    console.print()


def print_separator() -> None:
    console.print("─" * console.width, style="dim cyan")


def confirm_action(message: str) -> bool:
    from prompt_toolkit.shortcuts import confirm as pt_confirm
    return pt_confirm(message)
