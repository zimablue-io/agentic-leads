import {
	pgTable,
	uuid,
	text,
	jsonb,
	timestamp,
	varchar,
} from "drizzle-orm/pg-core";

export const audiences = pgTable("audiences", {
	id: uuid("id").primaryKey().defaultRandom(),
	name: text("name").notNull(),
	description: text("description"),
	config: jsonb("config").notNull(),
	createdAt: timestamp("created_at").defaultNow(),
	updatedAt: timestamp("updated_at").defaultNow().notNull(),
});

export const workflowRuns = pgTable("workflow_runs", {
	id: uuid("id").primaryKey().defaultRandom(),
	audienceId: uuid("audience_id").references(() => audiences.id),
	location: varchar("location", { length: 128 }),
	status: text("status").default("queued"),
	startedAt: timestamp("started_at"),
	finishedAt: timestamp("finished_at"),
	createdAt: timestamp("created_at").defaultNow(),
});
