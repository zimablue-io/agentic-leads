import type React from "react";

// Sidebar components
import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";
import { AppSidebar } from "@/components/app-sidebar";

export default function AuthenticatedLayout({
	children,
}: {
	children: React.ReactNode;
}) {
	return (
		<>
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
		</>
	);
}
