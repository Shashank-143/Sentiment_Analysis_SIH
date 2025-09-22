"use client";
import { Bolt } from "lucide-react";
import WrapButton from "../wrap-button";
import { ThreeDMarquee } from "./3-d-marquee";

export function ThreeDMarqueeDemoSecond() {
    const images = [
        "/siri.png",
        "/prism.png",
        "/opensource2.png",
        "/sphere.png",
        "/siri.png",
        "/siri.png",
        "/siri.png",
        "/ice.png",
        "/earth.jpeg",
        "/siri.png",
        "/stylesleep.jpeg",
        "/siri.png",
        "/siri.png",
        "/colours.png",
        "/colours.png",
        "/colours.png",

        "/siri.png",
        "/siri.png",
        "/siri.png",
        "/siri.png",
        "/siri.png",
        "/siri.png",
        "/siri.png",
        "/sphere.png",
        "/siri.png",
        "/siri.png",
        "/siri.png",
        "/siri.png",
        "/siri.png",
        "/siri.png",
        "/sphere.png",
    ];

    return (
        <div className="relative flex h-screen w-screen flex-col items-center justify-center overflow-hidden ">
            <h2 className="relative z-20 mx-auto max-w-4xl text-center text-2xl font-bold text-white md:text-4xl lg:text-6xl">
                Sentiment analysis of comments {" "}
                <span className="relative z-20 inline-block rounded-xl bg-blue-500/40 px-4 py-1 text-white underline decoration-sky-500 decoration-[6px] underline-offset-[16px] backdrop-blur-sm">
                    E-consultation modules
                </span>{" "}



            </h2>
            <p className="relative z-20 mx-auto max-w-2xl py-8 text-center text-sm text-neutral-200 md:text-base">
                Analyze public feedback with AI-powered sentiment detection, helping decision-makers
                understand opinions and improve consultation outcomes.
            </p>

            <div className="relative z-20 flex flex-wrap items-center justify-center gap-4 pt-4">
                <WrapButton
                    href="/dashboard"
                    innerClass="bg-[#17ffc1] text-black"
                    arrowClass="text-[#00ffea] border-[#00fff2]"
                >
                    <Bolt className="animate-spin w-4 h-4 sm:w-5 sm:h-5 lg:w-6 lg:h-6" />
                    Get Started
                </WrapButton>
            </div>

            {/* overlay */}
            <div className="absolute inset-0 z-10 h-full w-full bg-black/80" />
            <ThreeDMarquee
                className="pointer-events-none absolute inset-0 h-full w-full"
                images={images}
            />
        </div>
    );
}
