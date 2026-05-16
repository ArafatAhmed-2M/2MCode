// @ts-nocheck

import { 2M_CODE } from "@2mcode-ai/core"
import { ReadTool } from "@2mcode-ai/core/tools"

const 2M_CODE = 2M_CODE.make({})

2M_CODE.tool.add(ReadTool)

2M_CODE.tool.add({
  name: "bash",
  schema: {
    type: "object",
    properties: {
      command: {
        type: "string",
        description: "The command to run.",
      },
    },
    required: ["command"],
  },
  execute(input, ctx) {},
})

2M_CODE.auth.add({
  provider: "openai",
  type: "api",
  value: process.env.OPENAI_API_KEY,
})

2M_CODE.agent.add({
  name: "build",
  permissions: [],
  model: {
    id: "gpt-5-5",
    provider: "openai",
    variant: "xhigh",
  },
})

const sessionID = await 2M_CODE.session.create({
  agent: "build",
})

2M_CODE.subscribe((event) => {
  console.log(event)
})

await 2M_CODE.session.prompt({
  sessionID,
  text: "hey what is up",
})

await 2M_CODE.session.prompt({
  sessionID,
  text: "what is up with this",
  files: [
    {
      mime: "image/png",
      uri: "data:image/png;base64,xxxx",
    },
  ],
})

await 2M_CODE.session.wait()

console.log(await 2M_CODE.session.messages(sessionID))
