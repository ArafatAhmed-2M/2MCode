import { Resource } from "@2M_CODE-ai/console-resource"

export const logger = {
  metric: (values: Record<string, any>) => {
    console.log(`_metric:${JSON.stringify(values)}`)
  },
  log: console.log,
  debug: (message: string) => {
    if (Resource.App.stage === "production") return
    console.debug(message)
  },
}
