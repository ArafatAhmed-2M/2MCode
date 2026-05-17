// @ts-nocheck

import { _2mcode } from "@2mcode-ai/core"
import { ReadTool } from "@2mcode-ai/core/tools"

const _2mcode = _2mcode.make({})

_2mcode.tool.add(ReadTool)

_2mcode.tool.add({
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

_2mcode.auth.add({
  provider: "openai",
  type: "api",
  value: process.env.OPENAI_API_KEY,
})

_2mcode.agent.add({
  name: "build",
  permissions: [],
  model: {
    id: "gpt-5-5",
    provider: "openai",
    variant: "xhigh",
  },
})

const sessionID = await _2mcode.session.create({
  agent: "build",
})

_2mcode.subscribe((event) => {
  console.log(event)
})

await _2mcode.session.prompt({
  sessionID,
  text: "hey what is up",
})

await _2mcode.session.prompt({
  sessionID,
  text: "what is up with this",
  files: [
    {
      mime: "image/png",
      uri: "data:image/png;base64,xxxx",
    },
  ],
})

await _2mcode.session.wait()

console.log(await _2mcode.session.messages(sessionID))
