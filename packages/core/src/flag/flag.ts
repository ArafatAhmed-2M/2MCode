import { Config } from "effect"

function truthy(key: string) {
  const value = process.env[key]?.toLowerCase()
  return value === "true" || value === "1"
}

const _2MCODE_EXPERIMENTAL = truthy("_2MCODE_EXPERIMENTAL")
const copy = process.env["_2MCODE_EXPERIMENTAL_DISABLE_COPY_ON_SELECT"]

export const Flag = {
  OTEL_EXPORTER_OTLP_ENDPOINT: process.env["OTEL_EXPORTER_OTLP_ENDPOINT"],
  OTEL_EXPORTER_OTLP_HEADERS: process.env["OTEL_EXPORTER_OTLP_HEADERS"],

  _2MCODE_AUTO_HEAP_SNAPSHOT: truthy("_2MCODE_AUTO_HEAP_SNAPSHOT"),
  _2MCODE_GIT_BASH_PATH: process.env["_2MCODE_GIT_BASH_PATH"],
  _2MCODE_CONFIG: process.env["_2MCODE_CONFIG"],
  _2MCODE_CONFIG_CONTENT: process.env["_2MCODE_CONFIG_CONTENT"],
  _2MCODE_DISABLE_AUTOUPDATE: truthy("_2MCODE_DISABLE_AUTOUPDATE"),
  _2MCODE_ALWAYS_NOTIFY_UPDATE: truthy("_2MCODE_ALWAYS_NOTIFY_UPDATE"),
  _2MCODE_DISABLE_PRUNE: truthy("_2MCODE_DISABLE_PRUNE"),
  _2MCODE_DISABLE_TERMINAL_TITLE: truthy("_2MCODE_DISABLE_TERMINAL_TITLE"),
  _2MCODE_SHOW_TTFD: truthy("_2MCODE_SHOW_TTFD"),
  _2MCODE_PERMISSION: process.env["_2MCODE_PERMISSION"],
  _2MCODE_DISABLE_AUTOCOMPACT: truthy("_2MCODE_DISABLE_AUTOCOMPACT"),
  _2MCODE_DISABLE_MODELS_FETCH: truthy("_2MCODE_DISABLE_MODELS_FETCH"),
  _2MCODE_DISABLE_MOUSE: truthy("_2MCODE_DISABLE_MOUSE"),
  _2MCODE_FAKE_VCS: process.env["_2MCODE_FAKE_VCS"],
  _2MCODE_SERVER_PASSWORD: process.env["_2MCODE_SERVER_PASSWORD"],
  _2MCODE_SERVER_USERNAME: process.env["_2MCODE_SERVER_USERNAME"],

  // Experimental
  _2MCODE_EXPERIMENTAL_FILEWATCHER: Config.boolean("_2MCODE_EXPERIMENTAL_FILEWATCHER").pipe(
    Config.withDefault(false),
  ),
  _2MCODE_EXPERIMENTAL_DISABLE_FILEWATCHER: Config.boolean("_2MCODE_EXPERIMENTAL_DISABLE_FILEWATCHER").pipe(
    Config.withDefault(false),
  ),
  _2MCODE_EXPERIMENTAL_DISABLE_COPY_ON_SELECT:
    copy === undefined ? process.platform === "win32" : truthy("_2MCODE_EXPERIMENTAL_DISABLE_COPY_ON_SELECT"),
  _2MCODE_MODELS_URL: process.env["_2MCODE_MODELS_URL"],
  _2MCODE_MODELS_PATH: process.env["_2MCODE_MODELS_PATH"],
  _2MCODE_DB: process.env["_2MCODE_DB"],

  _2MCODE_WORKSPACE_ID: process.env["_2MCODE_WORKSPACE_ID"],
  _2MCODE_EXPERIMENTAL_WORKSPACES: _2MCODE_EXPERIMENTAL || truthy("_2MCODE_EXPERIMENTAL_WORKSPACES"),

  // Evaluated at access time (not module load) because tests, the CLI, and
  // external tooling set these env vars at runtime.
  get _2MCODE_DISABLE_PROJECT_CONFIG() {
    return truthy("_2MCODE_DISABLE_PROJECT_CONFIG")
  },
  get _2MCODE_TUI_CONFIG() {
    return process.env["_2MCODE_TUI_CONFIG"]
  },
  get _2MCODE_CONFIG_DIR() {
    return process.env["_2MCODE_CONFIG_DIR"]
  },
  get _2MCODE_PURE() {
    return truthy("_2MCODE_PURE")
  },
  get _2MCODE_PLUGIN_META_FILE() {
    return process.env["_2MCODE_PLUGIN_META_FILE"]
  },
  get _2MCODE_CLIENT() {
    return process.env["_2MCODE_CLIENT"] ?? "cli"
  },
}
