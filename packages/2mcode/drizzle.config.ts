import { defineConfig } from "drizzle-kit"

export default defineConfig({
  dialect: "sqlite",
  schema: "./src/**/*.sql.ts",
  out: "./migration",
  dbCredentials: {
    url: "/home/thdxr/.local/share/2M_CODE/2M_CODE.db",
  },
})
