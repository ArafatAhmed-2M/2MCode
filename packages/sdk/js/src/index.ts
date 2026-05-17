export * from "./client.js"
export * from "./server.js"

import { create_2MCodeClient } from "./client.js"
import { create2M_CODEServer } from "./server.js"
import type { ServerOptions } from "./server.js"

export async function create2M_CODE(options?: ServerOptions) {
  const server = await create2M_CODEServer({
    ...options,
  })

  const client = create_2MCodeClient({
    baseUrl: server.url,
  })

  return {
    client,
    server,
  }
}
