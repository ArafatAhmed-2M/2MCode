# 2M Code

> AI-powered development tool for your terminal — code with the best models, right where you work.

2M Code is a full-featured AI coding assistant that runs in your terminal, browser, or desktop. It supports **30+ LLM providers**, offers a rich **plugin system**, and integrates directly with **GitHub**, **Slack**, **VS Code**, and **Zed**.

---

## Features

- **Multi-Provider AI** — Use Anthropic, OpenAI, Google Gemini, DeepSeek, Groq, Mistral, Amazon Bedrock, Azure, OpenRouter, Perplexity, xAI, Together AI, Groq, Cerebras, Cohere, Nvidia NIM, Cloudflare, SAP AI Core, Venice, Kilo, Zenmux, LLMGateway, and more — all through a unified interface.
- **Agent Mode** — Autonomous coding agent with tool calling: file search, web search, shell commands, code execution, image generation, and GitHub PR review.
- **Rich Terminal UI** — Beautiful TUI built with OpenTUI for interactive sessions.
- **Web & Desktop** — Full-featured SolidJS web app and Electron desktop app with code editing, diff viewer, syntax highlighting, and drag-and-drop.
- **Plugin System** — Extend 2M Code via `@2mcode-ai/plugin` SDK. Add custom providers, models, tools, and hooks.
- **MCP Support** — Model Context Protocol server for integrating external tools.
- **ACP Support** — Agent-Client Protocol for agent-to-agent communication.
- **GitHub Integration** — GitHub Action for CI/CD, PR review, issue triage, and stats.
- **Slack Bot** — Interact with 2M Code directly from Slack.
- **VS Code & Zed Extensions** — Use 2M Code inside your editor.
- **Session Management** — Persistent sessions with SQLite storage, export/import, and JSON migration.
- **Enterprise Ready** — Self-hosted deployment on Cloudflare with Stripe billing, PlanetScale database, and Honeycomb observability.
- **Skills System** — Install community skills to extend capabilities.
- **Cross-Platform** — Linux, macOS, and Windows support.

---

## Quick Install

```bash
curl -fsSL https://raw.githubusercontent.com/ArafatAhmed-2M/2MCode/main/install | bash
```

Or with a specific version:

```bash
curl -fsSL https://raw.githubusercontent.com/ArafatAhmed-2M/2MCode/main/install | bash -s -- --version 1.15.0
```

### From source

```bash
# Prerequisites: Bun 1.3+
bun install
bun run build:local
bun run install:global
```

### Other install methods

