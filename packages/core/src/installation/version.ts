declare global {
  const _2MCODE_VERSION: string
  const _2MCODE_CHANNEL: string
}

export const InstallationVersion = typeof _2MCODE_VERSION === "string" ? _2MCODE_VERSION : "local"
export const InstallationChannel = typeof _2MCODE_CHANNEL === "string" ? _2MCODE_CHANNEL : "local"
export const InstallationLocal = InstallationChannel === "local"
