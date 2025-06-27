import { db, prospects, siteAnalyses, contacts } from "@agentic-leads/db";
import { eq } from "drizzle-orm";
import { notFound } from "next/navigation";

export const dynamic = "force-dynamic";

async function getProspectData(id: string) {
	const prospect = await db
		.select()
		.from(prospects)
		.where(eq(prospects.id, id))
		.limit(1);

	if (!prospect.length) return null;

	const analysis = await db
		.select()
		.from(siteAnalyses)
		.where(eq(siteAnalyses.prospectId, id))
		.limit(1);

	const contactRows = await db
		.select()
		.from(contacts)
		.where(eq(contacts.prospectId, id));

	return {
		prospect: prospect[0],
		analysis: analysis[0] ?? null,
		contacts: contactRows,
	};
}

export default async function ProspectDetail({
	params,
}: {
	params: { id: string };
}) {
	const data = await getProspectData(params.id);

	if (!data) notFound();

	const { prospect, analysis, contacts } = data;

	return (
		<div className="p-8 space-y-6">
			<h1 className="text-2xl font-semibold break-all">
				Prospect Detail – {prospect.url}
			</h1>

			<section className="space-y-4">
				<h2 className="text-xl font-medium">Site Analysis Scores</h2>
				{analysis ? (
					<ul className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
						{Object.entries(analysis.scores).map(([key, value]) => (
							<li
								key={key}
								className="bg-card border border-border rounded-md p-4 flex flex-col gap-2"
							>
								<span className="text-sm text-muted-foreground uppercase">
									{key}
								</span>
								<span className="text-lg font-semibold">
									{value}
								</span>
							</li>
						))}
					</ul>
				) : (
					<p className="text-muted-foreground">
						No analysis available.
					</p>
				)}
			</section>

			<section className="space-y-4">
				<h2 className="text-xl font-medium">
					Contacts ({contacts.length})
				</h2>
				{contacts.length ? (
					<ul className="space-y-2">
						{contacts.map((c) => (
							<li
								key={c.id}
								className="bg-card border border-border rounded p-2"
							>
								<span className="font-medium">{c.type}:</span>{" "}
								{c.value}
							</li>
						))}
					</ul>
				) : (
					<p className="text-muted-foreground">No contacts found.</p>
				)}
			</section>
		</div>
	);
}
