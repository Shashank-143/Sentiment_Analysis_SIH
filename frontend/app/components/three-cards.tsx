import React from 'react';
import { File, Brain, Sparkles } from 'lucide-react';

interface FeatureProps {
    icon: React.ReactNode;
    title: string;
    description: string;
    glowColor: string;
    accentColor: string;
}

const Feature: React.FC<FeatureProps> = ({ icon, title, description, glowColor, accentColor }) => {
    return (
        <div className="flex flex-col items-center text-center p-6 ">
            <div className="relative mb-10">
                {/* Icon container with static styling */}
                <div
                    className="relative z-10 bg-black rounded-full p-6 border-2 shadow-xl"
                    style={{ borderColor: `${accentColor}B3` }} // B3 = 70% opacity
                >
                    <div style={{ color: accentColor }}>{icon}</div>
                </div>
                {/* Static glow effects */}
                <div
                    className="absolute -inset-2 rounded-full opacity-40 blur-xl"
                    style={{ backgroundColor: glowColor }}
                />
                <div
                    className="absolute -inset-4 rounded-full opacity-20 blur-2xl"
                    style={{ backgroundColor: accentColor }}
                />
            </div>

            {/* Text with static gradient */}
            <h3
                className="text-2xl md:text-3xl font-bold mb-4 text-white bg-clip-text text-transparent"
                style={{
                    backgroundImage: `linear-gradient(to right, ${accentColor}, ${glowColor})`,
                }}
            >
                {title}
            </h3>
            <p className="text-lg max-w-md" style={{ color: `${accentColor}CC` }}>
                {description}
            </p>
        </div>
    );
};

const FeatureGrid: React.FC = () => {
    const features = [
        {
            icon: <File size={32} />,
            title: "Sentiment Analysis",
            description:
                "Analyze public feedback with AI-powered sentiment detection, helping decision-makers understand opinions and improve consultation outcomes.",
            glowColor: "#f97316",
            accentColor: "#fb923c",
        },
        {
            icon: <Brain size={32} />,
            title: "Comprehensive Feedback Review",
            description:
                "AI-assisted tools ensure every comment on draft legislation is carefully analysed, so no observation is overlooked.",
            glowColor: "#06b6d4",
            accentColor: "#22d3ee",
        },


        {
            icon: <Sparkles size={32} />,
            title: "Insights from Comments",
            description:
                "Leverage existing public feedback without creating new silos—extract key themes and actionable insights directly from citizen input.",
            glowColor: "#a855f7",
            accentColor: "#c084fc",
        },
    ];

    return (
        <div className="w-full relative px-6 overflow-hidden bg-black pb-10">
            {/* Static background patterns */}
            <div className="absolute top-0 left-0 w-full h-full opacity-10">
                <div
                    className="absolute top-1/4 left-1/4 w-32 h-32 rounded-full blur-3xl"
                    style={{ backgroundColor: "#f97316" }}
                />
                <div
                    className="absolute bottom-1/3 right-1/4 w-40 h-40 rounded-full blur-3xl"
                    style={{ backgroundColor: "#06b6d4" }}
                />
                <div
                    className="absolute top-2/3 right-1/3 w-24 h-24 rounded-full blur-3xl"
                    style={{ backgroundColor: "#a855f7" }}
                />
            </div>

            <div className="max-w-6xl mx-auto relative z-10">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-12">
                    {features.map((feature, index) => (
                        <div
                            key={index}
                            className="relative bg-gray-900 bg-opacity-20 backdrop-blur-sm rounded-xl p-6 border border-gray-800 shadow-2xl overflow-hidden"
                            style={{ borderColor: `${feature.glowColor}50` }}
                        >
                            {/* Static border glow */}
                            <div
                                className="absolute -inset-0.5 rounded-xl border-2 blur-sm"
                                style={{ borderColor: `${feature.glowColor}80` }}
                            />

                            {/* Static corner glow */}
                            <div
                                className="absolute -top-2 -right-2 w-16 h-16 rounded-full opacity-30 blur-2xl"
                                style={{ backgroundColor: feature.glowColor }}
                            />

                            <Feature
                                icon={feature.icon}
                                title={feature.title}
                                description={feature.description}
                                glowColor={feature.glowColor}
                                accentColor={feature.accentColor}
                            />
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default FeatureGrid;
