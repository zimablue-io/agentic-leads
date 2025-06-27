"use client";

import { supabase } from "@/lib/supabase/client";
import { useState, useEffect } from "react";
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
		const channel = supabase
			.channel("runs-feed")
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
			.subscribe();

		return () => {
			supabase.removeChannel(channel);
		};
	}, []);

	return (
		<table className="min-w-full text-sm text-left text-gray-400">
			<thead>
				<tr className="border-b border-gray-700">
					<th className="px-4 py-2">Audience</th>
					<th className="px-4 py-2">Location</th>
					<th className="px-4 py-2">Created</th>
					<th className="px-4 py-2">Status</th>
				</tr>
			</thead>
			<tbody>
				{rows.map((r) => (
					<tr key={r.id} className="border-b border-gray-800">
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
