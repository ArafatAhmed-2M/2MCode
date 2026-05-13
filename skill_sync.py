#!/usr/bin/env python3
"""
2M Code — Skill Sync & Management Framework

Handles:
  • Cloning / pulling the global skills repository (ArafatAhmed-2M/skills.git)
  • Discovering available skill markdown files
  • Interactive checklist-based skill selection (max 3)
  • Injecting selected skill content into the orchestrator's state

Usage:
    from skill_sync import ensure_synced, select_skills_interactive, get_active_skill_contents
"""

from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path
from typing import Optional

from prompt_toolkit.shortcuts import checkboxlist_dialog, message_dialog
from prompt_toolkit.styles import Style as PtStyle
from rich.text import Text

from core.config import load_config, save_config, CONFIG_DIR
from core.ui import console, make_panel, status_spinner

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SKILLS_REPO: str = "https://github.com/ArafatAhmed-2M/skills.git"
SKILLS_DIR: Path = CONFIG_DIR / "skills"
MAX_SKILLS: int = 3

PROMPT_STYLE = PtStyle.from_dict({
    "dialog": "bg:#0a0a1a",
    "dialog.body": "bg:#0f1a2e",
    "dialog shadow": "bg:#000000",
    "checkbox": "white",
    "selected": "#00b4d8 bold",
    "text": "white",
    "title": "#00b4d8 bold",
    "radio": "white",
    "radio.selected": "#00b4d8 bold",
    "label": "white",
})


# ---------------------------------------------------------------------------
# Git Sync
# ---------------------------------------------------------------------------

def ensure_synced() -> Path:
    """
    Clone the global skills repository if it doesn't exist,
    or git pull the latest version. Returns the skills directory path.
    """
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


# ---------------------------------------------------------------------------
# Skill Discovery
# ---------------------------------------------------------------------------

def _extract_description(md_path: Path) -> str:
    """Extract first heading or first non-empty line from a skill markdown."""
    try:
        content = md_path.read_text(encoding="utf-8", errors="replace")
        # First # heading
        m = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        if m:
            return m.group(1).strip()
        # First meaningful line
        for line in content.splitlines():
            stripped = line.strip()
            if stripped:
                return stripped[:80]
    except Exception:
        pass
    return "No description"


def discover_skills() -> list[dict]:
    """
    Scan the skills directory for .md files and return a list of
    dicts with keys: name, path, description, content.
    """
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
    """Read the full markdown content of a single skill by name."""
    md_path = SKILLS_DIR / f"{name}.md"
    if md_path.exists():
        return md_path.read_text(encoding="utf-8", errors="replace")
    return None


# ---------------------------------------------------------------------------
# Interactive Selection (prompt_toolkit checklist)
# ---------------------------------------------------------------------------

def select_skills_interactive() -> list[str]:
    """
    Launch an interactive checkbox-list dialog to select skills (max 3).
    Returns a list of selected skill names. 'skill-creator' is always prepended.
    """
    skills_dir = ensure_synced()
    all_skills = discover_skills()

    if not all_skills:
        console.print("[yellow]No skills found in repository.[/yellow]")
        return ["skill-creator"]

    cfg = load_config()
    current_active = set(cfg.active_skills)

    # Build choices for the dialog
    choices = []
    for s in all_skills:
        label = s["description"]
        if s["name"] == "skill-creator":
            label += " [cyan](Create your own skills)[/cyan]"
        choices.append((s["name"], label))

    default_values = [name for name, _ in choices if name in current_active]
    if not default_values:
        default_values = ["skill-creator"]

    result = checkboxlist_dialog(
        title="2M Code — Skill Selection",
        text=f"Select up to {MAX_SKILLS} skills to activate (skill-creator is always included):",
        values=choices,
        default_values=default_values,
        style=PROMPT_STYLE,
    ).run()

    if result is None:
        console.print("[yellow]Using previously selected skills.[/yellow]")
        return cfg.active_skills

    selected = list(result)

    if "skill-creator" not in selected:
        selected.insert(0, "skill-creator")

    if len(selected) > MAX_SKILLS:
        selected = selected[:MAX_SKILLS]
        console.print(f"[yellow]Limited to {MAX_SKILLS} skills: {', '.join(selected)}[/yellow]")

    # Persist selection
    cfg.active_skills = selected
    save_config(cfg)

    # Show confirmation
    names = [s["description"] for s in all_skills if s["name"] in selected]
    console.print(make_panel(
        Text(f"Active: {', '.join(names)}", style="bold white"),
        title="Skills Loaded",
        border_style="green",
    ))

    return selected


# ---------------------------------------------------------------------------
# Skill Content Retrieval for Orchestrator
# ---------------------------------------------------------------------------

def get_active_skill_contents() -> list[dict]:
    """
    Read and return the full markdown content of all currently active skills.
    Returns a list of dicts: {name, content}.
    Used by the orchestrator to inject skill instructions into the system prompt.
    """
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
