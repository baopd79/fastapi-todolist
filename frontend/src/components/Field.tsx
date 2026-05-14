import type { InputHTMLAttributes, TextareaHTMLAttributes } from "react";
import { clsx } from "clsx";

type FieldProps = InputHTMLAttributes<HTMLInputElement> & {
  label: string;
  error?: string;
};

type TextAreaFieldProps = TextareaHTMLAttributes<HTMLTextAreaElement> & {
  label: string;
  error?: string;
};

const controlClass =
  "focus-ring w-full rounded-control bg-white px-3 text-sm text-ink shadow-ring outline-none transition-shadow placeholder:text-disabled focus-visible:shadow-ring-light";

export function Field({ className, error, id, label, ...props }: FieldProps) {
  return (
    <label className="grid gap-2" htmlFor={id}>
      <span className="text-sm font-medium text-ink">{label}</span>
      <input
        className={clsx(controlClass, "h-10", className)}
        id={id}
        {...props}
      />
      {error ? <span className="text-xs font-medium text-ship">{error}</span> : null}
    </label>
  );
}

export function TextAreaField({
  className,
  error,
  id,
  label,
  ...props
}: TextAreaFieldProps) {
  return (
    <label className="grid gap-2" htmlFor={id}>
      <span className="text-sm font-medium text-ink">{label}</span>
      <textarea
        className={clsx(controlClass, "min-h-24 resize-none py-3", className)}
        id={id}
        {...props}
      />
      {error ? <span className="text-xs font-medium text-ship">{error}</span> : null}
    </label>
  );
}
