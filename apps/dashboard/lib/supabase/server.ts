import { createServerClient } from "@supabase/ssr";
import { cookies } from "next/headers";
import { cache } from "react";

// Check if Supabase environment variables are available
export const isSupabaseConfigured =
	typeof process.env.NEXT_PUBLIC_SUPABASE_URL === "string" &&
	process.env.NEXT_PUBLIC_SUPABASE_URL.length > 0 &&
	typeof process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY === "string" &&
	process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY.length > 0;

// Create a cached version of the Supabase client for Server Components
export const createClient = cache(async () => {
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

	const cookieStore = await cookies();
	return createServerClient(
		process.env.NEXT_PUBLIC_SUPABASE_URL!,
		process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
		{
			cookies: {
				getAll() {
					return cookieStore.getAll();
				},
				setAll(
					_cookies: { name: string; value: string; options?: any }[]
				) {
					// Server Components cannot modify cookies – middleware does that
				},
			},
		}
	);
});
