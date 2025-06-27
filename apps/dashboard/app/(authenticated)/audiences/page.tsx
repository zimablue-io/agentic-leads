import { db, audiences } from "@agentic-leads/db";
import AudiencesTable, { AudienceRow } from "@/components/audiences-table";
import { desc } from "drizzle-orm";

async function getAudiences(): Promise<AudienceRow[]> {
	const rows = await db
		.select()
		.from(audiences)
		.orderBy(desc(audiences.createdAt));

	return rows.map((r) => ({
		id: r.id,
		name: r.name,
		description: r.description,
		createdAt:
			typeof r.createdAt === "string" ? r.createdAt : String(r.createdAt),
	}));
}

export const dynamic = "force-dynamic";

export default async function AudiencesPage() {
	const rows = await getAudiences();

	return (
		<div className="p-8 space-y-6">
			<h1 className="text-2xl font-semibold">Audiences</h1>
			<AudiencesTable initialRows={rows} />
		</div>
	);
}
