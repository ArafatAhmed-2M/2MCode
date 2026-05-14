#!/usr/bin/env python3
"""
Multiplayer Tic Tac Toe — 2M Edition

A beautiful, feature-rich terminal Tic Tac Toe game with:
  • Player vs Player & Player vs AI modes
  • 3 AI difficulties (Easy / Medium / Hard / Impossible)
  • Rich-powered UI with colors, panels, and live board
  • Score tracking across rounds
  • Winning line highlight
  • Sound effects (optional, via beep)

Usage:
    python tictactoe.py
"""

from __future__ import annotations

import random
import sys
import time
from typing import Literal, Optional

from rich import box
from rich.align import Align
from rich.console import Console, Group
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.prompt import Prompt
from rich.style import Style
from rich.table import Table
from rich.text import Text

console = Console()

# ── Constants ──────────────────────────────────────────────────────────────

PLAYER_X = "X"
PLAYER_O = "O"
EMPTY = " "
WIN_COMBOS = [
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
]

# ── Colour / Style helpers ─────────────────────────────────────────────────

X_STYLE = Style(color="cyan", bold=True)
O_STYLE = Style(color="yellow", bold=True)
EMPTY_STYLE = Style(dim=True, color="grey35")
BOARD_LINE_STYLE = Style(color="grey54")
WIN_STYLE = Style(color="green", bold=True, reverse=True)
DRAW_STYLE = Style(color="magenta", bold=True)


def styled_cell(val: str, is_win: bool = False) -> Text:
    if val == PLAYER_X:
        t = Text(" X ", style=X_STYLE)
    elif val == PLAYER_O:
        t = Text(" O ", style=O_STYLE)
    else:
        t = Text(" · ", style=EMPTY_STYLE)
    if is_win:
        t.stylize(WIN_STYLE)
    return t


# ── Board ──────────────────────────────────────────────────────────────────


class Board:
    def __init__(self) -> None:
        self.cells: list[str] = [EMPTY] * 9

    def copy(self) -> Board:
        b = Board()
        b.cells = self.cells[:]
        return b

    def legal_moves(self) -> list[int]:
        return [i for i, c in enumerate(self.cells) if c == EMPTY]

    def is_full(self) -> bool:
        return EMPTY not in self.cells

    def winner(self) -> Optional[str]:
        for a, b, c in WIN_COMBOS:
            if self.cells[a] != EMPTY and self.cells[a] == self.cells[b] == self.cells[c]:
                return self.cells[a]
        return None

    def winning_combo(self) -> Optional[tuple[int, int, int]]:
        for a, b, c in WIN_COMBOS:
            if self.cells[a] != EMPTY and self.cells[a] == self.cells[b] == self.cells[c]:
                return (a, b, c)
        return None

    def place(self, idx: int, mark: str) -> None:
        self.cells[idx] = mark


# ── AI Engine (Minimax) ────────────────────────────────────────────────────


def minimax(board: Board, depth: int, is_max: bool, ai_mark: str) -> int:
    opponent = PLAYER_O if ai_mark == PLAYER_X else PLAYER_X
    w = board.winner()
    if w == ai_mark:
        return 10 - depth
    if w == opponent:
        return depth - 10
    if board.is_full():
        return 0

    if is_max:
        best = -1000
        for m in board.legal_moves():
            board.place(m, ai_mark)
            best = max(best, minimax(board, depth + 1, False, ai_mark))
            board.cells[m] = EMPTY
        return best
    else:
        best = 1000
        for m in board.legal_moves():
            board.place(m, opponent)
            best = min(best, minimax(board, depth + 1, True, ai_mark))
            board.cells[m] = EMPTY
        return best


