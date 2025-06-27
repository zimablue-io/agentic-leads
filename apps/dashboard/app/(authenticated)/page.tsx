import { Button } from "@/components/ui/button";
import { LogOut } from "lucide-react";
import { signOut, startProspectingRun } from "@/lib/actions";

// DB (server-side)
import { db, audiences, workflowRuns } from "@agentic-leads/db";
import { eq, desc } from "drizzle-orm";
import RunsTable, { RunWithAudience } from "@/components/runs-table";

async function getData(): Promise<{
	runs: RunWithAudience[];
	audiences: { id: string; name: string }[];
}> {
	// Fetch audiences for dropdown
	const auds = await db
		.select({ id: audiences.id, name: audiences.name })
		.from(audiences);

	// Fetch latest 20 runs with join for audience name
	const rawRuns = await db
		.select({
			id: workflowRuns.id,
			status: workflowRuns.status,
			location: workflowRuns.location,
			createdAt: workflowRuns.createdAt,
			audienceName: audiences.name,
		})
		.from(workflowRuns)
		.leftJoin(audiences, eq(workflowRuns.audienceId, audiences.id))
		.orderBy(desc(workflowRuns.createdAt))
		.limit(20);

	const runs: RunWithAudience[] = rawRuns.map((r) => ({
		...r,
		createdAt:
			r.createdAt instanceof Date
				? r.createdAt.toISOString()
				: r.createdAt,
	}));

	return { runs, audiences: auds };
}

export default async function Home() {
	// Fetch data for page
	const { runs, audiences: auds } = await getData();

	return (
		<div className="min-h-screen p-8 space-y-10">
			<header className="flex items-center justify-between">
				<h1 className="text-3xl font-bold">Agentic Leads Dashboard</h1>
				<form action={signOut}>
					<Button variant="destructive">
						<LogOut className="h-4 w-4 mr-2" /> Sign Out
					</Button>
				</form>
			</header>

			{/* New Run form */}
			<form action={startProspectingRun} className="space-y-4">
				<div className="flex gap-4">
					<select
						name="audience"
						className="bg-secondary border-border rounded px-3 py-2"
						required
					>
						<option value="" disabled>
							Select audience…
						</option>
						{auds.map((a) => (
							<option key={a.id} value={a.id}>
								{a.name}
							</option>
						))}
					</select>
					<input
						type="text"
						name="location"
						placeholder="Location (e.g. Johannesburg)"
						className="bg-secondary border-border rounded px-3 py-2 flex-1"
						required
					/>
					<input
						type="number"
						name="max"
						min="1"
						max="25"
						defaultValue={5}
						className="bg-secondary border-border rounded px-3 py-2 w-24"
					/>
					<Button
						type="submit"
						className="bg-green-700 hover:bg-green-600"
					>
						Start Run
					</Button>
				</div>
			</form>

			{/* Runs list */}
			<section className="bg-card p-4 rounded-lg overflow-x-auto border border-border/60">
				<h2 className="text-xl font-semibold mb-4">Recent Runs</h2>
				<RunsTable initialRuns={runs} />
			</section>
		</div>
	);
}
