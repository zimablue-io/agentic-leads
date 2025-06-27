# @agentic-leads/ui

Re-usable React **primitive components** shared across all front-end apps in the repository.

These components are deliberately _stateless_ and _framework-agnostic_—they contain **no business logic** and can be consumed by any feature module.

---

## Installation

```bash
pnpm --filter <your-app> add @agentic-leads/ui@workspace:* --save
```

Import directly by name:

```tsx
import { Button, Card } from "@agentic-leads/ui";

export default function Example() {
	return (
		<Card className="p-4">
			<Button appName="dashboard">Click me</Button>
		</Card>
	);
}
```

---

## Available Primitives

- `Button`
- `Card`
- `Code`
- … (add new primitives here)

When adding a new primitive, follow these rules:

1. **No data fetching or server actions** inside primitives.
2. If the component uses React hooks, place `'use client';` at the top.
3. Keep the API small and composable—prefer `className` overrides over prop bloat.

---

## Development

Run Storybook (if configured) or use the dashboard app as a playground:

```bash
pnpm -F @agentic-leads/ui dev
```

Lint & type-check:

```bash
pnpm -r turbo lint && pnpm -r turbo typecheck
```
