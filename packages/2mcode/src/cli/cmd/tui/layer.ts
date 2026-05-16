import { Layer } from "effect"
import { TuiConfig } from "./config/tui"
import { Npm } from "@2mcode-ai/core/npm"
import { Observability } from "@2mcode-ai/core/effect/observability"

export const CliLayer = Observability.layer.pipe(Layer.merge(TuiConfig.layer), Layer.provide(Npm.defaultLayer))
