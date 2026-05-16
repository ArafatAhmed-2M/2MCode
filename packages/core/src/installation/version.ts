declare global {
  const _2M_CODE_VERSION: string
  const _2M_CODE_CHANNEL: string
}

export const InstallationVersion = typeof _2M_CODE_VERSION === "string" ? _2M_CODE_VERSION : "local"
export const InstallationChannel = typeof _2M_CODE_CHANNEL === "string" ? _2M_CODE_CHANNEL : "local"
export const InstallationLocal = InstallationChannel === "local"
