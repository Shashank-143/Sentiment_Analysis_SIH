import { cn } from "@/lib/utils";
import {
    IconMoodHappy,
    IconMoodNeutral,
    IconReportAnalytics,
    IconChartBubble,
    IconMessageCircle,
    IconRobot,
} from "@tabler/icons-react";

export function FeaturesSectionDemo() {
    const features = [
        {
            title: "Sentiment Detection",
            description:
                "Classify feedback as Positive, Negative, or Neutral with AI-powered accuracy.",
            icon: <IconMoodHappy />,
        },
        {
            title: "Word Cloud Generation",
            description:
                "Visualize the most frequent keywords in feedback with dynamic word clouds.",
            icon: <IconChartBubble />,
        },
        {
            title: "Feedback Summarization",
            description:
                "AI summarizes large amounts of text into clear, concise insights.",
            icon: <IconReportAnalytics />,
        },
        {
            title: "Supports Excel Uploads",
            description:
                "Easily upload Excel files to process large volumes of feedback, enabling fast and accurate sentiment analysis at scale.",
            icon: <IconMoodNeutral />,
        },

        {
            title: "Resilient Multi-Model Design",
            description:
                "Core features like sentiment analysis, summarization, and keyword extraction have fallback mechanisms, ensuring uninterrupted operation even if external APIs are unavailable.",
            icon: <IconRobot />,
        },
        {
            title: "Real-time Analysis",
            description:
                "Get instant results as soon as you upload feedback or reports.",
            icon: <IconRobot />,
        },
        {
            title: "Engagement Monitoring",
            description:
                "Understand how people respond to policies, services, or products at scale.",
            icon: <IconMessageCircle />,
        },
        {
            title: "Completely Responsive",
            description:
                "Seamlessly adapts to all screen sizes, ensuring an optimal experience on desktops, tablets, and mobile devices without compromising on design or functionality.",
            icon: <IconReportAnalytics />,
        },

    ];

    return (
        <div className="max-w-7xl mx-auto py-10">
            <h2 className="text-3xl font-bold text-center mb-10 text-neutral-900 dark:text-neutral-100">
                How Our Sentiment AI Helps You
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 relative z-10">
                {features.map((feature, index) => (
                    <Feature key={feature.title} {...feature} index={index} />
                ))}
            </div>
        </div>
    );
}

const Feature = ({
    title,
    description,
    icon,
    index,
}: {
    title: string;
    description: string;
    icon: React.ReactNode;
    index: number;
}) => {
    return (
        <div
            className={cn(
                "flex flex-col lg:border-r py-10 relative group/feature dark:border-neutral-800",
                (index === 0 || index === 4) && "lg:border-l dark:border-neutral-800",
                index < 4 && "lg:border-b dark:border-neutral-800"
            )}
        >
            {index < 4 ? (
                <div className="opacity-0 group-hover/feature:opacity-100 transition duration-200 absolute inset-0 h-full w-full bg-gradient-to-t from-neutral-100 dark:from-neutral-800 to-transparent pointer-events-none" />
            ) : (
                <div className="opacity-0 group-hover/feature:opacity-100 transition duration-200 absolute inset-0 h-full w-full bg-gradient-to-b from-neutral-100 dark:from-neutral-800 to-transparent pointer-events-none" />
            )}
            <div className="mb-4 relative z-10 px-10 text-neutral-600 dark:text-neutral-400">
                {icon}
            </div>
            <div className="text-lg font-bold mb-2 relative z-10 px-10">
                <div className="absolute left-0 inset-y-0 h-6 group-hover/feature:h-8 w-1 rounded-tr-full rounded-br-full bg-neutral-300 dark:bg-neutral-700 group-hover/feature:bg-blue-500 transition-all duration-200 origin-center" />
                <span className="group-hover/feature:translate-x-2 transition duration-200 inline-block text-neutral-800 dark:text-neutral-100">
                    {title}
                </span>
            </div>
            <p className="text-sm text-neutral-600 dark:text-neutral-300 max-w-xs relative z-10 px-10">
                {description}
            </p>
        </div>
    );
};
