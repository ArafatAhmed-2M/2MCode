import { $ } from "bun"

await $`bun ./scripts/copy-icons.ts ${process.env._2MCODE_CHANNEL ?? "dev"}`

await $`cd ../2M_CODE && bun script/build-node.ts`
