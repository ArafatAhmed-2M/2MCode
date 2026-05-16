import type { ElectronAPI } from "../preload/types"

declare global {
  interface Window {
    api: ElectronAPI
    __2M_CODE__?: {
      deepLinks?: string[]
    }
  }
}
