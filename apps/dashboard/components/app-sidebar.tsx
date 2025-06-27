"use client";

import Link from "next/link";
import {
	Sidebar,
	SidebarContent,
	SidebarGroup,
	SidebarGroupContent,
	SidebarGroupLabel,
	SidebarMenu,
	SidebarMenuButton,
	SidebarMenuItem,
} from "@/components/ui/sidebar";
import { LayoutDashboard, Globe2, Users, Settings } from "lucide-react";

// Core navigation items for sidebar
const navItems = [
	{ title: "Dashboard", url: "/", icon: LayoutDashboard },
	{ title: "Prospects", url: "/prospects", icon: Globe2 },
	{ title: "Audiences", url: "/audiences", icon: Users },
	{ title: "Settings", url: "/settings", icon: Settings },
];

export function AppSidebar() {
	return (
		<Sidebar className="border-r border-border">
			<SidebarContent>
				<SidebarGroup>
					<SidebarGroupLabel>Navigation</SidebarGroupLabel>
					<SidebarGroupContent>
						<SidebarMenu>
							{navItems.map((item) => (
								<SidebarMenuItem key={item.title}>
									<SidebarMenuButton asChild>
										<Link
											href={item.url}
											className="flex items-center gap-2"
										>
											<item.icon className="size-4" />
											<span>{item.title}</span>
										</Link>
									</SidebarMenuButton>
								</SidebarMenuItem>
							))}
						</SidebarMenu>
					</SidebarGroupContent>
				</SidebarGroup>
			</SidebarContent>
		</Sidebar>
	);
}
