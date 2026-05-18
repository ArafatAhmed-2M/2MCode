# Contributing to 2M Code

Thank you for your interest in contributing to 2M Code! We welcome contributions from everyone.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Project Structure](#project-structure)
- [Coding Guidelines](#coding-guidelines)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting](#issue-reporting)

---

## Code of Conduct

This project and everyone participating in it is governed by the [2M Code Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

---

## Getting Started

### Prerequisites

- [Bun](https://bun.sh) 1.3.13+
- Node.js 22+
- Git

### Setup

1. Fork and clone the repository:

   ```bash
   git clone https://github.com/your-username/2MCode.git
   cd 2MCode
   ```

2. Install dependencies:

   ```bash
   bun install
   ```

3. Create a `.env` file:

   ```bash
   cp .env.example .env
   # Add your API key(s)
   ```

4. Start developing:

   ```bash
   bun run dev
   ```

---

## Development Workflow

### Branch Naming

- `feature/<description>` — New features
- `fix/<description>` — Bug fixes
- `docs/<description>` — Documentation changes
- `refactor/<description>` — Code refactoring
- `chore/<description>` — Maintenance tasks

### Commit Messages

We use conventional commits:

```
<type>(<scope>): <description>

[optional body]
```

Types: `feat`, `fix`, `docs`, `refactor`, `perf`, `test`, `chore`, `style`

### Running the CLI in Dev Mode

```bash
bun run dev
```

### Running the Web App

```bash
bun run dev:web
```

### Running the Desktop App

```bash
bun run dev:desktop
```

### Linting

```bash
bun run lint
```

### Type Checking

```bash
bun run typecheck
```

### Testing

```bash
# From the root (run tests in specific packages)
bun run --cwd packages/2mcode test

# Run E2E tests (playwright)
bun run --cwd packages/app test:e2e
```

---

## Project Structure

The monorepo uses Turborepo for orchestration. Key packages:

| Directory | Description |
|---|---|
| `packages/2mcode/` | CLI tool (entry point) |
| `packages/core/` | Shared core library |
| `packages/app/` | Web application |
| `packages/desktop/` | Electron desktop app |
| `packages/ui/` | Shared UI components |
| `packages/plugin/` | Plugin SDK |
| `packages/sdk/` | JavaScript SDK |
| `packages/llm/` | LLM protocol layer |
| `packages/web/` | Marketing website |
| `packages/slack/` | Slack integration |
| `sdks/vscode/` | VS Code extension |

---

## Coding Guidelines

- **Language**: TypeScript (strict mode)
- **Functional**: We use the [Effect](https://effect.website) library for type-safe effects. New code should follow existing patterns.
- **Style**: No semicolons, 120 character line width (Prettier enforced)
- **Imports**: Use `workspace:*` protocol for internal packages
- **UI**: SolidJS components with Tailwind CSS
- **Schema**: Use Zod for runtime validation
- **No comments in code** unless absolutely necessary — let the code speak

---

## Testing

- Unit tests use Bun's built-in test runner (`bun test`)
- E2E tests use Playwright
- HTTP API tests verify provider integrations
- Run tests before submitting a PR

```bash
bun run --cwd packages/2mcode test
```

---

## Pull Request Process

1. Create a feature branch from `main`
2. Make your changes
3. Run linting and type checking:

   ```bash
   bun run lint
   bun run typecheck
   ```

4. Write or update tests as needed
5. Open a pull request to `main`
6. Ensure CI passes
7. Request review from maintainers

### PR Checklist

- [ ] Branch is up to date with `main`
- [ ] Linting passes (`bun run lint`)
- [ ] Type checking passes (`bun run typecheck`)
- [ ] Tests pass
- [ ] New features include tests
- [ ] Documentation updated if needed
- [ ] Changeset added (if applicable)

---

## Issue Reporting

- Check existing issues before opening a new one
- Use the issue templates if available
- Include steps to reproduce for bugs
- Include relevant logs, screenshots, or error messages

---

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).
