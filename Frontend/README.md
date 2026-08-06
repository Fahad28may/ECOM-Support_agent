# Store Assistant — Support Chat Widget

A customer-facing chat frontend for an e-commerce store, built with Next.js
(App Router) + TypeScript + Tailwind CSS. It talks to an existing FastAPI
RAG support-agent backend over a single `POST /ask` endpoint.

This repo contains **frontend only** — no backend code, no API keys.

## Running it

```bash
npm install
npm run dev
```

Then open [http://localhost:3000](http://localhost:3000).

## Pointing it at your backend

The frontend reads the backend's base URL from an environment variable —
it is never hardcoded in the code.

1. Copy the example env file:
   ```bash
   cp .env.local.example .env.local
   ```
2. Edit `.env.local` and set `NEXT_PUBLIC_API_BASE_URL` to wherever your
   FastAPI backend is running. If you omit this file entirely, the app
   falls back to `http://127.0.0.1:8000` for local development.

The frontend expects the backend to expose:

```
POST {NEXT_PUBLIC_API_BASE_URL}/ask
Content-Type: application/json

Request:  { "question": "<string>" }
Response: { "question": "<string>", "answer": "<string>" }
```

If your backend restricts CORS, make sure it allows requests from wherever
this frontend is served from (e.g. `http://localhost:3000` in dev).

## Project structure

```
src/
  app/
    layout.tsx        Root layout, fonts, metadata
    page.tsx           Renders the ChatWidget
    globals.css        Design tokens (colors, animations) + Tailwind import
  components/
    ChatWidget.tsx      Owns conversation state, talks to the API
    MessageList.tsx     Scrollable, auto-scrolling, accessible message log
    MessageBubble.tsx   Individual bubble styling per role
    ChatInput.tsx        Composer: textarea, char counter, send button
    TypingIndicator.tsx  Animated "..." shown while waiting on the agent
  lib/
    api.ts              fetch wrapper for POST /ask (timeout, error handling)
    config.ts            Environment-driven config (API URL, limits)
    types.ts              Shared TypeScript types
    formatMessage.tsx     Safe **bold**/line-break rendering (no raw HTML)
```

## Security notes

- **No secrets on the client.** There are no API keys in this app at all —
  the backend is responsible for anything that needs a secret.
- **XSS-safe rendering.** Agent responses are untrusted text. They are never
  passed through `dangerouslySetInnerHTML`. Instead, `formatMessage.tsx`
  parses only `**bold**` and line breaks and emits them as React text nodes,
  which React escapes automatically — so any HTML/script content in a
  response renders as inert visible text, never as markup.
- **Input limits.** Questions are capped at 500 characters (enforced via the
  textarea's `maxLength` and mirrored in a visible counter), trimmed of
  whitespace, and empty/whitespace-only input is rejected before it ever
  reaches the network.
- **Abuse guard.** The send button is disabled while a request is in
  flight, and a short debounce blocks rapid repeat submissions (e.g. a held
  Enter key), to avoid flooding the backend.
- **Robust networking.** Requests use an `AbortController` with a 30s
  timeout, check `response.ok`, and catch all network/parse failures. Every
  failure path is normalized into one friendly, non-technical message — raw
  errors, status codes, and stack traces are never shown to the user, and
  the input always re-enables afterward.

## Design decisions

- Light-only, warm neutral palette with a single teal accent — a support
  widget should look consistent regardless of the visitor's OS theme.
- Full-window layout (header, scrolling history, fixed composer) rather than
  a floating bottom-right launcher, per the brief.
- No markdown/UI component library — the two markdown features required
  (bold, line breaks) are implemented directly to keep the dependency
  footprint minimal and the sanitization story simple to audit.