- **Homebrew** (coming soon)
- **npm** (coming soon)
- **Windows**: Download from [Releases](https://github.com/ArafatAhmed-2M/2MCode/releases)

---

## Quick Start

1. **Set your API key**

   ```bash
   export ANTHROPIC_API_KEY=sk-ant-...
   # or OPENAI_API_KEY, GEMINI_API_KEY, etc.
   ```

2. **Run 2M Code in your project**

   ```bash
   cd your-project
   2mcode
   ```

3. **Use commands**

   ```bash
   2mcode run "explain the architecture"
   2mcode generate "create a React component for a data table"
   2mcode agent "fix the bugs in src/"
   2mcode pr review
   2mcode models           # List available models
   2mcode providers        # List configured providers
   ```

---

## Configuration

Copy `.env.example` to `.env` and configure your preferred provider:

```bash
cp .env.example .env
```

Key environment variables:

| Variable | Description |
|---|---|
| `2MCODE_PROVIDER` | Default provider (anthropic, openai, gemini, etc.) |
| `2MCODE_MODEL` | Default model override |
| `ANTHROPIC_API_KEY` | API key for Anthropic |
| `OPENAI_API_KEY` | API key for OpenAI |
| `GEMINI_API_KEY` | API key for Google Gemini |
| `2MCODE_MAX_TURNS` | Max conversation turns (default: 50) |
| `2MCODE_PERMISSION_MODE` | Permission mode (default, accept, off) |

---

## Architecture

```
2MCODE/
├── packages/
│   ├── 2mcode/          # Main CLI tool (entry point)
│   ├── core/            # Shared core library (providers, sessions, plugins)
│   ├── app/             # Web application (SolidJS + Vite)
│   ├── desktop/         # Desktop app (Electron)
│   ├── ui/              # Shared UI component library (SolidJS)
│   ├── plugin/          # External plugin SDK
│   ├── sdk/js/          # JavaScript SDK
│   ├── llm/             # LLM protocol layer
│   ├── web/             # Marketing/docs site (Astro + Starlight)
│   ├── slack/           # Slack bot integration
│   ├── docs/            # Documentation content (Mintlify)
│   ├── function/        # Cloudflare Workers
│   ├── enterprise/      # Self-hosted enterprise deployment
│   ├── console/         # Admin console
│   ├── storybook/       # UI component storybook
│   ├── extensions/      # Editor extensions (Zed)
│   ├── script/          # Shared build/utility scripts
│   ├── containers/      # Docker/container definitions
│   └── identity/        # Branding assets
├── sdks/
│   └── vscode/          # VS Code extension
├── infra/               # Infrastructure (SST on Cloudflare)
├── github/              # GitHub Action
└── specs/               # API specifications
```

---

## Development

```bash
# Install dependencies
bun install

# Start the CLI in dev mode
bun run dev

# Start the web app
bun run dev:web

# Start the desktop app
bun run dev:desktop

# Lint
bun run lint

# Typecheck
bun run typecheck
```

See [Development Guide](CONTRIBUTING.md) for more details.

---

## Extending 2M Code

### Plugins

2M Code has a powerful plugin system. Create plugins with the `@2mcode-ai/plugin` SDK:

```bash
bun add @2mcode-ai/plugin
```

### Skills

Install community skills:

```bash
git clone https://github.com/ArafatAhmed-2M/skills.git ~/.2mcode/skills
```

---

## Supported LLM Providers

| Provider | Package |
|---|---|
| Anthropic | `@ai-sdk/anthropic` |
| OpenAI | `@ai-sdk/openai` |
| Google Gemini | `@ai-sdk/google` |
| Google Vertex AI | `@ai-sdk/google-vertex` |
| Amazon Bedrock | `@ai-sdk/amazon-bedrock` |
| Azure OpenAI | `@ai-sdk/azure` |
| DeepSeek | `@ai-sdk/openai-compatible` |
| Groq | `@ai-sdk/groq` |
| Mistral | `@ai-sdk/mistral` |
| Perplexity | `@ai-sdk/perplexity` |
| xAI | `@ai-sdk/xai` |
| Together AI | `@ai-sdk/togetherai` |
| OpenRouter | `@openrouter/ai-sdk-provider` |
| Cerebras | `@ai-sdk/cerebras` |
| Cohere | `@ai-sdk/cohere` |
| DeepInfra | `@ai-sdk/deepinfra` |
| Alibaba | `@ai-sdk/alibaba` |
| Cloudflare | `@ai-sdk/gateway` |
| Nvidia NIM | `@ai-sdk/openai-compatible` |
| SAP AI Core | `@ai-sdk/openai-compatible` |
| Venice | `venice-ai-sdk-provider` |
| Kilo | `@ai-sdk/openai-compatible` |
| Zenmux | `@ai-sdk/openai-compatible` |
| LLMGateway | `@ai-sdk/gateway` |
| GitLab AI | `gitlab-ai-provider` |
| Ollama | Local (no key needed) |
| LM Studio | Local (no key needed) |

---

## CLI Commands

| Command | Description |
|---|---|
| `2mcode` | Start interactive session |
| `2mcode run <prompt>` | Run a prompt and exit |
| `2mcode generate <prompt>` | Generate code from a prompt |
| `2mcode agent <task>` | Run autonomous agent mode |
| `2mcode serve` | Start HTTP API server |
| `2mcode mcp` | MCP server mode |
| `2mcode github <action>` | GitHub integration commands |
| `2mcode pr` | PR management commands |
| `2mcode session` | Session management |
| `2mcode models` | List available models |
| `2mcode providers` | List configured providers |
| `2mcode debug` | Debug and diagnostics |
| `2mcode stats` | Usage statistics |
| `2mcode upgrade` | Self-update |
| `2mcode uninstall` | Remove 2M Code |
| `2mcode web` | Open web UI |
| `2mcode account` | Account settings |
| `2mcode acp` | Agent-Client Protocol mode |
| `2mcode plug` | Plugin management |

---

## License

MIT © 2025 2M_CODE

---

## Links

- [GitHub](https://github.com/ArafatAhmed-2M/2MCode)
- [Releases](https://github.com/ArafatAhmed-2M/2MCode/releases)
- [Issues](https://github.com/ArafatAhmed-2M/2MCode/issues)
