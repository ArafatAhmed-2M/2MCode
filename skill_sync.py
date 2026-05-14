from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path
from typing import Optional

from rich.live import Live
from rich.padding import Padding
from rich.prompt import Prompt, IntPrompt
from rich.style import Style
from rich.table import Table
from rich.text import Text

from core.config import load_config, save_config, CONFIG_DIR
from core.ui import console, make_panel, status_spinner

SKILLS_REPO: str = "https://github.com/ArafatAhmed-2M/skills.git"
SKILLS_DIR: Path = CONFIG_DIR / "skills"
MAX_SKILLS: int = 3


def ensure_synced() -> Path:
    SKILLS_DIR.parent.mkdir(parents=True, exist_ok=True)

    if not (SKILLS_DIR / ".git").exists():
        console.print(make_panel(
            Text("Cloning global skills repository...", style="cyan"),
            title="Skills Sync",
            border_style="cyan",
        ))
        result = subprocess.run(
            ["git", "clone", SKILLS_REPO, str(SKILLS_DIR)],
            capture_output=True, text=True, timeout=120,
        )
        if result.returncode == 0:
            console.print("[green]✓ Skills repository cloned successfully.[/green]")
        else:
            console.print(f"[red]Failed to clone skills:[/red] {result.stderr}")
            console.print("[yellow]Continuing with local skills only.[/yellow]")
    else:
        with status_spinner("Pulling latest skills..."):
            result = subprocess.run(
                ["git", "-C", str(SKILLS_DIR), "pull", "--ff-only"],
                capture_output=True, text=True, timeout=60,
            )
            if result.returncode != 0:
                console.print(f"[dim]Skills sync note: {result.stderr.strip()}[/dim]")

    return SKILLS_DIR


def _extract_description(md_path: Path) -> str:
    try:
        content = md_path.read_text(encoding="utf-8", errors="replace")
        m = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        if m:
            return m.group(1).strip()
        for line in content.splitlines():
            stripped = line.strip()
            if stripped:
                return stripped[:80]
    except Exception:
        pass
    return "No description"


def discover_skills() -> list[dict]:
    if not SKILLS_DIR.exists():
        return []

    skills = []
    for md_file in sorted(SKILLS_DIR.glob("*.md")):
        content = md_file.read_text(encoding="utf-8", errors="replace")
        skills.append({
            "name": md_file.stem,
            "path": str(md_file),
            "description": _extract_description(md_file),
            "content": content,
        })
    return skills


def get_skill_content(name: str) -> Optional[str]:
    md_path = SKILLS_DIR / f"{name}.md"
    if md_path.exists():
        return md_path.read_text(encoding="utf-8", errors="replace")
    return None


def select_skills_interactive() -> list[str]:
    skills_dir = ensure_synced()
    all_skills = discover_skills()

    if not all_skills:
        console.print("[yellow]No skills found in repository.[/yellow]")
        return ["skill-creator"]

    cfg = load_config()
    current_active = set(cfg.active_skills)

    console.print(make_panel(
        f"[bold white]Select up to {MAX_SKILLS} skills to activate[/bold white]",
        title="2M Code — Skill Selection",
        border_style="cyan",
    ))
    console.print()
    for idx, s in enumerate(all_skills, 1):
        label = s["description"]
        if s["name"] == "skill-creator":
            label += " [cyan](Create your own skills)[/cyan]"
        active_mark = " [green]✓[/green]" if s["name"] in current_active else ""
        console.print(f"  [bold cyan]{idx}.[/bold cyan] [white]{label}[/white]{active_mark}")
    console.print()
    console.print("[dim]Enter numbers separated by commas (e.g. 1,3,5). Enter 0 for none, or leave blank to keep current.[/dim]")
    console.print()

    raw = Prompt.ask("[bold white]Your selection", default="").strip()
    if not raw:
        console.print("[yellow]Keeping previous selection.[/yellow]")
        return cfg.active_skills

    selected_indices = []
    for part in raw.split(","):
        part = part.strip()
        if part.isdigit():
            idx = int(part)
            if 1 <= idx <= len(all_skills):
                selected_indices.append(idx - 1)
            elif idx == 0:
                continue

    selected_names = [all_skills[i]["name"] for i in selected_indices]

    if "skill-creator" not in selected_names:
        selected_names.insert(0, "skill-creator")

    if len(selected_names) > MAX_SKILLS:
        selected_names = selected_names[:MAX_SKILLS]
        console.print(f"[yellow]Limited to {MAX_SKILLS} skills: {', '.join(selected_names)}[/yellow]")

    cfg.active_skills = selected_names
    save_config(cfg)

    names = [s["description"] for s in all_skills if s["name"] in selected_names]
    console.print(make_panel(
        Text(f"Active: {', '.join(names)}", style="bold white"),
        title="Skills Loaded",
        border_style="green",
    ))

    return selected_names


