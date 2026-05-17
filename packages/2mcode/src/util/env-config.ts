// Reads 2M Code env vars from process.env.
// Bun auto-loads .env from the project root — no dotenv dependency needed.
// Returns a partial config object merged as the lowest-priority layer;
// explicit 2mcode.jsonc settings always win.

const PROVIDER_KEY_MAP: Record<string, string> = {
  anthropic: "ANTHROPIC_API_KEY",
  openai: "OPENAI_API_KEY",
  google: "GEMINI_API_KEY",
  deepseek: "DEEPSEEK_API_KEY",
  groq: "GROQ_API_KEY",
  openrouter: "OPENROUTER_API_KEY",
}

export function fromEnv() {
  const provider = process.env["2MCODE_PROVIDER"]
  const model = process.env["2MCODE_MODEL"]
  const baseURL = process.env["2MCODE_BASE_URL"]

  const result: {
    model?: string
    provider?: Record<string, { options?: { apiKey?: string; baseURL?: string } }>
  } = {}

  if (provider && model) result.model = `${provider}/${model}`
  else if (model) result.model = model

  const providerBlock: typeof result.provider = {}

  for (const [providerID, envVar] of Object.entries(PROVIDER_KEY_MAP)) {
    const apiKey = process.env[envVar]
    if (!apiKey) continue
    providerBlock[providerID] = {
      options: {
        apiKey,
        ...(baseURL && provider === providerID ? { baseURL } : {}),
      },
    }
  }

  if (baseURL && provider && !providerBlock[provider]) {
    providerBlock[provider] = { options: { baseURL } }
  }

  if (Object.keys(providerBlock).length) result.provider = providerBlock

  return result
}

export * as EnvConfig from "./env-config"
