const stage = process.env.SST_STAGE || "dev"

export default {
  url: stage === "production" ? "https://2M_CODE.ai" : `https://${stage}.2M_CODE.ai`,
  console: stage === "production" ? "https://2M_CODE.ai/auth" : `https://${stage}.2M_CODE.ai/auth`,
  email: "contact@anoma.ly",
  socialCard: "https://social-cards.sst.dev",
  github: "https://github.com/ArafatAhmed-2M/2mcode",
  discord: "https://2M_CODE.ai/discord",
  headerLinks: [
    { name: "app.header.home", url: "/" },
    { name: "app.header.docs", url: "/docs/" },
  ],
}
