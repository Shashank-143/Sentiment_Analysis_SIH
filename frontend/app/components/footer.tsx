"use client";

import { IconBrandGithub } from "@tabler/icons-react";

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


                    {/* External social icons */}
                    <a
                        href="https://github.com/Shashank-143/Sentiment_Analysis_SIH"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-gray-500 transition hover:text-gray-900"
                    >
                        <IconBrandGithub size={20} />
                    </a>

                </div>
            </div>
        </footer>
    );
}
