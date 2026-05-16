import { Config } from "effect"

function truthy(key: string) {
  const value = process.env[key]?.toLowerCase()
  return value === "true" || value === "1"
}

const 2M_CODE_EXPERIMENTAL = truthy("2M_CODE_EXPERIMENTAL")
const copy = process.env["2M_CODE_EXPERIMENTAL_DISABLE_COPY_ON_SELECT"]

export const Flag = {
  OTEL_EXPORTER_OTLP_ENDPOINT: process.env["OTEL_EXPORTER_OTLP_ENDPOINT"],
  OTEL_EXPORTER_OTLP_HEADERS: process.env["OTEL_EXPORTER_OTLP_HEADERS"],

  2M_CODE_AUTO_HEAP_SNAPSHOT: truthy("2M_CODE_AUTO_HEAP_SNAPSHOT"),
  2M_CODE_GIT_BASH_PATH: process.env["2M_CODE_GIT_BASH_PATH"],
  2M_CODE_CONFIG: process.env["2M_CODE_CONFIG"],
  2M_CODE_CONFIG_CONTENT: process.env["2M_CODE_CONFIG_CONTENT"],
  2M_CODE_DISABLE_AUTOUPDATE: truthy("2M_CODE_DISABLE_AUTOUPDATE"),
  2M_CODE_ALWAYS_NOTIFY_UPDATE: truthy("2M_CODE_ALWAYS_NOTIFY_UPDATE"),
  2M_CODE_DISABLE_PRUNE: truthy("2M_CODE_DISABLE_PRUNE"),
  2M_CODE_DISABLE_TERMINAL_TITLE: truthy("2M_CODE_DISABLE_TERMINAL_TITLE"),
  2M_CODE_SHOW_TTFD: truthy("2M_CODE_SHOW_TTFD"),
  2M_CODE_PERMISSION: process.env["2M_CODE_PERMISSION"],
  2M_CODE_DISABLE_AUTOCOMPACT: truthy("2M_CODE_DISABLE_AUTOCOMPACT"),
  2M_CODE_DISABLE_MODELS_FETCH: truthy("2M_CODE_DISABLE_MODELS_FETCH"),
  2M_CODE_DISABLE_MOUSE: truthy("2M_CODE_DISABLE_MOUSE"),
  2M_CODE_FAKE_VCS: process.env["2M_CODE_FAKE_VCS"],
  2M_CODE_SERVER_PASSWORD: process.env["2M_CODE_SERVER_PASSWORD"],
  2M_CODE_SERVER_USERNAME: process.env["2M_CODE_SERVER_USERNAME"],

  // Experimental
  2M_CODE_EXPERIMENTAL_FILEWATCHER: Config.boolean("2M_CODE_EXPERIMENTAL_FILEWATCHER").pipe(
    Config.withDefault(false),
  ),
  2M_CODE_EXPERIMENTAL_DISABLE_FILEWATCHER: Config.boolean("2M_CODE_EXPERIMENTAL_DISABLE_FILEWATCHER").pipe(
    Config.withDefault(false),
  ),
  2M_CODE_EXPERIMENTAL_DISABLE_COPY_ON_SELECT:
    copy === undefined ? process.platform === "win32" : truthy("2M_CODE_EXPERIMENTAL_DISABLE_COPY_ON_SELECT"),
  2M_CODE_MODELS_URL: process.env["2M_CODE_MODELS_URL"],
  2M_CODE_MODELS_PATH: process.env["2M_CODE_MODELS_PATH"],
  2M_CODE_DB: process.env["2M_CODE_DB"],

  2M_CODE_WORKSPACE_ID: process.env["2M_CODE_WORKSPACE_ID"],
  2M_CODE_EXPERIMENTAL_WORKSPACES: 2M_CODE_EXPERIMENTAL || truthy("2M_CODE_EXPERIMENTAL_WORKSPACES"),

  // Evaluated at access time (not module load) because tests, the CLI, and
  // external tooling set these env vars at runtime.
  get 2M_CODE_DISABLE_PROJECT_CONFIG() {
    return truthy("2M_CODE_DISABLE_PROJECT_CONFIG")
  },
  get 2M_CODE_TUI_CONFIG() {
    return process.env["2M_CODE_TUI_CONFIG"]
  },
  get 2M_CODE_CONFIG_DIR() {
    return process.env["2M_CODE_CONFIG_DIR"]
  },
  get 2M_CODE_PURE() {
    return truthy("2M_CODE_PURE")
  },
  get 2M_CODE_PLUGIN_META_FILE() {
    return process.env["2M_CODE_PLUGIN_META_FILE"]
  },
  get 2M_CODE_CLIENT() {
    return process.env["2M_CODE_CLIENT"] ?? "cli"
  },
}
