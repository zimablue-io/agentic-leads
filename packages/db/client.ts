import postgres from "postgres";
import { drizzle } from "drizzle-orm/postgres-js";
import * as schema from "./schema";

// The DATABASE_URL should be set in env (.env or process)
const connectionString = process.env.DATABASE_URL as string;
if (!connectionString) {
	throw new Error("DATABASE_URL env variable not set");
}

export const client = postgres(connectionString, {
	ssl: "require",
});

export const db = drizzle(client, { schema });
