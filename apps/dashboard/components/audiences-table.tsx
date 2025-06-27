"use client";

import { format } from "date-fns";
import { useState } from "react";

export type AudienceRow = {
	id: string;
	name: string | null;
	description: string | null;
	createdAt: string | null;
};

interface Props {
	initialRows: AudienceRow[];
}

export default function AudiencesTable({ initialRows }: Props) {
	const [rows] = useState<AudienceRow[]>(initialRows);

	return (
		<table className="min-w-full text-sm text-left text-muted-foreground">
			<thead>
				<tr className="border-b border-border">
					<th className="px-4 py-2">Name</th>
					<th className="px-4 py-2">Description</th>
					<th className="px-4 py-2">Created</th>
				</tr>
			</thead>
			<tbody>
				{rows.map((r) => (
					<tr key={r.id} className="border-b border-border/60">
						<td className="px-4 py-2 font-medium">{r.name}</td>
						<td className="px-4 py-2 max-w-md truncate">
							{r.description}
						</td>
						<td className="px-4 py-2">
							{r.createdAt
								? format(new Date(r.createdAt), "yyyy-MM-dd")
								: ""}
						</td>
					</tr>
				))}
			</tbody>
		</table>
	);
}
