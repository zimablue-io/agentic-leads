"use client";

import { supabase } from "@/lib/supabase/client";
import { useEffect, useState } from "react";
import { format } from "date-fns";

export type RunWithAudience = {
	id: string;
	status: string | null;
	location: string | null;
	createdAt: string | null;
	audienceName: string | null;
};

interface Props {
	initialRuns: RunWithAudience[];
}

export default function RunsTable({ initialRuns }: Props) {
	const [rows, setRows] = useState<RunWithAudience[]>(initialRuns);

	useEffect(() => {
		if (!supabase) return;

		const channel = supabase
			.channel("runs-feed")
			// Status updates
			.on(
				"postgres_changes",
				{ event: "UPDATE", schema: "public", table: "workflow_runs" },
				(payload: any) => {
					setRows((prev) =>
						prev.map((r) =>
							r.id === payload.new.id
								? { ...r, status: payload.new.status }
								: r
						)
					);
				}
			)
			// New run inserts
			.on(
				"postgres_changes",
				{ event: "INSERT", schema: "public", table: "workflow_runs" },
				async (payload: any) => {
					const newRun = payload.new;

					const { data: audienceData } = await supabase
						.from("audiences")
						.select("name")
						.eq("id", newRun.audience_id)
						.single();

					const row: RunWithAudience = {
						id: newRun.id,
						status: newRun.status,
						location: newRun.location,
						createdAt: newRun.created_at,
						audienceName: audienceData?.name ?? "",
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
					<th className="px-4 py-2">Audience</th>
					<th className="px-4 py-2">Location</th>
					<th className="px-4 py-2">Created</th>
					<th className="px-4 py-2">Status</th>
				</tr>
			</thead>
			<tbody>
				{rows.map((r) => (
					<tr key={r.id} className="border-b border-border/60">
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
						<td className="px-4 py-2">
							<span
								className={`${
									r.status === "completed"
										? "bg-green-600"
										: r.status === "running"
											? "bg-yellow-500"
											: r.status === "failed"
												? "bg-red-600"
												: "bg-gray-500"
								} text-white px-2 py-1 rounded text-xs capitalize`}
							>
								{r.status ?? "queued"}
							</span>
						</td>
					</tr>
				))}
			</tbody>
		</table>
	);
}