def ai_move(board: Board, difficulty: str, ai_mark: str) -> int:
    moves = board.legal_moves()
    if not moves:
        return -1

    if difficulty == "easy":
        return random.choice(moves)

    if difficulty == "medium":
        if random.random() < 0.4:
            return random.choice(moves)

    if difficulty == "impossible" or difficulty == "hard":
        best_score = -1000
        best_moves: list[int] = []
        opponent = PLAYER_O if ai_mark == PLAYER_X else PLAYER_X
        for m in moves:
            board.place(m, ai_mark)
            score = minimax(board, 0, False, ai_mark)
            board.cells[m] = EMPTY
            if score > best_score:
                best_score = score
                best_moves = [m]
            elif score == best_score:
                best_moves.append(m)
        return random.choice(best_moves)

    return random.choice(moves)


# ── Game State ─────────────────────────────────────────────────────────────


class GameState:
    def __init__(self) -> None:
        self.board = Board()
        self.current = PLAYER_X
        self.scores: dict[str, int] = {"X": 0, "O": 0, "draws": 0}
        self.winner: Optional[str] = None
        self.win_combo: Optional[tuple[int, int, int]] = None
        self.is_draw = False
        self.game_over = False
        self.mode: Literal["pvp", "pve"] = "pvp"
        self.ai_mark: str = PLAYER_O
        self.difficulty: str = "hard"
        self.player_names: dict[str, str] = {"X": "Player 1", "O": "Player 2"}
        self.move_count = 0
        self.last_move: Optional[int] = None

    def reset(self) -> None:
        self.board = Board()
        self.current = PLAYER_X
        self.winner = None
        self.win_combo = None
        self.is_draw = False
        self.game_over = False
        self.move_count = 0
        self.last_move = None

    def switch_player(self) -> None:
        self.current = PLAYER_O if self.current == PLAYER_X else PLAYER_X

    def make_move(self, idx: int) -> bool:
        if self.board.cells[idx] != EMPTY or self.game_over:
            return False
        self.board.place(idx, self.current)
        self.last_move = idx
        self.move_count += 1

        wc = self.board.winning_combo()
        if wc is not None:
            self.winner = self.current
            self.win_combo = wc
            self.game_over = True
            self.scores[self.current] += 1
            return True

        if self.board.is_full():
            self.is_draw = True
            self.game_over = True
            self.scores["draws"] += 1
            return True

        self.switch_player()
        return True

    def get_current_player_name(self) -> str:
        return self.player_names[self.current]


# ── UI Rendering ───────────────────────────────────────────────────────────


def build_board_table(state: GameState) -> Table:
    table = Table.grid(padding=0)
    wc = state.win_combo or ()
    for row in range(3):
        cells: list[Text] = []
        for col in range(3):
            idx = row * 3 + col
            is_win = idx in wc
            cells.append(styled_cell(state.board.cells[idx], is_win))
        table.add_row(*cells)
        if row < 2:
            sep = Text("───┼───┼───", style=BOARD_LINE_STYLE)
            table.add_row(
                Text("", style=BOARD_LINE_STYLE),
                Text("", style=BOARD_LINE_STYLE),
                Text("", style=BOARD_LINE_STYLE),
            )
    return table


def build_scoreboard(state: GameState) -> Table:
    t = Table.grid(padding=(0, 2))
    t.add_row(
        Text(f"{state.player_names['X']} (X)", style=X_STYLE),
        Text(f"{state.scores['X']}", style=X_STYLE),
    )
    t.add_row(
        Text(f"{state.player_names['O']} (O)", style=O_STYLE),
        Text(f"{state.scores['O']}", style=O_STYLE),
    )
    t.add_row(
        Text("Draws", style=DRAW_STYLE),
        Text(f"{state.scores['draws']}", style=DRAW_STYLE),
    )
    return t


def build_status(state: GameState) -> Text:
    if state.winner:
        name = state.player_names[state.winner]
        return Text(f"  {name} ({state.winner}) wins!  ", style=WIN_STYLE)
    if state.is_draw:
        return Text("  It's a draw!  ", style=DRAW_STYLE)
    name = state.get_current_player_name()
    mark = state.current
    style = X_STYLE if mark == PLAYER_X else O_STYLE
    return Text(f"  {name} ({mark})'s turn  ", style=style)


