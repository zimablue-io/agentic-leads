# Tech Stack

This document captures the _core_ technologies and library versions used across the **Agentic-Leads** monorepo. Keep this file updated when upgrading dependencies so downstream services (workers, CI, infra) can stay in sync.

---

## JavaScript / TypeScript (PNPM Workspaces)

| Domain                | Package                 | Version                        | Notes                                                                               |
| --------------------- | ----------------------- | ------------------------------ | ----------------------------------------------------------------------------------- |
| **Framework**         | `next`                  | **15.2.4**                     | App Router (Next 15) – check release notes for eventual `app`-router-only features. |
|                       | `react` / `react-dom`   | **^19**                        | React 19 concurrent features available.                                             |
| **Styling**           | `tailwindcss`           | ^3.4.17                        | Config in `tailwind.config.ts`; uses Tailwind v3.                                   |
|                       | `tailwindcss-animate`   | ^1.0.7                         | Animations.                                                                         |
| **UI Primitives**     | `@radix-ui/*`           | 1.x / 2.x                      | Radix UI primitives; versions match shadcn-ui generator output.                     |
|                       | `lucide-react`          | ^0.454.0                       | Icon set.                                                                           |
| **Data / Backend**    | `@supabase/supabase-js` | latest (resolved via lockfile) | Typed client for Supabase.                                                          |
|                       | `drizzle-orm`           | ^0.44.2                        | Type-safe SQL builder.                                                              |
|                       | `pg`                    | ^8.11.3                        | Node Postgres driver (used by db package).                                          |
| **State / Forms**     | `react-hook-form`       | ^7.54.1                        | Forms.                                                                              |
|                       | `zod`                   | ^3.24.1                        | Validation schemas.                                                                 |
| **Build / Monorepo**  | `turbo`                 | 2.5.4                          | Task-runner for the monorepo.                                                       |
|                       | `pnpm`                  | 9.x (lockfile)                 | Workspace package manager.                                                          |
|                       | `typescript`            | 5.8.x                          | Monorepo‐wide ts-config base.                                                       |
| **Testing / Linting** | `eslint`                | ^9.29.0 (via workspace config) | Shared config in `packages/eslint-config`.                                          |
|                       | `prettier`              | ^3.6.0                         | Formatting.                                                                         |

## Python (apps/workflow)

| Domain             | Package           | Version  | Notes                                            |
| ------------------ | ----------------- | -------- | ------------------------------------------------ |
| **OpenAI Agents**  | `openai-agents`   | >=0.0.19 | SDK powering the autonomous workflows.           |
|                    | `openai`          | 1.50.0   | Official OpenAI Python SDK.                      |
| **Web Automation** | `playwright`      | >=1.48.0 | For website scraping / analysis.                 |
|                    | `beautifulsoup4`  | >=4.12.0 | HTML parsing.                                    |
| **Async HTTP**     | `aiohttp`         | >=3.10.0 | Async HTTP client (for scraping, APIs).          |
| **Database**       | `supabase`        | >=2.3.0  | Python Supabase client.                          |
|                    | `psycopg2-binary` | >=2.9.0  | Postgres driver.                                 |
|                    | `sqlalchemy`      | >=2.0.0  | SQL toolkit (used by worker for Ad-hoc queries). |
| **Utilities**      | `validators`      | >=0.22.0 | URL/email validation.                            |
|                    | `python-dotenv`   | >=1.0.0  | `.env` loading.                                  |
| **Dev / QA**       | `pytest`          | >=8.0.0  | Unit testing.                                    |
|                    | `black`           | >=24.0.0 | Code formatter.                                  |
|                    | `ruff`            | >=0.6.0  | Linter.                                          |
|                    | `mypy`            | >=1.11.0 | Type-checking.                                   |

## Runtime & Infrastructure

| Item              | Version / Service                                               |
| ----------------- | --------------------------------------------------------------- |
| Node.js (engines) | >=18 (set in root `package.json`)                               |
| Python            | 3.11 (required by `pyproject.toml`)                             |
| Database          | PostgreSQL (Supabase) – latest 15.x (cloud-managed)             |
| Queue             | `pgmq` extension on Supabase for job queueing                   |
| Deployment        | Next.js app → Vercel; Worker → Fly.io / Supabase Function (TBD) |

---

> **Tip**: Use `pnpm outdated` and `uv pip compile --upgrade` (for Python) to identify safe upgrade paths. When bumping major versions, cross-check breaking changes before merging.
