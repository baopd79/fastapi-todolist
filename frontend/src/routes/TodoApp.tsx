import { zodResolver } from "@hookform/resolvers/zod";
import {
  Check,
  CheckCircle2,
  Circle,
  LogOut,
  Pencil,
  Plus,
  Save,
  Trash2,
  X,
} from "lucide-react";
import { useEffect, useMemo, useState } from "react";
import { useForm } from "react-hook-form";
import { useNavigate } from "react-router-dom";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { clsx } from "clsx";
import { z } from "zod";

import { Badge } from "../components/Badge";
import { Button } from "../components/Button";
import { Field, TextAreaField } from "../components/Field";
import { ApiError, api } from "../lib/api";
import { formatShortDate, getErrorMessage } from "../lib/format";
import type { Todo, TodoFilter } from "../lib/types";
import { useAuth } from "../lib/useAuth";

const todoSchema = z.object({
  title: z.string().trim().min(1, "Title is required").max(255),
  description: z.string().trim().max(2000).optional(),
});

type TodoFormValues = z.infer<typeof todoSchema>;

const filters: Array<{ value: TodoFilter; label: string }> = [
  { value: "all", label: "All" },
  { value: "active", label: "Active" },
  { value: "completed", label: "Completed" },
];

export function TodoApp() {
  const navigate = useNavigate();
  const { logout, token } = useAuth();
  const [filter, setFilter] = useState<TodoFilter>("all");

  const meQuery = useQuery({
    queryKey: ["me", token],
    queryFn: api.me,
    enabled: Boolean(token),
  });

  const todosQuery = useQuery({
    queryKey: ["todos", filter],
    queryFn: () => api.listTodos(filter),
    enabled: Boolean(token),
  });

  const allTodosQuery = useQuery({
    queryKey: ["todos", "all"],
    queryFn: () => api.listTodos("all"),
    enabled: Boolean(token),
  });

  useEffect(() => {
    const error = meQuery.error ?? todosQuery.error;
    if (error instanceof ApiError && error.status === 401) {
      logout();
      navigate("/login", { replace: true });
    }
  }, [logout, meQuery.error, navigate, todosQuery.error]);

  const allTodos = allTodosQuery.data ?? [];
  const completedCount = allTodos.filter((todo) => todo.is_completed).length;
  const activeCount = Math.max(allTodos.length - completedCount, 0);
  const visibleTodos = todosQuery.data ?? [];

  const summary = useMemo(
    () => [
      { label: "TOTAL", value: allTodos.length, tone: "text-ink" },
      { label: "ACTIVE", value: activeCount, tone: "text-develop" },
      { label: "DONE", value: completedCount, tone: "text-ship" },
    ],
    [activeCount, allTodos.length, completedCount],
  );

  function handleLogout() {
    logout();
    navigate("/login", { replace: true });
  }

  return (
    <main className="min-h-screen bg-canvas text-ink">
      <header className="sticky top-0 z-10 bg-white/95 px-4 py-3 shadow-ring backdrop-blur sm:px-6">
        <div className="mx-auto flex max-w-app items-center justify-between gap-3">
          <div className="min-w-0">
            <div className="flex items-center gap-2">
              <CheckCircle2 className="h-5 w-5 text-ink" aria-hidden />
              <span className="text-sm font-semibold text-ink">Todolist</span>
            </div>
            <p className="mt-1 truncate font-mono text-xs font-medium text-muted">
              {meQuery.data?.email ?? "Loading session"}
            </p>
          </div>
          <Button
            aria-label="Sign out"
            onClick={handleLogout}
            size="icon"
            title="Sign out"
            variant="light"
          >
            <LogOut className="h-4 w-4" aria-hidden />
          </Button>
        </div>
      </header>

      <div className="mx-auto grid max-w-app gap-8 px-4 py-8 sm:px-6 lg:grid-cols-[360px_1fr] lg:py-12">
        <aside className="grid content-start gap-4">
          <section className="rounded-card bg-white p-5 shadow-card">
            <Badge>WORKSPACE</Badge>
            <h1 className="mt-5 text-4xl font-semibold leading-tight text-ink">
              Today
            </h1>
            <div className="mt-6 grid grid-cols-3 gap-2">
              {summary.map((item) => (
                <div
                  className="rounded-card bg-white px-3 py-3 shadow-ring"
                  key={item.label}
                >
                  <div
                    className={clsx(
                      "font-mono text-2xl font-medium leading-none",
                      item.tone,
                    )}
                  >
                    {item.value}
                  </div>
                  <div className="mt-2 font-mono text-[11px] font-medium text-subtle">
                    {item.label}
                  </div>
                </div>
              ))}
            </div>
          </section>

          <TodoComposer />
        </aside>

        <section className="min-w-0 rounded-card bg-white shadow-card-full">
          <div className="flex flex-col gap-4 px-4 py-4 sm:flex-row sm:items-center sm:justify-between sm:px-5">
            <div>
              <h2 className="text-2xl font-semibold leading-tight text-ink">
                Tasks
              </h2>
              <p className="mt-1 font-mono text-xs font-medium text-muted">
                {visibleTodos.length} visible
              </p>
            </div>
            <div className="grid grid-cols-3 gap-1 rounded-card bg-white p-1 shadow-ring">
              {filters.map((item) => (
                <button
                  className={clsx(
                    "focus-ring h-8 rounded-control px-3 text-sm font-medium transition-colors",
                    filter === item.value
                      ? "bg-ink text-white"
                      : "bg-white text-muted hover:bg-wash hover:text-ink",
                  )}
                  key={item.value}
                  onClick={() => setFilter(item.value)}
                  type="button"
                >
                  {item.label}
                </button>
              ))}
            </div>
          </div>

          <div className="h-px bg-ring" />

          <TodoList
            isLoading={todosQuery.isLoading}
            error={todosQuery.error}
            todos={visibleTodos}
          />
        </section>
      </div>
    </main>
  );
}

