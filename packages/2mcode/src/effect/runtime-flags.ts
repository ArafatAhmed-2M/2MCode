import { Config, ConfigProvider, Context, Effect, Layer } from "effect"
import { ConfigService } from "@/effect/config-service"

const bool = (name: string) => Config.boolean(name).pipe(Config.withDefault(false))
const positiveInteger = (name: string) =>
  Config.number(name).pipe(
    Config.map((value) => (Number.isInteger(value) && value > 0 ? value : undefined)),
    Config.orElse(() => Config.succeed(undefined)),
  )
const experimental = bool("_2MCODE_EXPERIMENTAL")
const enabledByExperimental = (name: string) =>
  Config.all({ experimental, enabled: bool(name) }).pipe(Config.map((flags) => flags.experimental || flags.enabled))

export class Service extends ConfigService.Service<Service>()("@2M_CODE/RuntimeFlags", {
  autoShare: bool("_2MCODE_AUTO_SHARE"),
  pure: bool("_2MCODE_PURE"),
  disableDefaultPlugins: bool("_2MCODE_DISABLE_DEFAULT_PLUGINS"),
  disableChannelDb: bool("_2MCODE_DISABLE_CHANNEL_DB"),
  disableEmbeddedWebUi: bool("_2MCODE_DISABLE_EMBEDDED_WEB_UI"),
  disableExternalSkills: bool("_2MCODE_DISABLE_EXTERNAL_SKILLS"),
  disableLspDownload: bool("_2MCODE_DISABLE_LSP_DOWNLOAD"),
  skipMigrations: bool("_2MCODE_SKIP_MIGRATIONS"),
  disableClaudeCodePrompt: Config.all({
    broad: bool("_2MCODE_DISABLE_CLAUDE_CODE"),
    direct: bool("_2MCODE_DISABLE_CLAUDE_CODE_PROMPT"),
  }).pipe(Config.map((flags) => flags.broad || flags.direct)),
  disableClaudeCodeSkills: Config.all({
    broad: bool("_2MCODE_DISABLE_CLAUDE_CODE"),
    direct: bool("_2MCODE_DISABLE_CLAUDE_CODE_SKILLS"),
  }).pipe(Config.map((flags) => flags.broad || flags.direct)),
  enableExa: Config.all({
    experimental,
    enabled: bool("_2MCODE_ENABLE_EXA"),
    legacy: bool("_2MCODE_EXPERIMENTAL_EXA"),
  }).pipe(Config.map((flags) => flags.experimental || flags.enabled || flags.legacy)),
  enableParallel: Config.all({
    enabled: bool("_2MCODE_ENABLE_PARALLEL"),
    legacy: bool("_2MCODE_EXPERIMENTAL_PARALLEL"),
  }).pipe(Config.map((flags) => flags.enabled || flags.legacy)),
  enableExperimentalModels: bool("_2MCODE_ENABLE_EXPERIMENTAL_MODELS"),
  enableQuestionTool: bool("_2MCODE_ENABLE_QUESTION_TOOL"),
  experimentalScout: enabledByExperimental("_2MCODE_EXPERIMENTAL_SCOUT"),
  experimentalBackgroundSubagents: enabledByExperimental("_2MCODE_EXPERIMENTAL_BACKGROUND_SUBAGENTS"),
  experimentalLspTy: bool("_2MCODE_EXPERIMENTAL_LSP_TY"),
  experimentalLspTool: enabledByExperimental("_2MCODE_EXPERIMENTAL_LSP_TOOL"),
  experimentalOxfmt: enabledByExperimental("_2MCODE_EXPERIMENTAL_OXFMT"),
  experimentalPlanMode: enabledByExperimental("_2MCODE_EXPERIMENTAL_PLAN_MODE"),
  experimentalEventSystem: enabledByExperimental("_2MCODE_EXPERIMENTAL_EVENT_SYSTEM"),
  experimentalWorkspaces: enabledByExperimental("_2MCODE_EXPERIMENTAL_WORKSPACES"),
  experimentalIconDiscovery: enabledByExperimental("_2MCODE_EXPERIMENTAL_ICON_DISCOVERY"),
  outputTokenMax: positiveInteger("_2MCODE_EXPERIMENTAL_OUTPUT_TOKEN_MAX"),
  bashDefaultTimeoutMs: positiveInteger("_2MCODE_EXPERIMENTAL_BASH_DEFAULT_TIMEOUT_MS"),
  client: Config.string("_2MCODE_CLIENT").pipe(Config.withDefault("cli")),
}) {}

export type Info = Context.Service.Shape<typeof Service>

const emptyConfigLayer = Service.defaultLayer.pipe(
  Layer.provide(ConfigProvider.layer(ConfigProvider.fromUnknown({}))),
  Layer.orDie,
)

export const layer = (overrides: Partial<Info> = {}) =>
  Layer.effect(
    Service,
    Effect.gen(function* () {
      const flags = yield* Service
      return Service.of({ ...flags, ...overrides })
    }),
  ).pipe(Layer.provide(emptyConfigLayer))

export const defaultLayer = Service.defaultLayer.pipe(Layer.orDie)

export * as RuntimeFlags from "./runtime-flags"
