# @agentic-leads/typescript-config

Centralised TypeScript configuration presets used across the monorepo.

---

## Available tsconfig presets

| File          | Extends                     | Purpose                                              |
| ------------- | --------------------------- | ---------------------------------------------------- |
| `base.json`   | —                           | Strict, modern defaults for libraries and Node tools |
| `nextjs.json` | `base.json` + `next` plugin | Configuration optimised for Next.js 14/15 apps       |

Each preset adheres to the _most restrictive rule set we can get away with_—`strict: true`, `skipLibCheck: true`, `target: ES2022`, etc.

---

## Usage

In your package:

```json
{
	"extends": "@agentic-leads/typescript-config/nextjs.json"
}
```

You can still override `compilerOptions` locally for package-specific needs, but avoid disabling strictness flags.

---

## Releasing changes

1. Edit the JSON files.
2. Bump the `version` field in `package.json`.
3. Run `pnpm -F @agentic-leads/typescript-config test` (if you add tests) or simply `pnpm -r turbo typecheck` to ensure every package still compiles.
