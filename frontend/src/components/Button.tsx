import type { ButtonHTMLAttributes, PropsWithChildren } from "react";
import { Loader2 } from "lucide-react";
import { clsx } from "clsx";

type ButtonVariant = "dark" | "light" | "ghost" | "danger";
type ButtonSize = "sm" | "md" | "icon";

type ButtonProps = PropsWithChildren<
  ButtonHTMLAttributes<HTMLButtonElement> & {
    variant?: ButtonVariant;
    size?: ButtonSize;
    loading?: boolean;
  }
>;

const variantClasses: Record<ButtonVariant, string> = {
  dark: "bg-ink text-white hover:bg-black",
  light:
    "bg-white text-ink shadow-ring-light hover:bg-ink hover:text-white disabled:hover:bg-white disabled:hover:text-ink",
  ghost: "bg-transparent text-ink hover:bg-wash",
  danger: "bg-white text-ship shadow-ring-light hover:bg-ship hover:text-white",
};

const sizeClasses: Record<ButtonSize, string> = {
  sm: "h-8 px-3 text-sm",
  md: "h-10 px-4 text-sm",
  icon: "h-9 w-9 p-0",
};

export function Button({
  children,
  className,
  disabled,
  loading,
  size = "md",
  type = "button",
  variant = "dark",
  ...props
}: ButtonProps) {
  return (
    <button
      className={clsx(
        "focus-ring inline-flex shrink-0 items-center justify-center gap-2 rounded-control font-medium transition-colors disabled:opacity-50",
        variantClasses[variant],
        sizeClasses[size],
        className,
      )}
      disabled={disabled || loading}
      type={type}
      {...props}
    >
      {loading ? <Loader2 className="h-4 w-4 animate-spin" aria-hidden /> : null}
      {children}
    </button>
  );
}
