# 2M_CODE VS Code Extension

A Visual Studio Code extension that integrates [2M_CODE](https://2M_CODE.ai) directly into your development workflow.

## Prerequisites

This extension requires the [2M_CODE CLI](https://2M_CODE.ai) to be installed on your system. Visit [2M_CODE.ai](https://2M_CODE.ai) for installation instructions.

## Features

- **Quick Launch**: Use `Cmd+Esc` (Mac) or `Ctrl+Esc` (Windows/Linux) to open 2M_CODE in a split terminal view, or focus an existing terminal session if one is already running.
- **New Session**: Use `Cmd+Shift+Esc` (Mac) or `Ctrl+Shift+Esc` (Windows/Linux) to start a new 2M_CODE terminal session, even if one is already open. You can also click the 2M_CODE button in the UI.
- **Context Awareness**: Automatically share your current selection or tab with 2M_CODE.
- **File Reference Shortcuts**: Use `Cmd+Option+K` (Mac) or `Alt+Ctrl+K` (Linux/Windows) to insert file references. For example, `@File#L37-42`.

## Support

This is an early release. If you encounter issues or have feedback, please create an issue at https://github.com/ArafatAhmed-2M/2mcode/issues.

## Development

1. `code sdks/vscode` - Open the `sdks/vscode` directory in VS Code. **Do not open from repo root.**
2. `bun install` - Run inside the `sdks/vscode` directory.
3. Press `F5` to start debugging - This launches a new VS Code window with the extension loaded.

#### Making Changes

`tsc` and `esbuild` watchers run automatically during debugging (visible in the Terminal tab). Changes to the extension are automatically rebuilt in the background.

To test your changes:

1. In the debug VS Code window, press `Cmd+Shift+P`
2. Search for `Developer: Reload Window`
3. Reload to see your changes without restarting the debug session
