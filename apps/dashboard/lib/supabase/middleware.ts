import { createServerClient } from "@supabase/ssr";
import { NextResponse, type NextRequest } from "next/server";

// Check if Supabase environment variables are available
export const isSupabaseConfigured =
	typeof process.env.NEXT_PUBLIC_SUPABASE_URL === "string" &&
	process.env.NEXT_PUBLIC_SUPABASE_URL.length > 0 &&
	typeof process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY === "string" &&
	process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY.length > 0;

interface SupabaseCookie {
	name: string;
	value: string;
	options?: { [key: string]: unknown };
}

export async function updateSession(request: NextRequest) {
	// If Supabase is not configured, just continue without auth
	if (!isSupabaseConfigured) {
		return NextResponse.next({
			request,
		});
	}

	const res = NextResponse.next();

	// Create a Supabase client configured to use cookies
	const supabase = createServerClient(
		process.env.NEXT_PUBLIC_SUPABASE_URL!,
		process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
		{
			cookies: {
				/**
				 * Read all cookies from the incoming request
				 */
				getAll() {
					return request.cookies.getAll();
				},
				/**
				 * Persist a set of cookies so that the browser and server stay in sync.
				 * We mirror writes to the outgoing `Response` object so that the client
				 * receives updated auth cookies.
				 */
				setAll(cookies: SupabaseCookie[]) {
					cookies.forEach(({ name, value, options }) => {
						// Update cookie on the response
						res.cookies.set(name, value, options);
					});
				},
			},
		}
	);

	// Check if this is an auth callback
	const requestUrl = new URL(request.url);
	const code = requestUrl.searchParams.get("code");

	if (code) {
		// Exchange the code for a session
		await supabase.auth.exchangeCodeForSession(code);
		// Redirect to home page after successful auth
		return NextResponse.redirect(new URL("/", request.url));
	}

	// Refresh session if expired - required for Server Components
	await supabase.auth.getSession();

	// Protected routes - redirect to login if not authenticated
	const isAuthRoute =
		request.nextUrl.pathname.startsWith("/auth/login") ||
		request.nextUrl.pathname.startsWith("/auth/sign-up") ||
		request.nextUrl.pathname === "/auth/callback";

	if (!isAuthRoute) {
		const {
			data: { session },
		} = await supabase.auth.getSession();

		if (!session) {
			const redirectUrl = new URL("/auth/login", request.url);
			return NextResponse.redirect(redirectUrl);
		}
	}

	return res;
}
