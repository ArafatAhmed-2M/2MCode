import { Effect } from "effect"
import { PluginV2 } from "../../plugin"
import { ProviderV2 } from "../../provider"

export const LLMGatewayPlugin = PluginV2.define({
  id: PluginV2.ID.make("llmgateway"),
  effect: Effect.gen(function* () {
    return {
      "provider.update": Effect.fn(function* (evt) {
        if (evt.provider.id !== ProviderV2.ID.make("llmgateway")) return
        if (evt.provider.enabled === false) return
        evt.provider.options.headers["HTTP-Referer"] = "https://2M_CODE.ai/"
        evt.provider.options.headers["X-Title"] = "2M_CODE"
        evt.provider.options.headers["X-Source"] = "2M_CODE"
      }),
    }
  }),
})
