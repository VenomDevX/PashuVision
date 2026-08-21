import type { Metadata } from "next";
import "./globals.css";
import Navbar from "@/components/Navbar";
import { LanguageProvider } from "@/context/LanguageContext";

export const metadata: Metadata = {
  title: "PashuDrishti – AI-Based Cattle and Buffalo Identification",
  description: "AI-powered livestock breed classification",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased bg-gray-50 min-h-screen flex flex-col">
        <LanguageProvider>
          <Navbar />
          <main className="flex-grow">
            {children}
          </main>
        </LanguageProvider>
      </body>
    </html>
  );
}
