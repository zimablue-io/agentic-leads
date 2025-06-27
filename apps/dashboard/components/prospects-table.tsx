"use client";

import { supabase } from "@/lib/supabase/client";
import { useEffect, useState } from "react";
import { format } from "date-fns";
import Link from "next/link";

export type ProspectRow = {
	id: string;
	url: string | null;
	location: string | null;
	audienceName: string | null;
	runId: string | null;
	createdAt: string | null;
};

interface Props {
	initialRows: ProspectRow[];
}

export default function ProspectsTable({ initialRows }: Props) {
	const [rows, setRows] = useState<ProspectRow[]>(initialRows);

	useEffect(() => {
		if (!supabase) return;

		const channel = supabase
			.channel("prospects-feed")
			.on(
				"postgres_changes",
				{ event: "INSERT", schema: "public", table: "prospects" },
				async (payload: any) => {
					const newProspect = payload.new;

					// Get run + audience info for the new prospect
					const { data: runData } = await supabase
						.from("workflow_runs")
						.select("location, audience_id")
						.eq("id", newProspect.workflow_run_id)
						.single();

					let audienceName: string | null = null;
					if (runData?.audience_id) {
						const { data: audData } = await supabase
							.from("audiences")
							.select("name")
							.eq("id", runData.audience_id)
							.single();
						audienceName = audData?.name ?? null;
					}

					const row: ProspectRow = {
						id: newProspect.id,
						url: newProspect.url,
						location: runData?.location ?? null,
						audienceName,
						runId: newProspect.workflow_run_id,
						createdAt: newProspect.created_at,
					};

					setRows((prev) => [row, ...prev]);
				}
			)
			.subscribe();

		return () => {
			supabase.removeChannel(channel);
		};
	}, []);

	return (
		<table className="min-w-full text-sm text-left text-muted-foreground">
			<thead>
				<tr className="border-b border-border">
					<th className="px-4 py-2">URL</th>
					<th className="px-4 py-2">Audience</th>
					<th className="px-4 py-2">Location</th>
					<th className="px-4 py-2">Created</th>
					<th className="px-4 py-2" />
				</tr>
			</thead>
			<tbody>
				{rows.map((r) => (
					<tr key={r.id} className="border-b border-border/60">
						<td className="px-4 py-2 truncate max-w-xs">
							{r.url ? (
								<a
									href={r.url}
									target="_blank"
									rel="noopener noreferrer"
									className="text-primary underline"
								>
									{r.url}
								</a>
							) : (
								"—"
							)}
						</td>
						<td className="px-4 py-2">{r.audienceName}</td>
						<td className="px-4 py-2">{r.location}</td>
						<td className="px-4 py-2">
							{r.createdAt
								? format(
										new Date(r.createdAt),
										"yyyy-MM-dd HH:mm:ss"
									)
								: ""}
						</td>
						<td className="px-4 py-2 text-right">
							<Link
								href={`/prospects/${r.id}`}
								className="text-primary underline text-xs"
							>
								Details
							</Link>
						</td>
					</tr>
				))}
			</tbody>
		</table>
	);
}
