"use client";

import * as React from "react";
import { Accordion as AccordionPrimitive } from "@base-ui-components/react/accordion";
import { IconChevronDown } from "@tabler/icons-react";
import { cn } from "@/lib/utils";

export interface AccordionProps {
    className?: string;
    openMultiple?: boolean;
    items?: Array<{
        value: string;
        trigger: string;
        content: React.ReactNode;
    }>;
    children?: React.ReactNode;
}

function Accordion({
    className,
    openMultiple = false,
    children,
    ...props
}: React.ComponentProps<typeof AccordionPrimitive.Root>) {
    return (
        <AccordionPrimitive.Root
            data-slot="accordion"
            openMultiple={openMultiple}
            className={cn("flex w-full max-w-2xl flex-col", className)}
            {...props}
        >
            {children}
        </AccordionPrimitive.Root>
    );
}

function AccordionItem({
    className,
    ...props
}: React.ComponentProps<typeof AccordionPrimitive.Item>) {
    return (
        <AccordionPrimitive.Item
            data-slot="accordion-item"
            className={cn("border-b border-gray-200 last:border-b-0 hover:bg-gray-50/50 transition-colors", className)}
            {...props}
        />
    );
}

function AccordionTrigger({
    className,
    children,
    ...props
}: React.ComponentProps<typeof AccordionPrimitive.Trigger>) {
    return (
        <AccordionPrimitive.Header data-slot="accordion-header">
            <AccordionPrimitive.Trigger
                data-slot="accordion-trigger"
                className={cn(
                    "flex w-full cursor-pointer items-center rounded-md py-4 text-left text-base font-medium text-gray-900 transition-all outline-none hover:underline [&[data-panel-open]>svg]:rotate-180",
                    className
                )}
                {...props}
            >
                {children}
                <IconChevronDown className="ml-auto size-4 shrink-0 text-gray-600 transition-transform duration-300 ease-out" />
            </AccordionPrimitive.Trigger>
        </AccordionPrimitive.Header>
    );
}

function AccordionContent({
    className,
    children,
    ...props
}: React.ComponentProps<typeof AccordionPrimitive.Panel>) {
    return (
        <AccordionPrimitive.Panel
            data-slot="accordion-content"
            className="h-[var(--accordion-panel-height)] overflow-hidden text-left text-sm text-gray-700 transition-[height,opacity] duration-300 ease-out data-[ending-style]:h-0 data-[ending-style]:opacity-0 data-[starting-style]:h-0 data-[starting-style]:opacity-0"
            {...props}
        >
            <div className={cn("pt-0 pb-4", className)}>{children}</div>
        </AccordionPrimitive.Panel>
    );
}

export default function AccordionDemo({
    className,
    openMultiple = false,
    items = [
        {
            value: "item-1",
            trigger: "What is the Sentiment Analysis Dashboard?",
            content: (
                <p>
                    It’s an <strong>AI-powered platform</strong> that analyzes written feedback
                    from text or Excel files. It classifies comments as{" "}
                    <span className="text-green-600 font-medium">positive</span>,{" "}
                    <span className="text-gray-600 font-medium">neutral</span>, or{" "}
                    <span className="text-red-600 font-medium">negative</span>, highlights{" "}
                    <strong>key points</strong>, generates a <strong>word cloud</strong>,
                    and provides results in a downloadable Excel file.
                </p>
            ),
        },
        {
            value: "item-2",
            trigger: "How do I upload comments or feedback?",
            content: (
                <p>
                    You can input comments directly as <strong>simple text</strong> or
                    upload them in <strong>Excel</strong> format. The system processes your
                    file instantly, adds new columns for sentiment, keywords, and insights,
                    and makes the updated file available for download.
                </p>
            ),
        },
        {
            value: "item-3",
            trigger: "What insights does the dashboard provide?",
            content: (
                <p>
                    The dashboard provides <strong>sentiment results</strong> (positive,
                    neutral, negative), <strong>top points extracted</strong> from each
                    comment, and <strong>word clouds</strong> that highlight frequently
                    used terms. These insights make it easy to spot trends, recurring
                    issues, and overall feedback tone.
                </p>
            ),
        },
        {
            value: "item-4",
            trigger: "Can I filter results by category or group?",
            content: (
                <p>
                    Yes. You can filter results by <strong>topics, categories, or
                        feedback groups</strong>, allowing you to focus on the areas that
                    matter most for your analysis.
                </p>
            ),
        },
        {
            value: "item-5",
            trigger: "Is my data secure?",
            content: (
                <p>
                    Absolutely. All uploaded data is processed securely, and the generated
                    Excel files are stored and shared only within your <strong>organization’s
                        environment</strong>, ensuring full compliance with data protection
                    and privacy standards.
                </p>
            ),
        },
        {
            value: "item-6",
            trigger: "How can this help decision-makers?",
            content: (
                <p>
                    The dashboard turns raw comments into <strong>actionable insights</strong>.
                    Decision-makers can quickly identify positive feedback, address
                    negative concerns, and track emerging themes, enabling{" "}
                    <strong>faster, data-driven responses</strong> and improving trust
                    in the consultation process.
                </p>
            ),
        },
    ]
}: AccordionProps) {
    return (
        <div className="flex w-full flex-col items-center justify-center bg-white px-4 py-16">
            {/* Heading + Description */}
            <div className="mb-8 max-w-2xl text-center">
                <h2 className="text-3xl font-bold text-gray-900">
                    Frequently Asked Questions
                </h2>
                <p className="mt-2 text-gray-600">
                    Here are the most common questions about our Sentiment Analysis
                    Dashboard. Click on a question to reveal the answer.
                </p>
            </div>

            {/* Accordion */}
            <Accordion className={className} openMultiple={openMultiple}>
                {items.map((item) => (
                    <AccordionItem key={item.value} value={item.value}>
                        <AccordionTrigger>{item.trigger}</AccordionTrigger>
                        <AccordionContent>{item.content}</AccordionContent>
                    </AccordionItem>
                ))}
            </Accordion>
        </div>
    );
}

export { Accordion, AccordionItem, AccordionTrigger, AccordionContent };
