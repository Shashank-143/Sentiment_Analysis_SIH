"use client";

import { useState, useEffect } from "react";

interface WordCloudProps {
    feedback: { text: string; sentiment: string }[];
}

const MockWordCloud = ({ words }: { words: { text: string; value: number }[] }) => {
    if (!words || words.length === 0) {
        return (
            <div className="h-full w-full flex items-center justify-center text-gray-500">
                <p>No data available for word cloud</p>
            </div>
        );
    }

    return (
        <div className="h-full w-full flex items-center justify-center">
            <div className="text-center">
                <p className="text-sm text-gray-400 mb-2">Word Cloud Preview</p>
                <div className="flex flex-wrap gap-2 justify-center">
                    {words.slice(0, 10).map((word, index) => (
                        <span
                            key={index}
                            className="px-2 py-1 bg-blue-500/20 text-blue-400 rounded text-sm"
                            style={{ fontSize: `${word.value}px` }}
                        >
                            {word.text}
                        </span>
                    ))}
                </div>
                {words.length > 10 && (
                    <p className="text-xs text-gray-500 mt-2">+{words.length - 10} more words</p>
                )}
            </div>
        </div>
    );
};

const WordCloud = ({ feedback }: WordCloudProps) => {
    const [words, setWords] = useState<{ text: string; value: number }[]>([]);

    useEffect(() => {
        if (!feedback || !feedback.length) {
            setWords([]);
            return;
        }

        // Only generate random values on the client after mount
        const processed = feedback
            .filter(item => item && item.text && typeof item.text === "string")
            .map(item => ({
                text: item.text.trim(),
                value: Math.floor(Math.random() * 20) + 10, // random font size between 10-30
            }))
            .filter(word => word.text.length > 0);

        setWords(processed);
    }, [feedback]);

    return (
        <div className="h-[400px] w-full">
            <MockWordCloud words={words} />
        </div>
    );
};

export default WordCloud;
