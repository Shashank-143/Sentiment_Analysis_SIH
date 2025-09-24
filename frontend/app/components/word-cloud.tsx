"use client";

import { useState, useEffect } from "react";
import { getWordCloudUrl } from "@/services/api";

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
    const [wordCloudUrl, setWordCloudUrl] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState<boolean>(false);

    useEffect(() => {
        if (!feedback || !feedback.length) {
            setWords([]);
            setWordCloudUrl(null);
            return;
        }

        setIsLoading(true);
        
        // Combine all feedback texts
        const allText = feedback
            .filter(item => item && item.text && typeof item.text === "string")
            .map(item => item.text.trim())
            .join(" ");
            
        // If we have text, generate a word cloud
        if (allText) {
            setWordCloudUrl(getWordCloudUrl(allText));
            
            // Also prepare the client-side fallback
            const processed = feedback
                .filter(item => item && item.text && typeof item.text === "string")
                .map(item => ({
                    text: item.text.trim(),
                    value: Math.floor(Math.random() * 20) + 10, 
                }))
                .filter(word => word.text.length > 0);
                
            setWords(processed);
        }
        
        setIsLoading(false);
    }, [feedback]);

    return (
        <div className="h-[400px] w-full flex justify-center items-center">
            {isLoading ? (
                <div className="text-gray-500">Loading word cloud...</div>
            ) : wordCloudUrl ? (
                <div className="relative w-full h-full">
                    <img
                        src={wordCloudUrl}
                        alt="Word Cloud"
                        className="max-w-full max-h-full object-contain mx-auto"
                        onError={() => {
                            setWordCloudUrl(null);
                        }}
                    />
                </div>
            ) : (
                <MockWordCloud words={words} />
            )}
        </div>
    );
};

export default WordCloud;