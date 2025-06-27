"use server";

import { createServerClient } from "@supabase/ssr";
import { cookies } from "next/headers";
import { redirect } from "next/navigation";
// DB helpers (server-side only)
import { queueProspectingJob } from "@agentic-leads/db";

// Update the signIn function to handle redirects properly
export async function signIn(prevState: any, formData: FormData) {
	// Check if formData is valid
	if (!formData) {
		return { error: "Form data is missing" };
	}

	const email = formData.get("email");
	const password = formData.get("password");

	// Validate required fields
	if (!email || !password) {
		return { error: "Email and password are required" };
	}

	const store = await cookies();
	const supabase = createServerClient(
		process.env.NEXT_PUBLIC_SUPABASE_URL!,
		process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
		{
			cookies: {
				get(name: string) {
					return store.get(name)?.value;
				},
				set(
					name: string,
					value: string,
					options?: Record<string, unknown>
				) {
					store.set({ name, value, ...options });
				},
				remove(name: string, options?: Record<string, unknown>) {
					store.set({ name, value: "", ...options });
				},
			},
		}
	);

	try {
		const { error } = await supabase.auth.signInWithPassword({
			email: email.toString(),
			password: password.toString(),
		});

		if (error) {
			return { error: error.message };
		}

		// Return success instead of redirecting directly
		return { success: true };
	} catch (error) {
		console.error("Login error:", error);
		return { error: "An unexpected error occurred. Please try again." };
	}
}

// Update the signUp function to handle potential null formData
export async function signUp(prevState: any, formData: FormData) {
	// Check if formData is valid
	if (!formData) {
		return { error: "Form data is missing" };
	}

	const email = formData.get("email");
	const password = formData.get("password");

	// Validate required fields
	if (!email || !password) {
		return { error: "Email and password are required" };
	}

	const store = await cookies();
	const supabase = createServerClient(
		process.env.NEXT_PUBLIC_SUPABASE_URL!,
		process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
		{
			cookies: {
				get(name: string) {
					return store.get(name)?.value;
				},
				set(
					name: string,
					value: string,
					options?: Record<string, unknown>
				) {
					store.set({ name, value, ...options });
				},
				remove(name: string, options?: Record<string, unknown>) {
					store.set({ name, value: "", ...options });
				},
			},
		}
	);

	try {
		const { error } = await supabase.auth.signUp({
			email: email.toString(),
			password: password.toString(),
		});

		if (error) {
			return { error: error.message };
		}

		return { success: "Check your email to confirm your account." };
	} catch (error) {
		console.error("Sign up error:", error);
		return { error: "An unexpected error occurred. Please try again." };
	}
}

export async function signOut() {
	const store = await cookies();
	const supabase = createServerClient(
		process.env.NEXT_PUBLIC_SUPABASE_URL!,
		process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
		{
			cookies: {
				get(name: string) {
					return store.get(name)?.value;
				},
				set(
					name: string,
					value: string,
					options?: Record<string, unknown>
				) {
					store.set({ name, value, ...options });
				},
				remove(name: string, options?: Record<string, unknown>) {
					store.set({ name, value: "", ...options });
				},
			},
		}
	);

	await supabase.auth.signOut();
	redirect("/auth/login");
}

export async function startProspectingRun(formData: FormData) {
	"use server";

	const audienceId = formData.get("audience")?.toString();
	const location = formData.get("location")?.toString() || "";
	const max = parseInt(formData.get("max")?.toString() || "5", 10);

	if (!audienceId || !location) {
		throw new Error("Audience and location are required");
	}

	const run = await queueProspectingJob(audienceId, location, max);
	console.log("Queued run", run!.id);
	// No redirect; page will revalidate via realtime
}
