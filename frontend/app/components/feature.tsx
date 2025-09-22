import { cn } from "@/lib/utils";
import {
    IconAdjustmentsBolt,
    IconCloud,
    IconCurrencyDollar,
    IconEaseInOut,
    IconHeart,
    IconHelp,
    IconRouteAltLeft,
    IconTerminal2,
} from "@tabler/icons-react";

export function FeaturesSectionDemo() {
    const features = [
        {
            title: "Sentiment Analysis",
            description:
                "Analyze public feedback with AI-powered sentiment detection, helping decision-makers understand opinions.",
            icon: <IconTerminal2 />,
        },
        {
            title: "E-Consultation Modules",
            description:
                "Enable online consultations with structured AI support, making expert guidance accessible anytime.",
            icon: <IconEaseInOut />,
        },
        {
            title: "Public Feedback Insights",
            description:
                "Collect and summarize opinions from multiple sources to improve policy and service outcomes.",
            icon: <IconCurrencyDollar />,
        },
        {
            title: "Automated Reporting",
            description:
                "Generate comprehensive reports on trends, sentiment, and engagement automatically.",
            icon: <IconCloud />,
        },
        {
            title: "Data Security",
            description:
                "All feedback and consultations are securely handled with privacy-first protocols.",
            icon: <IconRouteAltLeft />,
        },
        {
            title: "24/7 AI Assistance",
            description:
                "Our AI agents provide real-time help and guidance around the clock.",
            icon: <IconHelp />,
        },
        {
            title: "Actionable Recommendations",
            description:
                "Receive AI-driven suggestions to act on feedback and improve consultation outcomes.",
            icon: <IconAdjustmentsBolt />,
        },
        {
            title: "Comprehensive Coverage",
            description:
                "From sentiment detection to reporting, all tools are integrated for seamless decision-making.",
            icon: <IconHeart />,
        },
    ];

    return (
        <div className="max-w-7xl mx-auto py-10">
            <h2 className="text-3xl font-bold text-center mb-10 text-neutral-900 dark:text-neutral-100">
                How We Can Help You
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
