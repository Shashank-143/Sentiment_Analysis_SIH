"use client";

import * as React from "react";
import { motion } from "framer-motion";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import Link from "next/link";

interface HeroAction {
    label: string;
    href: string;
    variant?: "link" | "outline" | "default" | "destructive" | "secondary" | "ghost";
}

interface HeroProps extends React.HTMLAttributes<HTMLElement> {
    gradient?: boolean;
    blur?: boolean;
    title?: string;
    subtitle?: string;
    actions?: HeroAction[];
    titleClassName?: string;
    subtitleClassName?: string;
    actionsClassName?: string;
}

const LampComponent = React.forwardRef<HTMLElement, HeroProps>(
    (
        {
            className,
            gradient = true,
            blur = true,
            title = "Experience the Future",
            subtitle = "Discover innovative solutions designed to transform your world.",
            actions = [{ label: "Learn More", href: "#", variant: "default" }],
            titleClassName,
            subtitleClassName,
            actionsClassName,
            ...props
        },
        ref
    ) => {
        return (
            <section
                ref={ref}
                className={cn(
                    "relative z-0 flex min-h-[75vh] w-full flex-col items-center justify-start overflow-hidden bg-black",
                    className
                )}
                {...props}
            >
                {gradient && (
                    <div className="absolute top-28 isolate z-0 flex w-screen flex-1 items-start justify-center">
                        {blur && (
                            <div className="absolute top-0 z-50 h-48 w-screen bg-transparent opacity-10 backdrop-blur-md" />
                        )}

                        {/* Main glow */}
                        <div className="absolute inset-auto z-50 h-36 w-[28rem] -translate-y-1/4 rounded-full bg-teal-400/50 opacity-80 blur-3xl" />

                        {/* Lamp effect */}
                        <motion.div
                            initial={{ width: "8rem" }}
                            viewport={{ once: true }}
                            transition={{ ease: "easeInOut", delay: 0.3, duration: 0.8 }}
                            whileInView={{ width: "16rem" }}
                            className="absolute top-16 z-30 h-36 -translate-y-[20%] rounded-full bg-teal-400/50 blur-2xl"
                        />

                        {/* Top line */}
                        <motion.div
                            initial={{ width: "15rem" }}
                            viewport={{ once: true }}
                            transition={{ ease: "easeInOut", delay: 0.3, duration: 0.8 }}
                            whileInView={{ width: "30rem" }}
                            className="absolute inset-auto z-50 h-0.5 -translate-y-1/12 bg-teal-400/80"
                        />

                        {/* Left gradient cone */}
                        <motion.div
                            initial={{ opacity: 0.5, width: "15rem" }}
                            whileInView={{ opacity: 1, width: "30rem" }}
                            transition={{
                                delay: 0.3,
                                duration: 0.8,
                                ease: "easeInOut",
                            }}
                            style={{
                                backgroundImage: `conic-gradient(var(--conic-position), var(--tw-gradient-stops))`,
                            }}
                            className="absolute inset-auto right-1/2 h-56 w-[30rem] bg-gradient-conic from-teal-400/60 via-transparent to-transparent [--conic-position:from_70deg_at_center_top]"
                        >
                            <div className="absolute w-[100%] left-0 bg-black h-40 bottom-0 z-20 [mask-image:linear-gradient(to_top,white,transparent)]" />
                            <div className="absolute w-40 h-[100%] left-0 bg-black bottom-0 z-20 [mask-image:linear-gradient(to_right,white,transparent)]" />
                        </motion.div>

                        {/* Right gradient cone */}
                        <motion.div
                            initial={{ opacity: 0.5, width: "15rem" }}
                            whileInView={{ opacity: 1, width: "30rem" }}
                            transition={{
                                delay: 0.3,
                                duration: 0.8,
                                ease: "easeInOut",
                            }}
                            style={{
                                backgroundImage: `conic-gradient(var(--conic-position), var(--tw-gradient-stops))`,
                            }}
                            className="absolute inset-auto left-1/2 h-56 w-[30rem] bg-gradient-conic from-transparent via-transparent to-teal-400/60 [--conic-position:from_290deg_at_center_top]"
                        >
                            <div className="absolute w-40 h-[100%] right-0 bg-black bottom-0 z-20 [mask-image:linear-gradient(to_left,white,transparent)]" />
                            <div className="absolute w-[100%] right-0 bg-black h-40 bottom-0 z-20 [mask-image:linear-gradient(to_top,white,transparent)]" />
                        </motion.div>
                    </div>
                )}

                {/* Main content */}
                <motion.div
                    initial={{ y: 120, opacity: 0 }}
                    viewport={{ once: true }}
                    transition={{ ease: "easeInOut", delay: 0.3, duration: 0.8 }}
                    whileInView={{ y: 0, opacity: 1 }}
                    className="relative z-50 container flex justify-center flex-1 flex-col px-5 md:px-10 gap-4 -translate-y-36"
                >
                    <div className="flex flex-col items-center text-center space-y-6">
                        <h1
                            className={cn(
                                "text-5xl sm:text-6xl md:text-7xl lg:text-8xl font-semibold tracking-tight text-white",
                                titleClassName
                            )}
                        >
                            {title}
                        </h1>
                        {subtitle && (
                            <p
                                className={cn(
                                    "text-xl md:text-2xl text-gray-400 font-light max-w-2xl leading-relaxed",
                                    subtitleClassName
                                )}
                            >
                                {subtitle}
                            </p>
                        )}
                        {actions && actions.length > 0 && (
                            <div className={cn("flex gap-4 mt-8", actionsClassName)}>
                                {actions.map((action, index) => (
                                    <Link key={index} href={action.href}>
                                        <Button className="relative overflow-hidden px-8 py-6 rounded-full tracking-wide uppercase font-medium bg-teal-500 hover:bg-teal-600 text-white duration-300 transition-all shadow-lg hover:shadow-teal-500/30">
                                            <span className="relative z-10">{action.label}</span>
                                        </Button>
                                    </Link>
                                ))}
                            </div>
                        )}
                    </div>
                </motion.div>
            </section>
        );
    }
);

LampComponent.displayName = "LampComponent";

export default LampComponent;
