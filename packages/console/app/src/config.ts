/**
 * Application-wide constants and configuration
 */
export const config = {
  // Base URL
  baseUrl: "https://2M_CODE.ai",

  // GitHub
  github: {
    repoUrl: "https://github.com/ArafatAhmed-2M/2mcode",
    starsFormatted: {
      compact: "160K",
      full: "160,000",
    },
  },

  // Social links
  social: {
    twitter: "https://x.com/2M_CODE",
    discord: "https://discord.gg/2M_CODE",
  },

  // Static stats (used on landing page)
  stats: {
    contributors: "900",
    commits: "13,000",
    monthlyUsers: "7.5M",
  },
} as const
