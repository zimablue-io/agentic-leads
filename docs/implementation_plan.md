# Implementation Plan: Dashboard Modernisation

This document describes the **exact** steps we will execute to modernise the `apps/dashboard` application so that it:

- shares configuration with the rest of the monorepo
- uses clear TypeScript path aliases instead of deep relative imports
- consumes primitives from `packages/ui`
- replaces the deprecated **@supabase/auth-helpers-nextjs** package with **@supabase/ssr** (no deprecated code left behind)
- removes the legacy `apps/web` example entirely

---

## 1 Adopt Shared Configuration Packages (no placeholders)

1.  Replace the current `apps/dashboard/tsconfig.json` with a minimal file that **extends** the shared preset:

```json
{
	"extends": "@agentic-leads/typescript-config/nextjs.json"
}
```

This keeps dashboard fully aligned with the TypeScript configuration shipped in `packages/typescript-config` while letting package imports resolve naturally via pnpm workspaces.

2.  **Keep** the existing Tailwind setup inside `apps/dashboard/tailwind.config.ts`; just remove any redundant or duplicated theme definitions as we start re-using primitives from `packages/ui`.

## 2 Path Aliases & Import Hygiene

1.  Ensure each internal package you need is declared in `apps/dashboard/package.json` with the workspace wildcard, e.g.

```json
"dependencies": {
  "@agentic-leads/ui": "workspace:*",
  "@agentic-leads/db": "workspace:*"
}
```

After that, import directly:

```ts
import { Button } from "@agentic-leads/ui";
import { db } from "@agentic-leads/db";
```

2.  Convert every deep-relative import (e.g. `../../../packages/ui/button`) to the package import shown above. No "TODO" comments may remain.
3.  Keep the ESLint rule `import/no-relative-parent-imports` set to **error** to forbid crossing package boundaries via relative paths.

## 3 Establish `packages/db` as the Single Source of Truth

1.  Create **packages/db** and move the _working_ code currently under `supabase/` (including Drizzle ORM schema, client helpers, and queue logic) into this package.
2.  Provide a script `pnpm --filter @agentic-leads/db run generate:types` that invokes `supabase gen types typescript --linked --schema public` and writes the result to `src/generated.ts`. This script must run automatically after any schema migration.
3.  Ensure all TypeScript code in `apps/dashboard` imports database utilities from `@db/*`.
4.  Update the Python workflow app to import generated types (or the SQL schema) from `packages/db` if needed instead of duplicating definitions.

## 4 UI Layering

1.  Move all _pure_ primitives from `apps/dashboard/components/ui` to `packages/ui`.
2.  Keep feature-specific components (e.g. the Runs table) inside `apps/dashboard`.
3.  Delete any duplicated or legacy component versions—only one canonical implementation should exist.

## 5 Supabase Migration to `@supabase/ssr`

1.  Remove **@supabase/auth-helpers-nextjs** and add **@supabase/ssr**.
2.  Implement `lib/supabase/{client,server,middleware}.ts` using `createBrowserClient()` and `createServerClient()`—no placeholder code, no console noise.
3.  Update server actions, middleware, and client hooks to the new API.
4.  Delete every file or line that references the deprecated helpers.

## 6 Next.js 15 Client / Server Correctness

1.  Scan all files for React hooks; add `'use client'` where necessary or refactor to server components.
2.  Enable ESLint rules `@next/next/no-async-client-component` and `react-hooks/rules-of-hooks`.

## 7 Delete Legacy `apps/web`

Remove the entire `apps/web` directory and its references from `turbo.json` once the shared configs are confirmed to work.

---

### Milestone Checklist

| Milestone                                      | Status |
| ---------------------------------------------- | ------ |
| Shared TS & Tailwind configs in place          | ✔     |
| Import aliases converted                       | ✔     |
| `packages/db` established & types script ready | ✔     |
| Supabase fully migrated to `@supabase/ssr`     | ✔     |
| UI primitives centralised in `packages/ui`     | ✔     |
| Legacy `apps/web` removed                      | ✔     |
| React client/server boundaries verified        | ✔     |