function TodoComposer() {
  const queryClient = useQueryClient();
  const {
    formState: { errors, isSubmitting },
    handleSubmit,
    register,
    reset,
    setError,
  } = useForm<TodoFormValues>({
    resolver: zodResolver(todoSchema),
    defaultValues: {
      title: "",
      description: "",
    },
  });

  const createMutation = useMutation({
    mutationFn: api.createTodo,
    onSuccess() {
      reset();
      void queryClient.invalidateQueries({ queryKey: ["todos"] });
    },
  });

  async function onSubmit(values: TodoFormValues) {
    try {
      await createMutation.mutateAsync({
        title: values.title,
        description: values.description || null,
      });
    } catch (error) {
      setError("root", { message: getErrorMessage(error) });
    }
  }

  return (
    <form
      className="rounded-card bg-white p-5 shadow-card"
      onSubmit={handleSubmit(onSubmit)}
    >
      <div className="flex items-center justify-between gap-3">
        <h2 className="text-2xl font-semibold leading-tight text-ink">New task</h2>
        <Plus className="h-4 w-4 text-muted" aria-hidden />
      </div>

      <div className="mt-5 grid gap-4">
        <Field
          error={errors.title?.message}
          id="todo-title"
          label="Title"
          maxLength={255}
          placeholder="Ship backend docs"
          {...register("title")}
        />
        <TextAreaField
          error={errors.description?.message}
          id="todo-description"
          label="Description"
          maxLength={2000}
          placeholder="Optional notes"
          {...register("description")}
        />
      </div>

      {errors.root?.message ? (
        <p className="mt-4 rounded-control bg-white px-3 py-2 text-sm font-medium text-ship shadow-ring">
          {errors.root.message}
        </p>
      ) : null}

      <Button
        className="mt-5 w-full"
        loading={isSubmitting || createMutation.isPending}
        type="submit"
      >
        Add task
      </Button>
    </form>
  );
}