def get_active_skill_contents() -> list[dict]:
    cfg = load_config()
    ensure_synced()
    all_skills = discover_skills()
    skill_map = {s["name"]: s for s in all_skills}

    active = []
    for name in cfg.active_skills:
        if name in skill_map:
            active.append({"name": name, "content": skill_map[name]["content"]})
        else:
            console.print(f"[yellow]Skill '{name}' not found. Skipping.[/yellow]")

    return active


# ---------------------------------------------------------------------------
# Library Loading with Live Progress
# ---------------------------------------------------------------------------

def load_library() -> list[dict]:
    """
    Load all skill/library files with real-time progress display.

    The user can see each library being loaded as it is processed,
    without any interactive selection dialog required.
    Automatically ensures 'skill-creator' is in the active skills list.
    """
    skills_dir = ensure_synced()
    if not skills_dir.exists():
        return []

    md_files = sorted(skills_dir.glob("*.md"))
    if not md_files:
        console.print("[yellow]No library files found.[/yellow]")
        return []

    from rich import box

    table = Table(
        title="Library Loading",
        border_style="cyan",
        box=box.ROUNDED,
        title_style="bold white",
    )
    table.add_column("#", style="dim", width=3)
    table.add_column("Library", style="cyan", no_wrap=True)
    table.add_column("Description", style="white")
    table.add_column("Status", style="bold", width=8)

    skills = []
    with Live(table, refresh_per_second=10, console=console) as live:
        for i, md_file in enumerate(md_files, 1):
            name = md_file.stem
            desc = _extract_description(md_file)
            content = md_file.read_text(encoding="utf-8", errors="replace")

            skills.append({
                "name": name,
                "path": str(md_file),
                "description": desc,
                "content": content,
            })
            table.add_row(str(i), name, desc[:60], "[green]✓[/green]")
            live.update(table)

    cfg = load_config()
    if "skill-creator" not in cfg.active_skills:
        cfg.active_skills = ["skill-creator"] + [s["name"] for s in skills if s["name"] != "skill-creator"][:MAX_SKILLS]
        save_config(cfg)

    console.print(f"[green]✓ Loaded {len(skills)} libraries.[/green]")
    return skills


# ---------------------------------------------------------------------------
# Search with Incremental Results
# ---------------------------------------------------------------------------

def _append_with_highlight(
    text: Text,
    line: str,
    query: str,
    query_lower: str,
    highlight_style: Style,
) -> None:
    """Append a line to a Rich Text object with query terms highlighted."""
    idx = 0
    while idx < len(line):
        pos = line.lower().find(query_lower, idx)
        if pos == -1:
            text.append(line[idx:])
            break
        text.append(line[idx:pos])
        text.append(line[pos:pos + len(query)], style=highlight_style)
        idx = pos + len(query)


def search_skills(query: str) -> list[dict]:
    """
    Search through all library/skill files for the given query.

    Shows results as soon as they are found, with the matching term
    highlighted using a background colour.  A loading/spinner message
    is displayed only while the search is in progress.
    """
    skills_dir = ensure_synced()
    if not skills_dir.exists():
        return []

    md_files = sorted(skills_dir.glob("*.md"))
    if not md_files:
        console.print("[yellow]No library files to search.[/yellow]")
        return []

    query_lower = query.lower()
    results: list[dict] = []
    highlight = Style(bgcolor="dark_orange", bold=True)

    with console.status(f"[yellow]Scanning libraries...", spinner="dots") as status:
        for md_file in md_files:
            name = md_file.stem
            status.update(f"[yellow]Scanning {name}...")
            content = md_file.read_text(encoding="utf-8", errors="replace")

            if query_lower not in name.lower() and query_lower not in content.lower():
                continue

            preview = Text()
            lines = content.splitlines()
            matched = 0
            for line in lines:
                stripped = line.strip()
                if query_lower in stripped.lower() and matched < 3:
                    matched += 1
                    if preview:
                        preview.append("\n")
                    display_line = stripped[:80]
                    _append_with_highlight(preview, display_line, query, query_lower, highlight)

            if not matched:
                preview.append("(matched in name)", style="dim")

            results.append({"name": name, "preview": preview})
            console.print(f"\n  [cyan]{name}[/cyan]")
            console.print(Padding(preview, (0, 4)))

    if not results:
        console.print(f"[yellow]No matches found for '{query}'.[/yellow]")
    else:
        console.print(f"\n[green]✓ Found {len(results)} match(es).[/green]")

    return results
