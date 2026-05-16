import { afterEach, describe, expect, test } from "bun:test"
import { Option, Redacted } from "effect"
import { Flag } from "@2mcode-ai/core/flag/flag"
import { ServerAuth } from "../../src/server/auth"

const original = {
  _2MCODE_SERVER_PASSWORD: Flag._2MCODE_SERVER_PASSWORD,
  _2MCODE_SERVER_USERNAME: Flag._2MCODE_SERVER_USERNAME,
}

afterEach(() => {
  Flag._2MCODE_SERVER_PASSWORD = original._2MCODE_SERVER_PASSWORD
  Flag._2MCODE_SERVER_USERNAME = original._2MCODE_SERVER_USERNAME
})

describe("ServerAuth", () => {
  test("does not emit auth headers without a password", () => {
    Flag._2MCODE_SERVER_PASSWORD = undefined
    Flag._2MCODE_SERVER_USERNAME = "alice"

    expect(ServerAuth.header()).toBeUndefined()
    expect(ServerAuth.headers()).toBeUndefined()
  })

  test("defaults to the 2M_CODE username", () => {
    Flag._2MCODE_SERVER_PASSWORD = "secret"
    Flag._2MCODE_SERVER_USERNAME = undefined

    expect(ServerAuth.headers()).toEqual({
      Authorization: `Basic ${Buffer.from("2M_CODE:secret").toString("base64")}`,
    })
  })

  test("uses the configured username", () => {
    Flag._2MCODE_SERVER_PASSWORD = "secret"
    Flag._2MCODE_SERVER_USERNAME = "alice"

    expect(ServerAuth.headers()).toEqual({
      Authorization: `Basic ${Buffer.from("alice:secret").toString("base64")}`,
    })
  })

  test("prefers explicit credentials", () => {
    Flag._2MCODE_SERVER_PASSWORD = "secret"
    Flag._2MCODE_SERVER_USERNAME = "alice"

    expect(ServerAuth.headers({ password: "cli-secret", username: "bob" })).toEqual({
      Authorization: `Basic ${Buffer.from("bob:cli-secret").toString("base64")}`,
    })
  })

  test("validates decoded credentials against effect config", () => {
    const config = { password: Option.some("secret"), username: "alice" }

    expect(ServerAuth.required(config)).toBe(true)
    expect(ServerAuth.authorized({ username: "alice", password: Redacted.make("secret") }, config)).toBe(true)
    expect(ServerAuth.authorized({ username: "2M_CODE", password: Redacted.make("secret") }, config)).toBe(false)
  })
})
