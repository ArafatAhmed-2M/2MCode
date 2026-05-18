#!/usr/bin/env bun

/**
 * install.ts — builds a native 2mcode binary and installs it globally.
 *
 * Usage:  bun run install:global   (from repo root)
 *         bun run script/install.ts  (from packages/2mcode)
 */

import { $ } from "bun"
import fs from "fs"
import os from "os"
import path from "path"
import { fileURLToPath } from "url"

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const pkgDir = path.resolve(__dirname, "..")
const platform = os.platform() // "win32" | "darwin" | "linux"
const arch = os.arch()         // "x64" | "arm64"

// ── helpers ──────────────────────────────────────────────────────────────────

function log(icon: string, msg: string) {
  console.log(`  ${icon}  ${msg}`)
}

function ok(msg: string) {
  log("✓", msg)
}

function info(msg: string) {
  log("ℹ", msg)
}

function fail(msg: string): never {
  console.error(`\n  ✗  ${msg}\n`)
  process.exit(1)
}

// ── resolve paths ─────────────────────────────────────────────────────────────

const platformLabel = platform === "win32" ? "windows" : platform
const binaryName = platform === "win32" ? "2M_CODE.exe" : "2M_CODE"
const installName = platform === "win32" ? "2mcode.exe" : "2mcode"

// Where bun build --compile puts the output
const distName = `2mcode-${platformLabel}-${arch}`
const builtBinary = path.join(pkgDir, "dist", distName, "bin", binaryName)

// Where to install (XDG / Windows convention)
const installDir =
  platform === "win32"
    ? path.join(os.homedir(), ".local", "bin")
    : path.join(os.homedir(), ".local", "bin")

const installTarget = path.join(installDir, installName)

// ── step 1: build ─────────────────────────────────────────────────────────────

console.log("\n  ┌─────────────────────────────────────────┐")
console.log("  │   2M Code — Global Install               │")
console.log("  └─────────────────────────────────────────┘\n")

info(`Building for ${platformLabel}-${arch}  (this takes ~1-2 min)…`)

try {
  // --skip-install avoids downloading cross-platform native packages (node-pty,
  // parcel/watcher for other OSes) which fail integrity checks on Windows.
  await $`bun run script/build.ts --single --skip-embed-web-ui --skip-install`.cwd(pkgDir)
} catch {
  fail("Build failed. Check the output above for errors.")
}

if (!fs.existsSync(builtBinary)) {
  fail(`Expected binary not found at:\n     ${builtBinary}`)
}

ok(`Binary built   → ${path.relative(pkgDir, builtBinary)}`)

// ── step 2: copy binary ───────────────────────────────────────────────────────

fs.mkdirSync(installDir, { recursive: true })

// Remove stale copy if present
if (fs.existsSync(installTarget)) fs.unlinkSync(installTarget)

try {
  fs.linkSync(builtBinary, installTarget)
} catch {
  // Hard link may fail across drives; fall back to copy
  fs.copyFileSync(builtBinary, installTarget)
}

if (platform !== "win32") fs.chmodSync(installTarget, 0o755)

ok(`Installed      → ${installTarget}`)

// ── step 3: verify binary runs ───────────────────────────────────────────────

const probe = Bun.spawnSync([installTarget, "--version"], { stderr: "pipe" })
const version = probe.stdout.toString().trim()

if (probe.exitCode !== 0) {
  fail(`Binary installed but failed to run. Try:\n     ${installTarget} --version`)
}

ok(`Verified       → 2mcode ${version}`)

// ── step 4: ensure install dir is on PATH ────────────────────────────────────

const currentPath = process.env.PATH ?? ""
const onPath = currentPath.split(path.delimiter).some((p) => {
  try {
    return fs.realpathSync(p) === fs.realpathSync(installDir)
  } catch {
    return p === installDir
  }
})

if (!onPath) {
  if (platform === "win32") {
    // Add to the user PATH in the Windows registry (persists across terminals)
    info("Adding ~/.local/bin to your user PATH…")
    const ps = [
      `$p = [Environment]::GetEnvironmentVariable('PATH','User')`,
      `$d = '${installDir}'`,
      `if ($p -notlike "*$d*") {`,
      `  [Environment]::SetEnvironmentVariable('PATH', "$d;$p", 'User')`,
      `  Write-Host 'added'`,
      `} else { Write-Host 'already' }`,
    ].join("; ")

    const result = Bun.spawnSync(["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", ps], {
      stderr: "pipe",
    })
    const out = Buffer.isBuffer(result.stdout) ? result.stdout.toString("utf8").trim() : String(result.stdout ?? "").trim()
    if (result.exitCode === 0 && out === "added") {
      ok(`PATH updated   → restart your terminal, then type:  2mcode`)
    } else if (out === "already") {
      ok("PATH already contains ~/.local/bin")
    } else {
      info(`Could not auto-update PATH. Add this manually:\n\n       ${installDir}\n\n     (Settings → System → Environment Variables → PATH)`)
    }
  } else {
    // Linux / macOS: print shell-specific instructions
    const shell = process.env.SHELL ?? ""
    const rcFile = shell.includes("zsh") ? "~/.zshrc" : "~/.bashrc"
    info(`Add this line to ${rcFile}, then restart your terminal:\n\n       export PATH="$HOME/.local/bin:$PATH"\n`)
  }
} else {
  ok("PATH already up to date")
}

console.log(`\n  ─────────────────────────────────────────────`)
console.log(`   All done! Open a new terminal and type:  2mcode`)
console.log(`  ─────────────────────────────────────────────\n`)
