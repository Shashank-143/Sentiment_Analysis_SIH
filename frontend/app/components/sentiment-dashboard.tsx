"use client";

import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { cn } from "@/lib/utils";
import WordCloud from "./word-cloud";
import FileUpload from "./file-upload";
import { analyzeSentiment, generateSummary, SentimentResult } from "@/services/api";

// --- Sentiment Pill ---
const SentimentPill = ({ 
    sentiment, 
    score 
}: { 
    sentiment: "Positive" | "Neutral" | "Negative"; 
    score?: number 
}) => {
    const colors: Record<string, string> = {
        Positive: "bg-emerald-100 text-emerald-700",
        Neutral: "bg-gray-100 text-gray-700",
        Negative: "bg-rose-100 text-rose-700",
    };

    return (
        <span
            className={cn(
                "px-3 py-1 rounded-full text-sm font-medium",
                colors[sentiment] || "bg-gray-100 text-gray-700"
            )}
        >
            {sentiment}{score !== undefined && ` (${score.toFixed(2)})`}
        </span>
    );
};

// Interface for feedback items
interface FeedbackItem {
    text: string; 
    sentiment: "Positive" | "Neutral" | "Negative";
    score?: number;
}

// --- Main Dashboard ---
export default function SentimentDashboard() {
    const [feedback, setFeedback] = useState("");
    const [submittedFeedback, setSubmittedFeedback] = useState<FeedbackItem[]>([]);
    const [isLoading, setIsLoading] = useState(false);
    const [summary, setSummary] = useState<string[]>([]);

    const handleSubmit = async () => {
        if (!feedback.trim()) return;
        
        setIsLoading(true);
        
        try {
            // Get sentiment analysis
            const sentimentResult = await analyzeSentiment(feedback);
            
            // Map API sentiment labels to UI labels
            const sentimentLabel = sentimentResult.sentiment_label === "POSITIVE" ? "Positive" : 
                                  sentimentResult.sentiment_label === "NEGATIVE" ? "Negative" : "Neutral";
            
            // Add new feedback with sentiment analysis
            const newFeedback: FeedbackItem = {
                text: feedback,
                sentiment: sentimentLabel as "Positive" | "Neutral" | "Negative",
                score: sentimentResult.sentiment_score
            };
            
            setSubmittedFeedback([newFeedback, ...submittedFeedback]);
            
            // Generate summary if this is the first feedback or periodically
            if (submittedFeedback.length === 0 || submittedFeedback.length % 3 === 0) {
                const allText = [feedback, ...submittedFeedback.map(f => f.text)].join(" ");
                const summaryResult = await generateSummary(allText);
                if (summaryResult.summary) {
                    // Split the summary into bullet points
                    const bulletPoints = summaryResult.summary
                        .split('.')
                        .filter(point => point.trim().length > 0)
                        .map(point => point.trim());
                    
                    setSummary(bulletPoints);
                }
            }
            
            setFeedback("");
        } catch (error) {
            console.error("Error processing feedback:", error);
        } finally {
            setIsLoading(false);
        }
    };

    // --- Group by sentiment ---
    const positives = submittedFeedback.filter((f) => f.sentiment === "Positive");
    const neutrals = submittedFeedback.filter((f) => f.sentiment === "Neutral");
    const negatives = submittedFeedback.filter((f) => f.sentiment === "Negative");

    return (
        <section className="min-h-screen bg-white text-gray-900 p-8 mt-10">
            {/* Header */}
            <div className="max-w-3xl mx-auto text-center mb-12">
                <h1 className="text-3xl font-semibold">Sentiment Analysis of Comments</h1>
                <p className="text-gray-600 mt-2">
                    Analyze public feedback with AI-powered sentiment detection, helping decision-makers
                    understand opinions and improve consultation outcomes.
                </p>
            </div>

            {/* Input */}
            <div className="max-w-3xl mx-auto mb-12 flex flex-col gap-4">
                <div className="flex gap-2 h-14">
                    <Input
                        value={feedback}
                        onChange={(e) => setFeedback(e.target.value)}
                        placeholder="Write your comment..."
                        className="flex-1 h-full"
                        disabled={isLoading}
                    />
                    <Button 
                        onClick={handleSubmit} 
                        className="h-full flex-shrink-0"
                        disabled={isLoading || !feedback.trim()}
                    >
                        {isLoading ? 'Analyzing...' : 'Submit'}
                    </Button>
                </div>
                <FileUpload />
            </div>

            {/* Dashboard */}
            <div className="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Word Cloud */}
                <Card>
                    <CardHeader>
                        <CardTitle>Word Cloud</CardTitle>
                    </CardHeader>
                    <CardContent className="max-h-[500px] overflow-y-auto">
                        <WordCloud feedback={submittedFeedback} />
                    </CardContent>
                </Card>

                {/* Sentiment Analysis */}
                <Card>
                    <CardHeader>
                        <CardTitle>Feedback Overview</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-6 max-h-[500px] overflow-y-auto">
                        {/* Positive */}
                        <div>
                            <h3 className="text-sm font-medium text-gray-700 mb-2">Positive Feedback</h3>
                            <div className="flex flex-wrap gap-2">
                                {positives.length
                                    ? positives.map((f, i) => (
                                        <SentimentPill key={i} sentiment="Positive" score={f.score} />
                                      ))
                                    : <p className="text-gray-400 text-xs">No positive feedback yet.</p>}
                            </div>
                        </div>

                        {/* Neutral */}
                        <div>
                            <h3 className="text-sm font-medium text-gray-700 mb-2">Neutral Feedback</h3>
                            <div className="flex flex-wrap gap-2">
                                {neutrals.length
                                    ? neutrals.map((f, i) => (
                                        <SentimentPill key={i} sentiment="Neutral" score={f.score} />
                                      ))
                                    : <p className="text-gray-400 text-xs">No neutral feedback yet.</p>}
                            </div>
                        </div>

                        {/* Negative */}
                        <div>
                            <h3 className="text-sm font-medium text-gray-700 mb-2">Negative Feedback</h3>
                            <div className="flex flex-wrap gap-2">
                                {negatives.length
                                    ? negatives.map((f, i) => (
                                        <SentimentPill key={i} sentiment="Negative" score={f.score} />
                                      ))
                                    : <p className="text-gray-400 text-xs">No negative feedback yet.</p>}
                            </div>
                        </div>

                        {/* Top Points */}
                        <div>
                            <h3 className="text-sm font-medium text-gray-700 mb-2">Top Points</h3>
                            <ul className="list-disc pl-5 text-gray-600 space-y-1 text-sm">
                                {submittedFeedback.length === 0 && summary.length === 0 ? (
                                    <li>Submit feedback to see summary points</li>
                                ) : summary.length > 0 ? (
                                    summary.map((point, i) => <li key={i}>{point}</li>)
                                ) : (
                                    submittedFeedback.slice(0, 5).map((f, i) => <li key={i}>{f.text}</li>)
                                )}
                            </ul>
                        </div>
                    </CardContent>
                </Card>
            </div>
        </section>
    );
}
