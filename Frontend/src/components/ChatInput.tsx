"use client";

import { useRef, useState, type KeyboardEvent } from "react";
import { MAX_QUESTION_LENGTH, SEND_DEBOUNCE_MS } from "@/lib/config";

interface ChatInputProps {
  disabled: boolean;
  onSend: (question: string) => void;
}

/**
 * The message composer: a growable textarea plus a send button.
 * Enforces length limits, blocks empty/whitespace-only sends, and
 * debounces rapid repeat submissions to protect the backend.
 */
export function ChatInput({ disabled, onSend }: ChatInputProps) {
  const [value, setValue] = useState("");
  const lastSentAtRef = useRef(0);

  const trimmedLength = value.trim().length;
  const canSend = !disabled && trimmedLength > 0;

  function attemptSend() {
    if (!canSend) return;

    const now = Date.now();
    if (now - lastSentAtRef.current < SEND_DEBOUNCE_MS) {
      // Ignore rapid repeat submissions (e.g. double-click, held Enter key).
      return;
    }
    lastSentAtRef.current = now;

    onSend(value.trim());
    setValue("");
  }

  function handleKeyDown(event: KeyboardEvent<HTMLTextAreaElement>) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      attemptSend();
    }
  }

  const nearLimit = value.length >= MAX_QUESTION_LENGTH - 40;

  return (
    <div className="border-t border-border bg-surface px-4 py-3 sm:px-6">
      <div className="mx-auto flex w-full max-w-2xl flex-col gap-1.5">
        <label htmlFor="chat-input" className="sr-only">
          Type your question for the store assistant
        </label>
        <div className="flex items-end gap-2">
          <textarea
            id="chat-input"
            value={value}
            onChange={(event) => setValue(event.target.value)}
            onKeyDown={handleKeyDown}
            disabled={disabled}
            rows={1}
            placeholder="Ask about your order, shipping, returns..."
            maxLength={MAX_QUESTION_LENGTH}
            className="max-h-32 min-h-[44px] flex-1 resize-none rounded-xl border border-border bg-canvas px-3.5 py-2.5 text-[0.925rem] text-ink placeholder:text-ink-muted focus:border-accent focus:outline-none focus:ring-2 focus:ring-accent-soft disabled:cursor-not-allowed disabled:opacity-60"
          />
          <button
            type="button"
            onClick={attemptSend}
            disabled={!canSend}
            aria-label="Send message"
            className="flex h-11 w-11 shrink-0 items-center justify-center rounded-full bg-accent text-white shadow-sm transition-colors duration-150 hover:bg-accent-dark disabled:cursor-not-allowed disabled:bg-border disabled:text-ink-muted"
          >
            <SendIcon />
          </button>
        </div>
        <div className="flex justify-end">
          <span
            className={`text-xs ${nearLimit ? "text-error" : "text-ink-muted"}`}
            aria-live="polite"
          >
            {value.length}/{MAX_QUESTION_LENGTH}
          </span>
        </div>
      </div>
    </div>
  );
}

function SendIcon() {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 20 20"
      fill="currentColor"
      className="h-4.5 w-4.5"
      aria-hidden="true"
    >
      <path d="M2.94 2.94a.75.75 0 0 1 .82-.16l14 5.5a.75.75 0 0 1 0 1.44l-14 5.5a.75.75 0 0 1-1-.94L4.5 10 2.76 3.66a.75.75 0 0 1 .18-.72Z" />
    </svg>
  );
}
