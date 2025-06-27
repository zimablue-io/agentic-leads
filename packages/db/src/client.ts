import { createClient } from "@supabase/supabase-js";
import { drizzle } from "drizzle-orm/node-postgres";
import { Pool } from "pg";
import type { Database } from "./generated";

if (
	!process.env.NEXT_PUBLIC_SUPABASE_URL ||
	!process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY
) {
	console.warn("Supabase environment variables are missing");
}

export const supabase = createClient<Database>(
	process.env.NEXT_PUBLIC_SUPABASE_URL || "",
	process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || "",
	{} // default options
);

export const pool = new Pool({
	connectionString:
		process.env.DATABASE_URL || process.env.NEXT_PUBLIC_SUPABASE_URL,
	ssl:
		process.env.NODE_ENV === "production"
			? { rejectUnauthorized: false }
			: undefined,
});

export const db = drizzle(pool);