function TodoList({
  error,
  isLoading,
  todos,
}: {
  error: unknown;
  isLoading: boolean;
  todos: Todo[];
}) {
  if (isLoading) {
    return (
      <div className="grid gap-2 p-4 sm:p-5">
        {[0, 1, 2].map((item) => (
          <div
            className="h-24 animate-pulse rounded-card bg-wash shadow-ring"
            key={item}
          />
        ))}
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 sm:p-5">
        <div className="rounded-card bg-white p-5 text-sm font-medium text-ship shadow-ring">
          {getErrorMessage(error)}
        </div>
      </div>
    );
  }

  if (todos.length === 0) {
    return (
      <div className="p-4 sm:p-5">
        <div className="grid min-h-48 place-items-center rounded-card bg-white p-8 text-center shadow-ring">
          <div>
            <Circle className="mx-auto h-8 w-8 text-disabled" aria-hidden />
            <p className="mt-4 text-sm font-medium text-muted">No tasks</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="grid gap-2 p-4 sm:p-5">
      {todos.map((todo) => (
        <TodoItem key={todo.id} todo={todo} />
      ))}
    </div>
  );
}

function TodoItem({ todo }: { todo: Todo }) {
  const queryClient = useQueryClient();
  const [isEditing, setIsEditing] = useState(false);
  const [title, setTitle] = useState(todo.title);
  const [description, setDescription] = useState(todo.description ?? "");
  const [localError, setLocalError] = useState<string | null>(null);

  const updateMutation = useMutation({
    mutationFn: ({
      id,
      next,
    }: {
      id: number;
      next: { title?: string; description?: string | null; is_completed?: boolean };
    }) => api.updateTodo(id, next),
    async onMutate({ id, next }) {
      await queryClient.cancelQueries({ queryKey: ["todos"] });
      const snapshots = queryClient.getQueriesData<Todo[]>({
        queryKey: ["todos"],
      });

      queryClient.setQueriesData<Todo[]>({ queryKey: ["todos"] }, (old) =>
        old?.map((item) => (item.id === id ? { ...item, ...next } : item)),
      );

      return { snapshots };
    },
    onError(_error, _variables, context) {
      context?.snapshots.forEach(([key, value]) => {
        queryClient.setQueryData(key, value);
      });
    },
    onSettled() {
      void queryClient.invalidateQueries({ queryKey: ["todos"] });
    },
  });

  const deleteMutation = useMutation({
    mutationFn: api.deleteTodo,
    async onMutate(id: number) {
      await queryClient.cancelQueries({ queryKey: ["todos"] });
      const snapshots = queryClient.getQueriesData<Todo[]>({
        queryKey: ["todos"],
      });

      queryClient.setQueriesData<Todo[]>({ queryKey: ["todos"] }, (old) =>
        old?.filter((item) => item.id !== id),
      );

      return { snapshots };
    },
    onError(_error, _variables, context) {
      context?.snapshots.forEach(([key, value]) => {
        queryClient.setQueryData(key, value);
      });
    },
    onSettled() {
      void queryClient.invalidateQueries({ queryKey: ["todos"] });
    },
  });

  async function toggleCompleted() {
    setLocalError(null);
    try {
      await updateMutation.mutateAsync({
        id: todo.id,
        next: { is_completed: !todo.is_completed },
      });
    } catch (error) {
      setLocalError(getErrorMessage(error));
    }
  }

  async function saveEdit() {
    const cleanTitle = title.trim();
    const cleanDescription = description.trim();

    if (!cleanTitle) {
      setLocalError("Title is required");
      return;
    }

    setLocalError(null);
    try {
      await updateMutation.mutateAsync({
        id: todo.id,
        next: {
          title: cleanTitle,
          description: cleanDescription || null,
        },
      });
      setIsEditing(false);
    } catch (error) {
      setLocalError(getErrorMessage(error));
    }
  }

  async function deleteTodo() {
    if (!window.confirm("Delete this task?")) return;
    setLocalError(null);
    try {
      await deleteMutation.mutateAsync(todo.id);
    } catch (error) {
      setLocalError(getErrorMessage(error));
    }
  }

  function cancelEdit() {
    setTitle(todo.title);
    setDescription(todo.description ?? "");
    setLocalError(null);
    setIsEditing(false);
  }

  return (
    <article
      className={clsx(
        "rounded-card bg-white p-4 shadow-ring transition-shadow hover:shadow-card",
        todo.is_completed && "bg-wash",
      )}
    >
      <div className="flex items-start gap-3">
        <button
          aria-label={todo.is_completed ? "Mark active" : "Mark completed"}
          className="focus-ring mt-0.5 grid h-8 w-8 shrink-0 place-items-center rounded-full text-ink shadow-ring-light transition-colors hover:bg-wash disabled:opacity-50"
          disabled={updateMutation.isPending}
          onClick={toggleCompleted}
          title={todo.is_completed ? "Mark active" : "Mark completed"}
          type="button"
        >
          {todo.is_completed ? (
            <Check className="h-4 w-4 text-develop" aria-hidden />
          ) : (
            <Circle className="h-4 w-4 text-muted" aria-hidden />
          )}
        </button>

        <div className="min-w-0 flex-1">
          {isEditing ? (
            <div className="grid gap-3">
              <input
                className="focus-ring h-9 w-full rounded-control bg-white px-3 text-sm font-medium text-ink shadow-ring outline-none"
                maxLength={255}
                onChange={(event) => setTitle(event.target.value)}
                value={title}
              />
              <textarea
                className="focus-ring min-h-20 w-full resize-none rounded-control bg-white px-3 py-2 text-sm leading-6 text-muted shadow-ring outline-none"
                maxLength={2000}
                onChange={(event) => setDescription(event.target.value)}
                value={description}
              />
              <div className="flex flex-wrap gap-2">
                <Button
                  loading={updateMutation.isPending}
                  onClick={saveEdit}
                  size="sm"
                >
                  <Save className="h-4 w-4" aria-hidden />
                  Save
                </Button>
                <Button onClick={cancelEdit} size="sm" variant="light">
                  <X className="h-4 w-4" aria-hidden />
                  Cancel
                </Button>
              </div>
            </div>
          ) : (
            <div>
              <h3
                className={clsx(
                  "break-words text-base font-semibold leading-6 text-ink",
                  todo.is_completed && "text-muted line-through",
                )}
              >
                {todo.title}
              </h3>
              {todo.description ? (
                <p className="mt-1 whitespace-pre-wrap break-words text-sm leading-6 text-muted">
                  {todo.description}
                </p>
              ) : null}
              <p className="mt-3 font-mono text-xs font-medium text-subtle">
                {formatShortDate(todo.updated_at)}
              </p>
            </div>
          )}

          {localError ? (
            <p className="mt-3 text-sm font-medium text-ship">{localError}</p>
          ) : null}
        </div>

        {!isEditing ? (
          <div className="flex shrink-0 gap-1">
            <Button
              aria-label="Edit task"
              onClick={() => {
                setTitle(todo.title);
                setDescription(todo.description ?? "");
                setLocalError(null);
                setIsEditing(true);
              }}
              size="icon"
              title="Edit task"
              variant="ghost"
            >
              <Pencil className="h-4 w-4" aria-hidden />
            </Button>
            <Button
              aria-label="Delete task"
              loading={deleteMutation.isPending}
              onClick={deleteTodo}
              size="icon"
              title="Delete task"
              variant="danger"
            >
              <Trash2 className="h-4 w-4" aria-hidden />
            </Button>
          </div>
        ) : null}
      </div>
    </article>
  );
}
