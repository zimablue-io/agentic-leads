"use client";

import { createBrowserClient } from "@supabase/ssr";

// Check if Supabase environment variables are available
export const isSupabaseConfigured =
	typeof process.env.NEXT_PUBLIC_SUPABASE_URL === "string" &&
	process.env.NEXT_PUBLIC_SUPABASE_URL.length > 0 &&
	typeof process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY === "string" &&
	process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY.length > 0;

// Singleton browser client
export const supabase = isSupabaseConfigured
	? createBrowserClient(
			process.env.NEXT_PUBLIC_SUPABASE_URL!,
			process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
		)
	: undefined;
