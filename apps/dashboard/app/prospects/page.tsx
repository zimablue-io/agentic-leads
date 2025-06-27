import { db, workflowRuns, audiences } from "@agentic-leads/db";
import { prospects as prospectsTable } from "@agentic-leads/db/schema";
import { desc, eq } from "drizzle-orm";
import ProspectsTable, { ProspectRow } from "@/components/prospects-table";

async function getProspects(): Promise<ProspectRow[]> {
	const rows = await db
		.select({
			id: prospectsTable.id,
			url: prospectsTable.url,
			createdAt: prospectsTable.createdAt,
			runId: workflowRuns.id,
			location: workflowRuns.location,
			audienceName: audiences.name,
		})
		.from(prospectsTable)
		.leftJoin(workflowRuns, eq(prospectsTable.runId, workflowRuns.id))
		.leftJoin(audiences, eq(workflowRuns.audienceId, audiences.id))
		.orderBy(desc(prospectsTable.createdAt))
		.limit(50);

	return rows.map((r) => ({
		...r,
		createdAt: r.createdAt ? String(r.createdAt) : null,
	}));
}

export const dynamic = "force-dynamic"; // ensure fresh data on each request

export default async function ProspectsPage() {
	const prospects = await getProspects();

	return (
		<div className="p-8 space-y-6">
			<h1 className="text-2xl font-semibold">Prospects</h1>
			<ProspectsTable initialRows={prospects} />
		</div>
	);
}
