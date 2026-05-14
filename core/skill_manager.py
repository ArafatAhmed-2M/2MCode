from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional

from rich.prompt import Prompt, IntPrompt
from rich.text import Text
from rich.markdown import Markdown

from core.config import load_config, save_config, CONFIG_DIR
from core.ui import console, make_panel, show_status, status_spinner

SKILLS_REPO = "https://github.com/ArafatAhmed-2M/skills.git"
SKILLS_DIR = CONFIG_DIR / "skills"
MAX_SKILLS = 3


def ensure_synced() -> Path:
    if not SKILLS_DIR.exists():
        console.print(make_panel(
            Text("Cloning global skills repository...", style="cyan"),
            title="Skills Sync",
            border_style="cyan",
        ))
        SKILLS_DIR.parent.mkdir(parents=True, exist_ok=True)
        result = subprocess.run(
            ["git", "clone", SKILLS_REPO, str(SKILLS_DIR)],
            capture_output=True, text=True, timeout=120,
        )
        if result.returncode != 0:
            console.print(f"[red]Failed to clone skills repo:[/red] {result.stderr}")
            console.print("[yellow]Continuing with local skills only.[/yellow]")
        else:
            console.print("[green]Skills repository cloned successfully.[/green]")
    else:
        with status_spinner("Pulling latest skills..."):
            result = subprocess.run(
                ["git", "-C", str(SKILLS_DIR), "pull", "--ff-only"],
                capture_output=True, text=True, timeout=60,
            )
            if result.returncode == 0:
                pass
            else:
                console.print(f"[dim]Skills sync: {result.stderr.strip()}[/dim]")

    return SKILLS_DIR


def discover_skills(skills_dir: Optional[Path] = None) -> list[dict]:
    if skills_dir is None:
        skills_dir = SKILLS_DIR
    if not skills_dir.exists():
        return []

    skills = []
    for md_file in sorted(skills_dir.glob("*.md")):
        content = md_file.read_text(encoding="utf-8", errors="replace")
        first_line = content.split("\n")[0].strip().lstrip("#").strip() if content else md_file.stem
        skill_name = md_file.stem
        skills.append({
            "name": skill_name,
            "label": first_line or skill_name,
            "path": str(md_file),
            "content": content,
        })
    return skills


def interactive_skill_selection() -> list[str]:
    skills_dir = ensure_synced()
    all_skills = discover_skills(skills_dir)
    cfg = load_config()
    current_active = set(cfg.active_skills)

    if not all_skills:
        console.print("[yellow]No skills found in repository.[/yellow]")
        default = ["skill-creator"]
        cfg.active_skills = default
        save_config(cfg)
        return default

    console.print(make_panel(
        f"[bold white]Select up to {MAX_SKILLS} skills to activate[/bold white]",
        title="2M Code — Skill Selection",
        border_style="cyan",
    ))
    console.print()
    for idx, s in enumerate(all_skills, 1):
        label = s["label"]
        if s["name"] == "skill-creator":
            label += " [cyan](Special: Create your own skills)[/cyan]"
        else:
            label += f" [dim]{s['name']}[/dim]"
        active_mark = " [green]✓[/green]" if s["name"] in current_active else ""
        console.print(f"  [bold cyan]{idx}.[/bold cyan] [white]{label}[/white]{active_mark}")
    console.print()
    console.print("[dim]Enter numbers separated by commas (e.g. 1,3,5). Leave blank to keep current.[/dim]")
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

    selected_names = [all_skills[i]["name"] for i in selected_indices]

    if "skill-creator" not in selected_names:
        selected_names.insert(0, "skill-creator")

    if len(selected_names) > MAX_SKILLS:
        selected_names = selected_names[:MAX_SKILLS]
        console.print(f"[yellow]Limited to {MAX_SKILLS} skills. Keeping: {', '.join(selected_names)}[/yellow]")

    skill_names = [s["label"] for s in all_skills if s["name"] in selected_names]
    console.print(make_panel(
        Text(f"Active skills: {', '.join(skill_names)}", style="bold white"),
        title="Skills Loaded",
        border_style="green",
    ))

    cfg.active_skills = selected_names
    save_config(cfg)
    return selected_names


def get_active_skill_contents() -> list[dict]:
    cfg = load_config()
    skills_dir = ensure_synced()
    all_skills = discover_skills(skills_dir)

    skill_map = {s["name"]: s for s in all_skills}
    active = []
    for name in cfg.active_skills:
        if name in skill_map:
            active.append(skill_map[name])
        else:
            console.print(f"[yellow]Skill '{name}' not found locally. Skipping.[/yellow]")

    return active


def get_skill_content_by_name(name: str) -> Optional[str]:
    skills_dir = SKILLS_DIR
    if not skills_dir.exists():
        return None
    md_file = skills_dir / f"{name}.md"
    if md_file.exists():
        return md_file.read_text(encoding="utf-8", errors="replace")
    return None
