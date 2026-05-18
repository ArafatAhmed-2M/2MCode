<p align="center">

```
██████╗ ███╗   ███╗     ██████╗ ██████╗ ██████╗ ███████╗
╚════██╗████╗ ████║    ██╔════╝██╔═══██╗██╔══██╗██╔════╝
 █████╔╝██╔████╔██║    ██║     ██║   ██║██║  ██║█████╗  
██╔═══╝ ██║╚██╔╝██║    ██║     ██║   ██║██║  ██║██╔══╝  
███████╗██║ ╚═╝ ██║    ╚██████╗╚██████╔╝██████╔╝███████╗
╚══════╝╚═╝     ╚═╝     ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝
```

</p>
<p align="center">The advanced, custom AI engineering assistant.</p>
<p align="center">
  <a href="https://github.com/ArafatAhmed-2M/2MCode"><img alt="GitHub" src="https://img.shields.io/badge/github-2MCode-blue?style=flat-square" /></a>
  <a href="https://github.com/ArafatAhmed-2M/2MCode/releases"><img alt="Release" src="https://img.shields.io/github/v/release/ArafatAhmed-2M/2MCode?style=flat-square" /></a>
  <a href="https://github.com/ArafatAhmed-2M/2MCode/actions"><img alt="Build status" src="https://img.shields.io/github/actions/workflow/status/ArafatAhmed-2M/2MCode/publish.yml?style=flat-square&branch=main" /></a>
</p>

<p align="center">
  <a href="README.md">English</a> |
  <a href="README.zh.md">简体中文</a> |
  <a href="README.zht.md">繁體中文</a> |
  <a href="README.ko.md">한국어</a> |
  <a href="README.de.md">Deutsch</a> |
  <a href="README.es.md">Español</a> |
  <a href="README.fr.md">Français</a> |
  <a href="README.it.md">Italiano</a> |
  <a href="README.da.md">Dansk</a> |
  <a href="README.ja.md">日本語</a> |
  <a href="README.pl.md">Polski</a> |
  <a href="README.ru.md">Русский</a> |
  <a href="README.bs.md">Bosanski</a> |
  <a href="README.ar.md">العربية</a> |
  <a href="README.no.md">Norsk</a> |
  <a href="README.br.md">Português (Brasil)</a> |
  <a href="README.th.md">ไทย</a> |
  <a href="README.tr.md">Türkçe</a> |
  <a href="README.uk.md">Українська</a> |
  <a href="README.bn.md">বাংলা</a> |
  <a href="README.gr.md">Ελληνικά</a> |
  <a href="README.vi.md">Tiếng Việt</a>
</p>

---

### Installation

#### Global Install from Source (Recommended for Developers & Customization)

If you have cloned this repository, you can compile an optimized, native self-contained TUI executable and register it globally in your system path with a single command:

```bash
# 1. Install dependencies
bun install

# 2. Compile native binary and register it globally in PATH
bun run install:global
```

* **Windows**: Compiles `2mcode.exe` and installs it to `~/.local/bin`, adding it to your user registry `PATH`.
  > [!TIP]
  > **Note for Windows Users:** You must restart your terminal or reload environment variables in your current PowerShell session for the `2mcode` command to be recognized:
  > `$env:Path = [System.Environment]::GetEnvironmentVariable("Path", "User") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "Machine")`
* **macOS / Linux**: Compiles `2mcode` and installs it to `~/.local/bin/2mcode`, automatically appending the folder to your shell profile (`.zshrc`, `.bashrc`, etc.) if not already present.

---

#### Quick Package & Binary Installation

```bash
# Quick install script (macOS & Linux)
curl -fsSL https://raw.githubusercontent.com/ArafatAhmed-2M/2MCode/main/install | bash

# npm / bun / pnpm
npm i -g 2mcode@latest
bun add -g 2mcode
pnpm add -g 2mcode

# Windows (Scoop)
scoop install 2mcode

# macOS / Linux (Homebrew)
brew install ArafatAhmed-2M/tap/2mcode

# Arch Linux
paru -S 2mcode-bin
```

> [!TIP]
> After install, simply type `2mcode` in any project directory to start.

### Desktop App (BETA)

2M Code is also available as a desktop application. Download directly from the [releases page](https://github.com/ArafatAhmed-2M/2MCode/releases).

| Platform              | Download                              |
| --------------------- | ------------------------------------- |
| macOS (Apple Silicon) | `2mcode-desktop-mac-arm64.dmg`        |
| macOS (Intel)         | `2mcode-desktop-mac-x64.dmg`          |
| Windows               | `2mcode-desktop-windows-x64.exe`      |
| Linux                 | `.deb`, `.rpm`, or `.AppImage`        |

#### Installation Directory

The install script uses the following priority for the installation path:

1. `$_2MCODE_INSTALL_DIR` - Custom installation directory
2. `$XDG_BIN_DIR` - XDG Base Directory Specification compliant path
3. `$HOME/bin` - Standard user binary directory
4. `$HOME/.2mcode/bin` - Default fallback

```bash
# Custom install dir example
_2MCODE_INSTALL_DIR=/usr/local/bin curl -fsSL https://raw.githubusercontent.com/ArafatAhmed-2M/2MCode/main/install | bash
```

### Agents

2M Code includes two built-in agents you can switch between with the `Tab` key.

- **build** - Default, full-access agent for development work
- **plan** - Read-only agent for analysis and code exploration
  - Denies file edits by default
  - Asks permission before running bash commands
  - Ideal for exploring unfamiliar codebases or planning changes

Also included is a **general** subagent for complex searches and multistep tasks.
This is used internally and can be invoked using `@general` in messages.

### Documentation

For more info on how to configure 2M Code, [**head over to our docs**](https://github.com/ArafatAhmed-2M/2MCode/wiki).

### Contributing

If you're interested in contributing to 2M Code, please read our [contributing docs](./CONTRIBUTING.md) before submitting a pull request.

### Building on 2M Code

If you are working on a project that's related to 2M Code and is using "2M Code" as part of its name, please add a note to your README to clarify that it is not built by the 2M Code team and is not affiliated with us.

### FAQ

#### How is this different from Claude Code?

It's very similar to Claude Code in terms of capability. Here are the key differences:

- 100% open source
- Not coupled to any provider — 2M Code works with Claude, OpenAI, Google, or local models
- Built-in opt-in LSP support
- A focus on TUI — built by terminal enthusiasts, pushing the limits of what's possible in the terminal
- A client/server architecture — 2M Code can run on your computer while you drive it remotely

---

**Join our community** [GitHub](https://github.com/ArafatAhmed-2M/2MCode)
