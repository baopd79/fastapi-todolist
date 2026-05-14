# AGENTS.md

## Project Context

This repository is a FastAPI todo-list backend. The next frontend must be built as a real todo application, not a marketing landing page.

Backend API base path:

- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `GET /api/v1/auth/me`
- `POST /api/v1/todos`
- `GET /api/v1/todos?is_completed=&skip=&limit=`
- `GET /api/v1/todos/{todo_id}`
- `PATCH /api/v1/todos/{todo_id}`
- `DELETE /api/v1/todos/{todo_id}`

All todo endpoints require a Bearer JWT returned by login/register flow.

## Frontend Stack

Use this stack unless the user explicitly changes it:

- React
- TypeScript
- Vite
- Tailwind CSS
- React Router for auth/app routes
- TanStack Query for server state
- React Hook Form plus Zod for forms and validation
- Lucide React for icons
- Fetch API or a small typed API client; do not introduce a heavy HTTP abstraction unless needed

Prefer a `/frontend` app directory if the backend root remains Python-focused.

## Required Frontend Architecture

- Keep API calls in a dedicated client layer, for example `src/lib/api.ts`.
- Keep auth token handling centralized, for example `src/lib/auth.ts`.
- Keep route-level screens separate from reusable components.
- Model API payloads with TypeScript types matching the backend schemas.
- Handle loading, empty, error, optimistic update, and unauthorized states.
- Persist the access token deliberately, preferably `localStorage` for this learning app unless the backend changes to cookies.
- Redirect unauthenticated users away from the app shell.
- Do not leak backend internal fields such as `hashed_password`.

## Design Source Of Truth

Follow `DESIGN.md` strictly. If there is any conflict between generic frontend habits and `DESIGN.md`, `DESIGN.md` wins.

The UI should feel inspired by Vercel/Geist:

- White canvas: `#ffffff`
- Primary text: `#171717`
- Secondary text: `#4d4d4d`
- Tertiary text: `#666666`
- Light divider/ring: `#ebebeb`
- Subtle surface tint: `#fafafa`
- Link blue: `#0072f5`
- Focus blue: `hsla(212, 100%, 48%, 1)`
- Workflow accents only when meaningful:
  - Develop blue: `#0a72ef`
  - Preview pink: `#de1d8d`
  - Ship red: `#ff5b4f`

## Typography Rules

- Use Geist Sans for normal UI text.
- Use Geist Mono for technical labels, code-like text, counters, and small metadata.
- Enable OpenType ligatures globally with `font-feature-settings: "liga"`.
- Use only these normal weights:
  - `400` for reading/body text
  - `500` for UI controls and interactive text
  - `600` for headings/emphasis
- Avoid `700` except for tiny uppercase micro-badges if truly needed.
- Letter spacing must follow `DESIGN.md`:
  - Display 48px: `-2.4px` to `-2.88px`
  - 40px headings: `-2.4px`
  - 32px headings: `-1.28px`
  - 24px card titles: `-0.96px`
  - 16px semibold labels: `-0.32px`
  - 14px and body text: normal

## Component Rules

- Use shadow-as-border instead of CSS borders for cards and controls:
  `0px 0px 0px 1px rgba(0,0,0,0.08)`.
- Standard card shadow:
  `rgba(0,0,0,0.08) 0px 0px 0px 1px, rgba(0,0,0,0.04) 0px 2px 2px, #fafafa 0px 0px 0px 1px`.
- Featured card shadow may add:
  `rgba(0,0,0,0.04) 0px 8px 8px -8px`.
- Standard radii:
  - Buttons: `6px`
  - Cards/list rows: `8px`
  - Image/screenshot panels: `12px`
  - Badges/tags only: `9999px`
- Do not use pill-shaped primary action buttons. Pills are for badges/tags/status only.
- Use lucide icons in icon buttons and controls when an icon exists.
- Build tooltips for icon-only buttons when their meaning is not obvious.
- Do not put cards inside cards.
- Do not add decorative gradient orbs, bokeh blobs, or colorful chrome.
- Use workflow accent colors only for semantic todo/workflow states, never as random decoration.

## Todo App UX Requirements

The first screen after login should be the usable todo app.

Expected app behavior:

- Register and login screens.
- Authenticated app shell with current user context.
- Todo list with create, edit, complete/uncomplete, delete.
- Filter by all, active, completed.
- Clear empty states.
- Inline optimistic feedback where reasonable.
- Confirm or soften destructive delete interactions.
- Keyboard-friendly controls and visible focus states.
- Mobile layout must remain single-column and touch-friendly.

## Layout Rules

- Max content width should stay around `1200px`.
- Use generous whitespace; separation comes from spacing and shadow-rings, not colored sections.
- Desktop may use a two-column work surface if it improves todo editing, but do not make a marketing hero.
- Mobile should collapse to a dense, practical single-column app.
- Use stable dimensions for toolbars, icon buttons, list rows, counters, and filters to avoid layout shift.

## Tailwind Guidance

- Extend Tailwind theme with Geist fonts, exact color tokens, shadow tokens, and radius tokens from `DESIGN.md`.
- Prefer semantic utility composition through small components over long repeated class strings.
- Use arbitrary values only when they encode exact design-system values from `DESIGN.md`.
- Keep Tailwind classes readable and consistent.

## Quality Bar

Before considering frontend work complete:

- Run type-check.
- Run lint/build if configured.
- Start the dev server and provide the local URL.
- Verify the app in desktop and mobile viewport sizes.
- Check that text does not overflow buttons, cards, filters, or list rows.
- Confirm protected routes redirect correctly.
- Confirm API error states are visible and understandable.

