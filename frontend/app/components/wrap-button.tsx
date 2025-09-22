import React from "react"
import Link from "next/link"
import { ArrowRight } from "lucide-react"
import { cn } from "@/lib/utils"

interface WrapButtonProps {
    className?: string
    children: React.ReactNode
    href?: string
    innerClass?: string   // inner capsule (LED part)
    arrowClass?: string   // arrow circle
}

const WrapButton: React.FC<WrapButtonProps> = ({
    className,
    children,
    href,
    innerClass,
    arrowClass,
}) => {
    const ButtonContent = (
        <div
            className={cn(
                "group cursor-pointer border border-[#3B3A3A] bg-[#151515] gap-2 h-[64px] flex items-center p-[11px] rounded-full",
                className
            )}
        >
            {/* Inner capsule */}
            <div
                className={cn(
                    "border border-[#3B3A3A] h-[43px] rounded-full flex items-center justify-center px-3",
                    innerClass ? innerClass : "bg-[#17ffc1] text-black"
                )}
            >
                <p className="font-medium tracking-tight flex items-center gap-2 justify-center">
                    {children}
                </p>
            </div>

            {/* Arrow */}
            <div
                className={cn(
                    "group-hover:ml-2 ease-in-out transition-all size-[26px] flex items-center justify-center rounded-full border-2",
                    arrowClass ? arrowClass : "text-[#00ffea] border-[#00fff2]"
                )}
            >
                <ArrowRight
                    size={18}
                    className="group-hover:rotate-45 ease-in-out transition-all"
                />
            </div>
        </div>
    )

    return (
        <div className="flex items-center justify-center">
            {href ? (
                <Link href={href}>{ButtonContent}</Link>
            ) : (
                ButtonContent
            )}
        </div>
    )
}

export default WrapButton
