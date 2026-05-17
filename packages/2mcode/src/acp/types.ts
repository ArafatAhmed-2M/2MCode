import type { McpServer } from "@agentclientprotocol/sdk"
import type { _2MCodeClient } from "@2mcode-ai/sdk/v2"
import type { ProviderID, ModelID } from "../provider/schema"

export interface ACPSessionState {
  id: string
  cwd: string
  mcpServers: McpServer[]
  createdAt: Date
  model?: {
    providerID: ProviderID
    modelID: ModelID
  }
  variant?: string
  modeId?: string
}

export interface ACPConfig {
  sdk: _2MCodeClient
  defaultModel?: {
    providerID: ProviderID
    modelID: ModelID
  }
}
