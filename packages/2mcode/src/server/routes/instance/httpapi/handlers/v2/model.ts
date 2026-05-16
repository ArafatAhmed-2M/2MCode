import { Catalog } from "@2M_CODE-ai/core/catalog"
import { PluginBoot } from "@2M_CODE-ai/core/plugin/boot"
import { Effect } from "effect"
import { HttpApiBuilder } from "effect/unstable/httpapi"
import { InstanceHttpApi } from "../../api"

export const modelHandlers = HttpApiBuilder.group(InstanceHttpApi, "v2.model", (handlers) =>
  Effect.gen(function* () {
    return handlers.handle(
      "models",
      Effect.fn(function* () {
        const catalog = yield* Catalog.Service
        const pluginBoot = yield* PluginBoot.Service
        yield* pluginBoot.wait()
        return yield* catalog.model.available()
      }),
    )
  }),
)