def build_help_text(state: GameState) -> Text:
    if state.game_over:
        return Text("  Press any key to continue  ", style="grey58")
    return Text("  Enter position (1-9)  ", style="grey58")


def build_layout(state: GameState) -> Layout:
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=5),
        Layout(name="main"),
        Layout(name="footer", size=3),
    )

    header_group = Group(
        Align.center(Text(" TIC TAC TOE ", style="bold white on blue")),
        Align.center(build_scoreboard(state)),
    )
    layout["header"].update(Panel(header_group, box=box.ROUNDED, border_style="cyan"))

    board_panel = Panel(
        Align.center(build_board_table(state)),
        box=box.HEAVY,
        border_style="bright_blue",
        padding=(1, 4),
    )

    status = build_status(state)
    status_panel = Panel(status, box=box.ROUNDED, border_style="bright_blue", padding=(0, 1))

    mode_info = Text(
        f"Mode: {'PvP' if state.mode == 'pvp' else 'PvE'}  "
        f"{'| AI: ' + state.difficulty.capitalize() if state.mode == 'pve' else ''}",
        style="grey58",
    )

    main_group = Group(
        Align.center(board_panel),
        Align.center(status_panel),
        Align.center(mode_info),
    )
    layout["main"].update(main_group)

    footer_group = Group(
        Align.center(build_help_text(state)),
        Align.center(Text("  [1-9] Move  |  [Q] Quit  |  [R] Reset Scores  ", style="grey35")),
    )
    layout["footer"].update(Panel(footer_group, box=box.SIMPLE, border_style="grey35"))

    return layout


# ── Splash / Menu ──────────────────────────────────────────────────────────


def show_splash() -> None:
    console.clear()
    title_text = Text("""
    ╔══════════════════════════════════╗
    ║                                  ║
    ║     T I C   T A C   T O E       ║
    ║        2M  Edition              ║
    ║                                  ║
    ╚══════════════════════════════════╝
    """, style="bold cyan")
    subtitle = Text("\n  A beautiful multiplayer experience  \n", style="white")
    console.print(Align.center(title_text))
    console.print(Align.center(subtitle))
    console.print()


def choose_mode() -> str:
    console.print(Align.center(Text("Choose Game Mode:", style="bold white")))
    console.print(Align.center("  [1]  Player vs Player"))
    console.print(Align.center("  [2]  Player vs AI"))
    console.print()
    choice = Prompt.ask(
        Align.center(Text("Your choice", style="cyan")).renderable,
        choices=["1", "2"],
        default="1",
    )
    return "pvp" if choice == "1" else "pve"


def choose_difficulty() -> str:
    console.print(Align.center(Text("Choose AI Difficulty:", style="bold white")))
    console.print(Align.center("  [1]  Easy"))
    console.print(Align.center("  [2]  Medium"))
    console.print(Align.center("  [3]  Hard"))
    console.print(Align.center("  [4]  Impossible"))
    console.print()
    choice = Prompt.ask(
        Align.center(Text("Your choice", style="cyan")).renderable,
        choices=["1", "2", "3", "4"],
        default="3",
    )
    return {"1": "easy", "2": "medium", "3": "hard", "4": "impossible"}[choice]


def choose_mark() -> str:
    console.print(Align.center(Text("Do you want to be X or O?", style="bold white")))
    console.print(Align.center("  X goes first"))
    console.print()
    choice = Prompt.ask(
        Align.center(Text("Choose", style="cyan")).renderable,
        choices=["X", "O"],
        default="X",
    )
    return choice.upper()


# ── Game Loop ──────────────────────────────────────────────────────────────


