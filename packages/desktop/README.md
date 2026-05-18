# 2M Code — Desktop App

The 2M Code Desktop app, built with Electron.

## Development

```bash
bun install
bun dev
```

## Build

Run `build` to compile the app's JS assets, then `package` to bundle into a distributable application.

```bash
bun run build
bun run package
```

The packaged app will be in `dist/`.

> [!TIP]
> For production builds, run `bun run build && bun run package` sequentially.
