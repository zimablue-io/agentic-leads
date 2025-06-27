# @agentic-leads/eslint-config

Shared ESLint configurations for all JavaScript/TypeScript workspaces in the monorepo.

Three presets are exported:

| Export name      | Extends                                       | Recommended usage                            |
| ---------------- | --------------------------------------------- | -------------------------------------------- |
| `base`           | `eslint:recommended`, Prettier                | Node and tooling packages                    |
| `react-internal` | `base` + `eslint-plugin-react`, `react-hooks` | React packages that are not Next.js          |
| `next-js`        | `react-internal` + `@next/eslint-plugin-next` | Next.js applications (e.g. `apps/dashboard`) |

---

## How to Use

In your package's `eslint.config.js` (new flat config) or `.eslintrc`:

```js
import { nextJs } from "@agentic-leads/eslint-config/next-js";

export default [nextJs];
```

or for classic config:

```json
{
	"extends": "@agentic-leads/eslint-config/next-js"
}
```

---

## Rules of Thumb

- Keep new rules inside this package so every project stays consistent.
- Never disable a rule locally unless there is a _strong_ justification.
- If you add a dependency (e.g. a new plugin), remember to bump `peerDependencies` here.
