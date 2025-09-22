"use client";

import * as React from "react";
import { Accordion as AccordionPrimitive } from "@base-ui-components/react/accordion";
import { IconChevronDown } from "@tabler/icons-react"; // swapped Lucide with Tabler
import { cn } from "@/lib/utils";

export interface AccordionProps {
    className?: string;
    openMultiple?: boolean;
    items?: Array<{
        value: string;
        trigger: string;
        content: string;
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
            className={cn("border-b border-gray-200 last:border-b-0", className)}
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
            content:
                "It is a platform that uses AI-powered sentiment detection to analyze public feedback. Decision-makers can quickly understand opinions, spot trends, and improve consultation outcomes.",
        },
        {
            value: "item-2",
            trigger: "How do I upload comments or feedback?",
            content:
                "You can upload feedback data in CSV, Excel, or JSON format. The dashboard automatically processes and categorizes text into positive, negative, or neutral sentiment.",
        },
        {
            value: "item-3",
            trigger: "What insights does the dashboard provide?",
            content:
                "You’ll see sentiment distribution charts, keyword trends, and heatmaps of discussion topics. These insights help you identify emerging concerns and measure public approval.",
        },
        {
            value: "item-4",
            trigger: "Can I filter results by category or group?",
            content:
                "Yes. You can filter sentiment results by demographics, topics, or consultation modules to get more precise insights tailored to specific stakeholders.",
        },
        {
            value: "item-5",
            trigger: "Is my data secure?",
            content:
                "Absolutely. All feedback is processed securely within your organization’s approved cloud or VPC, ensuring compliance with enterprise security standards.",
        },
        {
            value: "item-6",
            trigger: "How can this help decision-makers?",
            content:
                "By surfacing real-time sentiment insights, the dashboard enables faster responses, data-driven decisions, and improved trust in the consultation process.",
        },
    ],
}: AccordionProps) {
    return (
        <div className="flex w-full flex-col items-center justify-center bg-white px-4 py-16">
            {/* Heading + Description */}
            <div className="mb-8 max-w-2xl text-center">
                <h2 className="text-3xl font-bold text-gray-900">
                    Frequently Asked Questions
                </h2>
                <p className="mt-2 text-gray-600">
                    Here are some of the most common questions about our Sentiment
                    Analysis Dashboard. Click on a question to reveal the answer.
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
