import type React from "react";
import type { Metadata } from "next";
import { Geist } from "next/font/google";
import "./globals.css";

const geist = Geist({
	subsets: ["latin"],
});

export const metadata: Metadata = {
	title: "Lead Management",
	description: "Zima Blue's Lead Management System",
};

export default function RootLayout({
	children,
}: {
	children: React.ReactNode;
}) {
	return (
		<html lang="en">
			<body className={geist.className}>{children}</body>
		</html>
	);
}
