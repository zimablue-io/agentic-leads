import type React from "react";
import type { Metadata } from "next";
import { Geist } from "next/font/google";
import "./globals.css";

// Sidebar components
import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";
import { AppSidebar } from "@/components/app-sidebar";

const geist = Geist({
	subsets: ["latin"],
});

export const metadata: Metadata = {
	title: "Supabase Auth with SSR",
	description: "A Next.js application with Supabase authentication using SSR",
	generator: "v0.dev",
};

export default function RootLayout({
	children,
}: {
	children: React.ReactNode;
}) {
	return (
		<html lang="en">
			<body className={geist.className}>
				{/* Sidebar layout wrapper */}
				<SidebarProvider className="flex min-h-screen">
					{/* Application sidebar */}
					<AppSidebar />

					{/* Main content area */}
					<main className="flex-1">
						{/* Optional floating trigger for collapsed sidebar */}
						<SidebarTrigger className="m-2" />
						{children}
					</main>
				</SidebarProvider>
			</body>
		</html>
	);
}
