"use client";

import Link from "next/link";
import { IconBrandGithub, IconBrandTwitter, IconMail } from "@tabler/icons-react";

export default function Footer() {
    return (
        <footer className="w-full border-t border-gray-200 bg-white">
            <div className="mx-auto flex max-w-6xl flex-col items-center justify-between gap-4 px-6 py-8 md:flex-row">
                {/* Left: Brand / Copyright */}
                <p className="text-sm text-gray-500">
                    © {new Date().getFullYear()} SentimentAI. All rights reserved.
                </p>

                {/* Right: Navigation / Social Links */}
                <div className="flex gap-4 items-center">
                    {/* Internal links using Next.js Link */}
                    <Link href="/about" className="text-gray-500 transition hover:text-gray-900 text-sm">
                        About
                    </Link>
                    <Link href="/contact" className="text-gray-500 transition hover:text-gray-900 text-sm">
                        Contact
                    </Link>
                    <Link href="/privacy" className="text-gray-500 transition hover:text-gray-900 text-sm">
                        Privacy
                    </Link>

                    {/* External social icons */}
                    <a
                        href="https://github.com/"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-gray-500 transition hover:text-gray-900"
                    >
                        <IconBrandGithub size={20} />
                    </a>
                    <a
                        href="https://twitter.com/"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-gray-500 transition hover:text-gray-900"
                    >
                        <IconBrandTwitter size={20} />
                    </a>
                    <a
                        href="mailto:hello@example.com"
                        className="text-gray-500 transition hover:text-gray-900"
                    >
                        <IconMail size={20} />
                    </a>
                </div>
            </div>
        </footer>
    );
}
