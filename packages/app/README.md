# 2M Code — Web App

Shared web UI components for 2M Code, built with SolidJS.

## Development

Start the backend server first, then the app:

```bash
# Terminal 1 — Backend (from packages/2mcode)
bun run --conditions=browser ./src/index.ts serve --port 4096

# Terminal 2 — App (from packages/app)
bun dev -- --port 4444
```

Open `http://localhost:4444` to verify UI changes (it targets the backend at `http://localhost:4096`).

## Commands

| Command               | Description                                        |
| --------------------- | -------------------------------------------------- |
| `bun dev`             | Start development server at `localhost:4444`       |
| `bun run build`       | Build for production to `dist/`                    |
| `bun run test:e2e:local` | Run Playwright e2e tests                       |

## E2E Testing

Playwright starts the Vite dev server automatically via `webServer`, and UI tests expect a 2M Code backend at `localhost:4096` by default.

```bash
bunx playwright install chromium
bun run test:e2e:local
bun run test:e2e:local -- --grep "settings"
```

### Environment Options

- `PLAYWRIGHT_SERVER_HOST` / `PLAYWRIGHT_SERVER_PORT` — backend address (default: `localhost:4096`)
- `PLAYWRIGHT_PORT` — Vite dev server port (default: `3000`)
- `PLAYWRIGHT_BASE_URL` — override base URL (default: `http://localhost:<PLAYWRIGHT_PORT>`)

## Deployment

Deploy the `dist/` folder to any static host provider (Netlify, Surge, Vercel, etc.).
