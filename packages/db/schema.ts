import {
	pgTable,
	uuid,
	text,
	timestamp,
	integer,
	jsonb,
	varchar,
} from "drizzle-orm/pg-core";
import { sql } from "drizzle-orm";

/**
 * audiences – stores saved AudienceConfig objects (JSON so that Python + TS stay in-sync).
 */
export const audiences = pgTable("audiences", {
	id: uuid("id").defaultRandom().primaryKey(),
	name: text("name").notNull(),
	description: text("description"),
	config: jsonb("config").notNull(), // raw AudienceConfig JSON
	createdAt: timestamp("created_at", { mode: "string" }).defaultNow(),
	updatedAt: timestamp("updated_at", { mode: "string" })
		.defaultNow()
		.notNull(),
});

/**
 * workflow_runs – a single invocation of the prospecting workflow.
 */
export const workflowRuns = pgTable("workflow_runs", {
	id: uuid("id").defaultRandom().primaryKey(),
	audienceId: uuid("audience_id").references(() => audiences.id, {
		onDelete: "cascade",
	}),
	location: varchar("location", { length: 128 }),
	status: text("status").default("queued"), // queued | running | completed | failed
	startedAt: timestamp("started_at", { mode: "string" }),
	finishedAt: timestamp("finished_at", { mode: "string" }),
	createdAt: timestamp("created_at", { mode: "string" }).defaultNow(),
});

/**
 * prospects – raw URLs discovered by the search tool.
 */
export const prospects = pgTable("prospects", {
	id: uuid("id").defaultRandom().primaryKey(),
	runId: uuid("workflow_run_id").references(() => workflowRuns.id, {
		onDelete: "cascade",
	}),
	url: text("url").notNull(),
	sourceQuery: text("source_query"),
	createdAt: timestamp("created_at", { mode: "string" }).defaultNow(),
});

/**
 * site_analyses – output of Python Playwright analysis and scoring JSON.
 */
export const siteAnalyses = pgTable("site_analyses", {
	id: uuid("id").defaultRandom().primaryKey(),
	prospectId: uuid("prospect_id").references(() => prospects.id, {
		onDelete: "cascade",
	}),
	scores: jsonb("scores_json").notNull(),
	techIssues: jsonb("tech_issues_json"),
	analyzedAt: timestamp("analyzed_at", { mode: "string" }).defaultNow(),
});

/**
 * contacts – emails / phones discovered on the website.
 */
export const contacts = pgTable("contacts", {
	id: uuid("id").defaultRandom().primaryKey(),
	prospectId: uuid("prospect_id").references(() => prospects.id, {
		onDelete: "cascade",
	}),
	type: text("type").notNull(), // email | phone | social
	value: text("value").notNull(),
	createdAt: timestamp("created_at", { mode: "string" }).defaultNow(),
});

// ------------------ Queue helpers ------------------
// Minimal TypeScript helpers to enqueue jobs from the server.
export type WorkerJobPayload = {
	run_id: string;
	audience_id: string;
	location?: string | null;
	max_prospects?: number;
};

export const enqueueWorkerJob = (payload: WorkerJobPayload) =>
	sql`SELECT * FROM pgmq.enqueue('worker_jobs', ${payload}::jsonb)`;
