import type { PropsWithChildren } from "react";
import { clsx } from "clsx";

export function Badge({
  children,
  className,
}: PropsWithChildren<{ className?: string }>) {
  return (
    <span
      className={clsx(
        "inline-flex h-6 items-center rounded-full bg-badge-blue px-2.5 font-mono text-xs font-medium text-badge-text",
        className,
      )}
    >
      {children}
    </span>
  );
}
