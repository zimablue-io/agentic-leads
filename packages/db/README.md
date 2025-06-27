# @agentic-leads/db

A **single-source-of-truth** database helper package that unifies access to the project's Supabase/PostgreSQL schema for both TypeScript (Dashboard) and Python (Workflow) code.

---

## What's inside?

| Path               | Purpose                                                          |
| ------------------ | ---------------------------------------------------------------- |
| `src/schema.ts`    | Drizzle ORM schema definitions (tables, enums, relations)        |
| `src/client.ts`    | Convenience helpers to obtain a typed Supabase or Drizzle client |
| `src/queue.ts`     | Functions for enqueuing / polling prospecting jobs               |
| `src/generated.ts` | **Auto-generated** TypeScript types from the live database       |

---

## Installation (inside the monorepo)

```bash
# Dashboard app (TypeScript)
pnpm --filter @agentic-leads/dashboard-app add @agentic-leads/db@workspace:* --save

# Workflow app (Python) – import via relative path or install as an editable package
pip install -e ../../packages/db  # from apps/workflow
```

> Tip: the `workspace:*` range lets pnpm link straight to the source.

---

## Generating Types

After you run a migration or modify the Supabase schema, regenerate the typed client:

```bash
pnpm --filter @agentic-leads/db run generate:types
```

This maps to the script in `package.json`:

```json
"generate:types": "supabase gen types typescript --linked --schema public > src/generated.ts"
```

Commit the updated `generated.ts` file so downstream packages stay in sync.

You may chain this in CI after a successful migration, e.g. in **supabase** package's `db:push` script.

---

## Usage Examples

```ts
import { db, audiences } from "@agentic-leads/db";

const rows = await db
	.select({ id: audiences.id, name: audiences.name })
	.from(audiences);
```

```python
from agentic_leads_db import Schema

user_table = Schema.tables.users
```

---

## Publishing (optional)

This package is consumed through the pnpm workspace, but can be published to npm or a private registry if you need to use it elsewhere:

```bash
pnpm -F @agentic-leads/db publish --access public
```
