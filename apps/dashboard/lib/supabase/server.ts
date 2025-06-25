import { createServerComponentClient } from "@supabase/auth-helpers-nextjs";
import { cookies } from "next/headers";
import { cache } from "react";

console.log("SUPABASE_URL: " + process.env.NEXT_PUBLIC_SUPABASE_URL);
console.log("SUPABASE_ANON_KEY: " + process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY);

// Check if Supabase environment variables are available
export const isSupabaseConfigured =
	typeof process.env.NEXT_PUBLIC_SUPABASE_URL === "string" &&
	process.env.NEXT_PUBLIC_SUPABASE_URL.length > 0 &&
	typeof process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY === "string" &&
	process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY.length > 0;

// Create a cached version of the Supabase client for Server Components
export const createClient = cache(() => {
	const cookieStore = cookies();

	if (!isSupabaseConfigured) {
		console.warn(
			"Supabase environment variables are not set. Using dummy client."
		);
		return {
			auth: {
				getUser: () =>
					Promise.resolve({ data: { user: null }, error: null }),
				getSession: () =>
					Promise.resolve({ data: { session: null }, error: null }),
			},
		};
	}

	return createServerComponentClient({ cookies: () => cookieStore });
});
