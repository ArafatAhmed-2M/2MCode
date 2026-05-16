import { addons, types } from "storybook/manager-api"
import { ThemeTool } from "./theme-tool"

addons.register("2M_CODE/theme-toggle", () => {
  addons.add("2M_CODE/theme-toggle/tool", {
    type: types.TOOL,
    title: "Theme",
    match: ({ viewMode }) => viewMode === "story" || viewMode === "docs",
    render: ThemeTool,
  })
})
