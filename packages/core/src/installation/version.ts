declare global {
  const 2M_CODE_VERSION: string
  const 2M_CODE_CHANNEL: string
}

export const InstallationVersion = typeof 2M_CODE_VERSION === "string" ? 2M_CODE_VERSION : "local"
export const InstallationChannel = typeof 2M_CODE_CHANNEL === "string" ? 2M_CODE_CHANNEL : "local"
export const InstallationLocal = InstallationChannel === "local"
