"use client";

import Link from "next/link";
import { useState } from "react";
import { Menu, X } from "lucide-react";

export function Navbar() {
    const [open, setOpen] = useState(false);

    return (
        <header className="fixed top-0 left-0 w-full z-50 border-b border-neutral-800 bg-white backdrop-blur-md">
            <div className="mx-auto flex h-14 max-w-7xl items-center justify-between px-4">
                {/* Logo */}
                <Link
                    href="/"
                    className="text-lg font-semibold tracking-tight text-black hover:text-cyan-400 transition-colors"
                >
                    Sentiment<span className="text-cyan-400">AI</span>
                </Link>



                {/* Mobile Toggle */}
                <button
                    onClick={() => setOpen(!open)}
                    className="md:hidden text-black hover:text-cyan-400 transition-colors"
                >
                    {open ? <X size={20} /> : <Menu size={20} />}
                </button>
            </div>

            {/* Mobile Menu */}
            {open && (
                <div className="md:hidden border-t border-neutral-800 bg-black/90 backdrop-blur-md">

                </div>
            )}
        </header>
    );
}
