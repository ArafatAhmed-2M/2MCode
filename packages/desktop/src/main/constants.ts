import { app } from "electron"

type Channel = "dev" | "beta" | "prod"
const raw = import.meta.env._2MCODE_CHANNEL
export const CHANNEL: Channel = raw === "dev" || raw === "beta" || raw === "prod" ? raw : "dev"

export const SETTINGS_STORE = "2M_CODE.settings"
export const DEFAULT_SERVER_URL_KEY = "defaultServerUrl"
export const WSL_ENABLED_KEY = "wslEnabled"
export const UPDATER_ENABLED = app.isPackaged && CHANNEL !== "dev"
