import { db } from "./client";
import { workflowRuns, enqueueWorkerJob } from "./schema";
import { sql } from "drizzle-orm";

export async function createWorkflowRun(audienceId: string, location: string) {
	const [run] = await db
		.insert(workflowRuns)
		.values({ audienceId, location })
		.returning();
	return run;
}

export async function queueProspectingJob(
	audienceId: string,
	location: string,
	maxProspects = 5
) {
	const run = await createWorkflowRun(audienceId, location);
	// Enqueue job
	await db.execute(
		enqueueWorkerJob({
			run_id: run.id,
			audience_id: audienceId,
			location,
			max_prospects: maxProspects,
		}) as unknown as ReturnType<typeof sql>
	);
	return run;
}
