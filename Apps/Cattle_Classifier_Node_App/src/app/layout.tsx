import type { Metadata, Viewport } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { Navigation } from "@/components/Navigation";
import { Footer } from "@/components/Footer";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
  display: "swap",
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
  display: "swap",
});

export const metadata: Metadata = {
  title: {
    default: "SIH 2026 - Indian Cattle Breed Classification",
    template: "%s | SIH 2026 Cattle Classifier",
  },
  description: "AI-powered livestock identification for smart agriculture. End-to-end deep learning solution for automated classification of Indian cattle breeds using EfficientNet-B0 transfer learning.",
  keywords: [
    "SIH 2026",
    "Smart India Hackathon",
    "cattle breed classification",
    "deep learning",
    "EfficientNet-B0",
    "transfer learning",
    "computer vision",
    "agriculture AI",
    "livestock identification",
  ],
  authors: [{ name: "Team SIH 2026" }],
  creator: "Team SIH 2026",
  publisher: "Smart India Hackathon 2026",
  robots: "index, follow",
  openGraph: {
    type: "website",
    locale: "en_US",
    url: "https://sih2026-cattle-classifier.vercel.app",
    title: "SIH 2026 - Indian Cattle Breed Classification",
    description: "AI-powered livestock identification for smart agriculture",
    siteName: "SIH 2026 Cattle Classifier",
  },
  twitter: {
    card: "summary_large_image",
    title: "SIH 2026 - Indian Cattle Breed Classification",
    description: "AI-powered livestock identification for smart agriculture",
  },
  verification: {
    google: "google-site-verification-code",
  },
};

export const viewport: Viewport = {
  themeColor: [
    { media: "(prefers-color-scheme: light)", color: "#ffffff" },
    { media: "(prefers-color-scheme: dark)", color: "#0f172a" },
  ],
  width: "device-width",
  initialScale: 1,
  maximumScale: 5,
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html
      lang="en"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased scroll-smooth`}
      suppressHydrationWarning
    >
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
      </head>
      <body className="min-h-full flex flex-col bg-white dark:bg-slate-950 text-gray-900 dark:text-gray-100">
        <Navigation />
        <main className="flex-1 pt-16 md:pt-20">{children}</main>
        <Footer />
      </body>
    </html>
  );
}