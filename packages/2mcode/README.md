# 2M Code — Core Package

The main 2M Code package containing the core business logic, TUI server, CLI commands, and agent system.

## Structure

| Directory / File       | Purpose                                                |
| ---------------------- | ------------------------------------------------------ |
| `src/cli/cmd/tui/`     | TUI — built with SolidJS and [opentui](https://github.com/sst/opentui) |
| `src/server/`          | HTTP API server                                        |
| `src/provider/`        | LLM provider integrations                              |
| `src/skill/`           | Skill/prompt system                                    |
| `src/config/`          | Configuration modules                                  |
| `src/project/`         | Project-level state                                    |

## Quick Start

```bash
bun install
bun dev
```

## Development Commands

| Command                | Description                                                |
| ---------------------- | ---------------------------------------------------------- |
| `bun dev`              | Start the TUI in development mode                          |
| `bun dev serve`        | Start headless API server (port `4096`)                    |
| `bun dev web`          | Start server + open web interface                          |
| `bun run install:global` | Compile native binary and register in `PATH`             |
| `bun run build:local`  | Compile standalone executable only                         |

## Global Binary

After running `bun run install:global`, the `2mcode` CLI is available globally:

```bash
2mcode --help            # Show all available commands
2mcode serve             # Start headless API server
2mcode web               # Start server + open web interface
2mcode <directory>       # Start TUI in specified directory
```

## Debugging

```bash
bun run --inspect=ws://localhost:6499/ --cwd packages/2mcode ./src/index.ts serve --port 4096
```

> [!TIP]
> Set `BUN_OPTIONS=--inspect=ws://localhost:6499/` to avoid repeating the `--inspect` flag on every invocation.

See the [contributing guide](../../CONTRIBUTING.md) for detailed development instructions.
