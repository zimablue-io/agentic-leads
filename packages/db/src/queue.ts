import { supabase } from "./client";
import type { Database } from "./generated";

export async function queueProspectingJob(
	audienceId: string,
	location: string,
	maxProspects: number
) {
	// Insert a workflow_run entry with status 'queued'
	const { data, error } = await supabase
		.from("workflow_runs")
		.insert({
			audience_id: audienceId,
			location,
			status: "queued",
		})
		.select()
		.single();

	if (error) {
		throw new Error(`Failed to queue run: ${error.message}`);
	}

	// Enqueue a job via pgmq function (if available) – best-effort
	await supabase.rpc("pgmq_enqueue", {
		queue_name: "worker_jobs",
		payload: {
			run_id: data.id,
			max: maxProspects,
		},
	});

	return data;
}
