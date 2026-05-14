import { zodResolver } from "@hookform/resolvers/zod";
import { ArrowRight, CheckCircle2 } from "lucide-react";
import { useMemo } from "react";
import { useForm } from "react-hook-form";
import { Link, useNavigate } from "react-router-dom";
import { z } from "zod";

import { Badge } from "../components/Badge";
import { Button } from "../components/Button";
import { Field } from "../components/Field";
import { api } from "../lib/api";
import { getErrorMessage } from "../lib/format";
import { useAuth } from "../lib/useAuth";

const loginSchema = z.object({
  email: z.string().trim().email("Enter a valid email"),
  password: z.string().min(1, "Password is required").max(128),
});

const registerSchema = z.object({
  email: z.string().trim().email("Enter a valid email"),
  password: z.string().min(8, "Use at least 8 characters").max(128),
});

type AuthValues = z.infer<typeof registerSchema>;

type AuthPageProps = {
  mode: "login" | "register";
};

export function AuthPage({ mode }: AuthPageProps) {
  const navigate = useNavigate();
  const { setSession } = useAuth();
  const schema = mode === "register" ? registerSchema : loginSchema;
  const copy = useMemo(
    () =>
      mode === "register"
        ? {
            eyebrow: "NEW SESSION",
            title: "Create account",
            action: "Create account",
            swapText: "Already have an account?",
            swapLabel: "Sign in",
            swapTo: "/login",
          }
        : {
            eyebrow: "WELCOME BACK",
            title: "Sign in",
            action: "Sign in",
            swapText: "New here?",
            swapLabel: "Create account",
            swapTo: "/register",
          },
    [mode],
  );

  const {
    formState: { errors, isSubmitting },
    handleSubmit,
    register,
    setError,
  } = useForm<AuthValues>({
    resolver: zodResolver(schema),
    defaultValues: {
      email: "",
      password: "",
    },
  });

  async function onSubmit(values: AuthValues) {
    try {
      if (mode === "register") {
        await api.register(values);
      }
      const token = await api.login(values);
      setSession(token.access_token);
      navigate("/", { replace: true });
    } catch (error) {
      setError("root", { message: getErrorMessage(error) });
    }
  }

  return (
    <main className="min-h-screen bg-canvas px-4 py-10 text-ink sm:px-6">
      <div className="mx-auto grid min-h-[calc(100vh-80px)] max-w-app place-items-center">
        <section className="grid w-full max-w-[960px] gap-8 lg:grid-cols-[1fr_420px] lg:items-center">
          <div className="hidden lg:block">
            <Badge>{copy.eyebrow}</Badge>
            <h1 className="mt-6 max-w-[560px] text-5xl font-semibold leading-none text-ink">
              Todolist
            </h1>
            <div className="mt-10 grid max-w-[520px] gap-3">
              {["Auth", "Tasks", "Focus"].map((item) => (
                <div
                  className="flex h-12 items-center gap-3 rounded-card bg-white px-4 shadow-card"
                  key={item}
                >
                  <CheckCircle2 className="h-4 w-4 text-develop" aria-hidden />
                  <span className="font-mono text-xs font-medium uppercase text-muted">
                    {item}
                  </span>
                </div>
              ))}
            </div>
          </div>

          <form
            className="rounded-card bg-white p-6 shadow-card-full sm:p-8"
            onSubmit={handleSubmit(onSubmit)}
          >
            <Badge className="lg:hidden">{copy.eyebrow}</Badge>
            <div className="mt-5 lg:mt-0">
              <h2 className="text-3xl font-semibold leading-tight text-ink">
                {copy.title}
              </h2>
              <p className="mt-2 text-sm leading-6 text-muted">
                {copy.swapText}{" "}
                <Link
                  className="focus-ring rounded-sm font-medium text-link underline underline-offset-4"
                  to={copy.swapTo}
                >
                  {copy.swapLabel}
                </Link>
              </p>
            </div>

            <div className="mt-8 grid gap-5">
              <Field
                autoComplete="email"
                error={errors.email?.message}
                id="email"
                label="Email"
                placeholder="you@example.com"
                type="email"
                {...register("email")}
              />
              <Field
                autoComplete={mode === "register" ? "new-password" : "current-password"}
                error={errors.password?.message}
                id="password"
                label="Password"
                placeholder="password"
                type="password"
                {...register("password")}
              />
            </div>

            {errors.root?.message ? (
              <p className="mt-5 rounded-control bg-white px-3 py-2 text-sm font-medium text-ship shadow-ring">
                {errors.root.message}
              </p>
            ) : null}

            <Button
              className="mt-8 w-full"
              loading={isSubmitting}
              type="submit"
            >
              {copy.action}
              <ArrowRight className="h-4 w-4" aria-hidden />
            </Button>
          </form>
        </section>
      </div>
    </main>
  );
}
