import { describe, expect } from "bun:test"
import { DateTime, Effect, Layer, Option } from "effect"
import { Catalog } from "@2mcode-ai/core/catalog"
import { Location } from "@2mcode-ai/core/location"
import { ModelV2 } from "@2mcode-ai/core/model"
import { PluginV2 } from "@2mcode-ai/core/plugin"
import { _2MCodePlugin } from "@2mcode-ai/core/plugin/provider/2mcode"
import { ProviderV2 } from "@2mcode-ai/core/provider"
import { it, model, provider, withEnv } from "./provider-helper"

const cost = (input: number, output = 0) => [{ input, output, cache: { read: 0, write: 0 } }]
const locationLayer = Layer.succeed(Location.Service, Location.Service.of({ directory: "test" }))

describe("_2MCodePlugin", () => {
  it.effect("uses a public key and cancels paid models without credentials", () =>
    withEnv({ _2MCODE_API_KEY: undefined }, () =>
      Effect.gen(function* () {
        const plugin = yield* PluginV2.Service
        yield* plugin.add(_2MCodePlugin)
        const updated = yield* plugin.trigger("provider.update", {}, { provider: provider("2M_CODE"), cancel: false })
        const paid = yield* plugin.trigger(
          "model.update",
          {},
          { model: model("2M_CODE", "paid", { cost: cost(1) }), cancel: false },
        )
        expect(updated.provider.options.aisdk.provider.apiKey).toBe("public")
        expect(paid.cancel).toBe(true)
      }),
    ),
  )

  it.effect("keeps free models without credentials", () =>
    withEnv({ _2MCODE_API_KEY: undefined }, () =>
      Effect.gen(function* () {
        const plugin = yield* PluginV2.Service
        yield* plugin.add(_2MCodePlugin)
        yield* plugin.trigger("provider.update", {}, { provider: provider("2M_CODE"), cancel: false })
        const free = yield* plugin.trigger(
          "model.update",
          {},
          { model: model("2M_CODE", "free", { cost: cost(0) }), cancel: false },
        )
        expect(free.cancel).toBe(false)
      }),
    ),
  )

  it.effect("treats output-only cost as free without credentials", () =>
    withEnv({ _2MCODE_API_KEY: undefined }, () =>
      Effect.gen(function* () {
        const plugin = yield* PluginV2.Service
        yield* plugin.add(_2MCodePlugin)
        yield* plugin.trigger("provider.update", {}, { provider: provider("2M_CODE"), cancel: false })
        const outputOnly = yield* plugin.trigger(
          "model.update",
          {},
          { model: model("2M_CODE", "output-only", { cost: cost(0, 1) }), cancel: false },
        )
        expect(outputOnly.cancel).toBe(false)
      }),
    ),
  )

  it.effect("uses _2MCODE_API_KEY as credentials", () =>
    withEnv({ _2MCODE_API_KEY: "secret" }, () =>
      Effect.gen(function* () {
        const plugin = yield* PluginV2.Service
        yield* plugin.add(_2MCodePlugin)
        const updated = yield* plugin.trigger("provider.update", {}, { provider: provider("2M_CODE"), cancel: false })
        const paid = yield* plugin.trigger(
          "model.update",
          {},
          { model: model("2M_CODE", "paid", { cost: cost(1) }), cancel: false },
        )
        expect(updated.provider.options.aisdk.provider.apiKey).toBeUndefined()
        expect(paid.cancel).toBe(false)
      }),
    ),
  )

  it.effect("uses configured provider env vars as credentials", () =>
    withEnv({ _2MCODE_API_KEY: undefined, CUSTOM_2M_CODE_API_KEY: "secret" }, () =>
      Effect.gen(function* () {
        const plugin = yield* PluginV2.Service
        yield* plugin.add(_2MCodePlugin)
        const updated = yield* plugin.trigger(
          "provider.update",
          {},
          { provider: provider("2M_CODE", { env: ["CUSTOM_2M_CODE_API_KEY"] }), cancel: false },
        )
        const paid = yield* plugin.trigger(
          "model.update",
          {},
          { model: model("2M_CODE", "paid", { cost: cost(1) }), cancel: false },
        )
        expect(updated.provider.options.aisdk.provider.apiKey).toBeUndefined()
        expect(paid.cancel).toBe(false)
      }),
    ),
  )

  it.effect("uses configured apiKey as credentials", () =>
    withEnv({ _2MCODE_API_KEY: undefined }, () =>
      Effect.gen(function* () {
        const plugin = yield* PluginV2.Service
        yield* plugin.add(_2MCodePlugin)
        const updated = yield* plugin.trigger(
          "provider.update",
          {},
          {
            provider: provider("2M_CODE", {
              options: {
                headers: {},
                body: {},
                aisdk: {
                  provider: { apiKey: "configured" },
                  request: {},
                },
              },
            }),
            cancel: false,
          },
        )
        const paid = yield* plugin.trigger(
          "model.update",
          {},
          { model: model("2M_CODE", "paid", { cost: cost(1) }), cancel: false },
        )
        expect(updated.provider.options.aisdk.provider.apiKey).toBe("configured")
        expect(paid.cancel).toBe(false)
      }),
    ),
  )

  it.effect("uses auth-enabled providers as credentials", () =>
    withEnv({ _2MCODE_API_KEY: undefined }, () =>
      Effect.gen(function* () {
        const plugin = yield* PluginV2.Service
        yield* plugin.add(_2MCodePlugin)
        const updated = yield* plugin.trigger(
          "provider.update",
          {},
          { provider: provider("2M_CODE", { enabled: { via: "auth", service: "2M_CODE" } }), cancel: false },
        )
        const paid = yield* plugin.trigger(
          "model.update",
          {},
          { model: model("2M_CODE", "paid", { cost: cost(1) }), cancel: false },
        )
        expect(updated.provider.options.aisdk.provider.apiKey).toBeUndefined()
        expect(paid.cancel).toBe(false)
      }),
    ),
  )

  it.effect("ignores non-2M_CODE providers and models", () =>
    withEnv({ _2MCODE_API_KEY: undefined }, () =>
      Effect.gen(function* () {
        const plugin = yield* PluginV2.Service
        yield* plugin.add(_2MCodePlugin)
        const updated = yield* plugin.trigger("provider.update", {}, { provider: provider("openai"), cancel: false })
        const paid = yield* plugin.trigger(
          "model.update",
          {},
          { model: model("openai", "paid", { cost: cost(1) }), cancel: false },
        )
        expect(updated.provider.options.aisdk.provider.apiKey).toBeUndefined()
        expect(paid.cancel).toBe(false)
      }),
    ),
  )

  it.effect("prefers gpt-5-nano as the 2M_CODE small model", () =>
    Effect.gen(function* () {
      const catalog = yield* Catalog.Service
      const providerID = ProviderV2.ID["2M_CODE"]

      yield* catalog.provider.update(providerID, () => {})
      yield* catalog.model.update(providerID, ModelV2.ID.make("cheap-mini"), (model) => {
        model.capabilities.input = ["text"]
        model.capabilities.output = ["text"]
        model.cost = cost(1, 1)
        model.time.released = DateTime.makeUnsafe(Date.now())
      })
      yield* catalog.model.update(providerID, ModelV2.ID.make("gpt-5-nano"), (model) => {
        model.capabilities.input = ["text"]
        model.capabilities.output = ["text"]
        model.cost = cost(10, 10)
        model.time.released = DateTime.makeUnsafe(Date.now())
      })

      const selected = yield* catalog.model.small(providerID)

      expect(Option.getOrUndefined(selected)?.id).toBe(ModelV2.ID.make("gpt-5-nano"))
    }).pipe(Effect.provide(Catalog.defaultLayer.pipe(Layer.provide(locationLayer)))),
  )
})