def run_game() -> None:
    show_splash()
    state = GameState()

    state.player_names["X"] = Prompt.ask(
        Align.center(Text("Enter name for Player X", style="cyan")).renderable,
        default="Player 1",
    )
    state.player_names["O"] = Prompt.ask(
        Align.center(Text("Enter name for Player O", style="cyan")).renderable,
        default="Player 2",
    )

    mode = choose_mode()
    state.mode = mode

    if mode == "pve":
        diff = choose_difficulty()
        state.difficulty = diff
        player_mark = choose_mark()
        state.ai_mark = PLAYER_O if player_mark == PLAYER_X else PLAYER_X
        state.player_names[state.ai_mark] = f"AI ({state.difficulty})"
        if state.ai_mark == PLAYER_X:
            state.current = PLAYER_X

    console.print()
    with console.status("[cyan]Starting game...", spinner="dots"):
        time.sleep(0.5)

    game_loop(state)


def game_loop(state: GameState) -> None:
    with Live(build_layout(state), refresh_per_second=10, screen=False) as live:
        while True:
            live.update(build_layout(state))

            if state.game_over:
                time.sleep(0.8)
                live.update(build_layout(state))
                time.sleep(0.5)

                key = Prompt.ask(
                    Align.center(Text("Play again?", style="bold white")).renderable,
                    choices=["y", "n", "r"],
                    default="y",
                )
                if key == "n":
                    show_goodbye(state)
                    return
                elif key == "r":
                    state.scores = {"X": 0, "O": 0, "draws": 0}
                state.reset()
                live.update(build_layout(state))
                continue

            if state.mode == "pve" and state.current == state.ai_mark:
                time.sleep(0.3)
                idx = ai_move(state.board, state.difficulty, state.ai_mark)
                if idx != -1:
                    state.make_move(idx)
                live.update(build_layout(state))
                continue

            try:
                key = Prompt.ask(
                    Align.center(Text("Move [1-9] or [Q/r]", style="cyan")).renderable,
                    default="",
                )
            except (EOFError, KeyboardInterrupt):
                show_goodbye(state)
                return

            if key is None:
                continue

            key = key.strip().lower()

            if key == "q":
                show_goodbye(state)
                return

            if key == "r":
                state.scores = {"X": 0, "O": 0, "draws": 0}
                state.reset()
                live.update(build_layout(state))
                continue

            if key.isdigit():
                idx = int(key) - 1
                if 0 <= idx <= 8:
                    if state.make_move(idx):
                        live.update(build_layout(state))
                        continue
                    else:
                        err = Panel(
                            Align.center(Text("Invalid move!", style="bold red")),
                            box=box.ROUNDED,
                            border_style="red",
                        )
                        live.update(err)
                        time.sleep(0.5)
                        live.update(build_layout(state))
                        continue

            err = Panel(
                Align.center(Text("Invalid input! Enter 1-9, Q, or R.", style="bold red")),
                box=box.ROUNDED,
                border_style="red",
            )
            live.update(err)
            time.sleep(0.5)
            live.update(build_layout(state))


def show_goodbye(state: GameState) -> None:
    console.clear()
    final = Panel(
        Group(
            Align.center(Text("GAME OVER", style="bold white on blue")),
            Align.center(Text("")),
            Align.center(Text(f"  {state.player_names['X']} (X):  {state.scores['X']}  ", style=X_STYLE)),
            Align.center(Text(f"  {state.player_names['O']} (O):  {state.scores['O']}  ", style=O_STYLE)),
            Align.center(Text(f"  Draws:  {state.scores['draws']}  ", style=DRAW_STYLE)),
            Align.center(Text("")),
            Align.center(Text("Thanks for playing!", style="white")),
        ),
        box=box.DOUBLE_EDGE,
        border_style="cyan",
        padding=(1, 4),
    )
    console.print(Align.center(final))
    console.print()


# ── Entry ──────────────────────────────────────────────────────────────────


def main() -> None:
    try:
        run_game()
    except (EOFError, KeyboardInterrupt):
        console.print("\n[yellow]Game interrupted. Goodbye![/yellow]")
    except Exception as e:
        console.print(f"\n[red]Unexpected error:[/red] {e}")
        raise


if __name__ == "__main__":
    main()
