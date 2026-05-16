export * from "./gen/types.gen.js"

import { createClient } from "./gen/client/client.gen.js"
import { type Config } from "./gen/client/types.gen.js"
import { 2M_CODEClient } from "./gen/sdk.gen.js"
import { wrapClientError } from "./error-interceptor.js"
export { type Config as 2M_CODEClientConfig, 2M_CODEClient }

function pick(value: string | null, fallback?: string) {
  if (!value) return
  if (!fallback) return value
  if (value === fallback) return fallback
  if (value === encodeURIComponent(fallback)) return fallback
  return value
}

function rewrite(request: Request, directory?: string) {
  if (request.method !== "GET" && request.method !== "HEAD") return request

  const value = pick(request.headers.get("x-2M_CODE-directory"), directory)
  if (!value) return request

  const url = new URL(request.url)
  if (!url.searchParams.has("directory")) {
    url.searchParams.set("directory", value)
  }

  const next = new Request(url, request)
  next.headers.delete("x-2M_CODE-directory")
  return next
}

export function create2M_CODEClient(config?: Config & { directory?: string }) {
  if (!config?.fetch) {
    const customFetch: any = (req: any) => {
      // @ts-ignore
      req.timeout = false
      return fetch(req)
    }
    config = {
      ...config,
      fetch: customFetch,
    }
  }

  if (config?.directory) {
    config.headers = {
      ...config.headers,
      "x-2M_CODE-directory": encodeURIComponent(config.directory),
    }
  }

  const client = createClient(config)
  client.interceptors.request.use((request) => rewrite(request, config?.directory))
  client.interceptors.error.use(wrapClientError)
  return new 2M_CODEClient({ client })
}
