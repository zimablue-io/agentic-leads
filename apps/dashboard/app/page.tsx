import { createClient, isSupabaseConfigured } from "@/lib/supabase/server";
import { redirect } from "next/navigation";
import { Button } from "@/components/ui/button";
import { LogOut } from "lucide-react";
import { signOut, startProspectingRun } from "@/lib/actions";

// DB (server-side)
import { db, audiences, workflowRuns } from "@agentic-leads/db";
import { eq, desc } from "drizzle-orm";
import RunsTable, { RunWithAudience } from "@/components/RunsTable";

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

function StatusBadge({ status }: { status: string | null }) {
	const color =
		status === "completed"
			? "bg-green-600"
			: status === "running"
				? "bg-yellow-500"
				: "bg-gray-500";
	return (
		<span
			className={`${color} text-white px-2 py-1 rounded text-xs capitalize`}
		>
			{status ?? "queued"}
		</span>
	);
}

export default async function Home() {
	// If Supabase is not configured, show setup message directly
	if (!isSupabaseConfigured) {
		return (
			<div className="flex min-h-screen items-center justify-center bg-[#161616]">
				<h1 className="text-2xl font-bold mb-4 text-white">
					Connect Supabase to get started app
				</h1>
			</div>
		);
	}

	// Auth guard
	const supabase = await createClient();
	const {
		data: { user },
	} = await supabase.auth.getUser();

	if (!user) redirect("/auth/login");

	// Fetch data for page
	const { runs, audiences: auds } = await getData();

	return (
		<div className="min-h-screen bg-[#161616] text-white p-8 space-y-10">
			<header className="flex items-center justify-between">
				<h1 className="text-3xl font-bold">Agentic Leads Dashboard</h1>
				<form action={signOut}>
					<Button className="bg-red-600 hover:bg-red-500">
						<LogOut className="h-4 w-4 mr-2" /> Sign Out
					</Button>
				</form>
			</header>

			{/* New Run form */}
			<form action={startProspectingRun} className="space-y-4">
				<div className="flex gap-4">
					<select
						name="audience"
						className="bg-[#1c1c1c] border-gray-700 rounded px-3 py-2"
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
						className="bg-[#1c1c1c] border-gray-700 rounded px-3 py-2 flex-1"
						required
					/>
					<input
						type="number"
						name="max"
						min="1"
						max="25"
						defaultValue={5}
						className="bg-[#1c1c1c] border-gray-700 rounded px-3 py-2 w-24"
					/>
					<Button
						type="submit"
						className="bg-[#2b725e] hover:bg-[#235e4c]"
					>
						Start Run
					</Button>
				</div>
			</form>

			{/* Runs list */}
			<section className="bg-[#1c1c1c] p-4 rounded-lg overflow-x-auto">
				<h2 className="text-xl font-semibold mb-4">Recent Runs</h2>
				<RunsTable initialRuns={runs} />
			</section>
		</div>
	);
}
