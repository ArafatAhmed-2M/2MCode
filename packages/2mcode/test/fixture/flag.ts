import type { WorkspaceID } from "@/control-plane/schema"
import { Flag } from "@2mcode-ai/core/flag/flag"
import { Effect, Scope } from "effect"

/**
 * Scoped override for `Flag._2MCODE_WORKSPACE_ID`. Saves the previous value
 * on entry and restores it via finalizer when the surrounding scope closes —
 * preserves the original try/finally semantics regardless of test outcome.
 */
export function withFixedWorkspaceID(id: WorkspaceID): Effect.Effect<void, never, Scope.Scope> {
  return Effect.gen(function* () {
    const previous = Flag._2MCODE_WORKSPACE_ID
    Flag._2MCODE_WORKSPACE_ID = id
    yield* Effect.addFinalizer(() =>
      Effect.sync(() => {
        Flag._2MCODE_WORKSPACE_ID = previous
      }),
    )
  })
}
