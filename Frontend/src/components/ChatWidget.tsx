"use client";

import { useState } from "react";
import { askAgent } from "@/lib/api";
import type { ChatMessage } from "@/lib/types";
import { ChatInput } from "./ChatInput";
import { MessageList } from "./MessageList";

const GREETING =
  "Hi there! I'm the store assistant. Ask me about orders, shipping, returns, or anything else — I'm happy to help.";

const FRIENDLY_ERROR_TEXT =
  "Sorry, I couldn't reach the store assistant. Please try again.";

function createId() {
  return typeof crypto !== "undefined" && "randomUUID" in crypto
    ? crypto.randomUUID()
    : `${Date.now()}-${Math.random().toString(36).slice(2)}`;
}

/** Top-level chat widget: owns conversation state and talks to the backend. */
export function ChatWidget() {
  const [messages, setMessages] = useState<ChatMessage[]>(() => [
    { id: createId(), role: "agent", text: GREETING },
  ]);
  const [isSending, setIsSending] = useState(false);

  async function handleSend(question: string) {
    const userMessage: ChatMessage = { id: createId(), role: "user", text: question };
    const pendingId = createId();
    const pendingMessage: ChatMessage = {
      id: pendingId,
      role: "agent",
      text: "",
      pending: true,
    };

    setMessages((prev) => [...prev, userMessage, pendingMessage]);
    setIsSending(true);

    try {
      const answer = await askAgent(question);
      setMessages((prev) =>
        prev.map((message) =>
          message.id === pendingId ? { ...message, text: answer, pending: false } : message,
        ),
      );
    } catch {
      setMessages((prev) =>
        prev.map((message) =>
          message.id === pendingId
            ? { ...message, role: "error", text: FRIENDLY_ERROR_TEXT, pending: false }
            : message,
        ),
      );
    } finally {
      setIsSending(false);
    }
  }

  return (
    <div className="flex h-dvh flex-col bg-canvas">
      <Header />
      <MessageList messages={messages} />
      <ChatInput disabled={isSending} onSend={handleSend} />
    </div>
  );
}

function Header() {
  return (
    <header className="flex items-center gap-3 border-b border-border bg-surface px-4 py-3.5 shadow-sm sm:px-6">
      <div className="flex h-9 w-9 items-center justify-center rounded-full bg-accent-soft text-accent-dark">
        <StoreIcon />
      </div>
      <div>
        <p className="text-sm font-semibold text-ink">Store Assistant</p>
        <p className="text-xs text-ink-muted">Usually replies in a few seconds</p>
      </div>
    </header>
  );
}

function StoreIcon() {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 20 20"
      fill="currentColor"
      className="h-5 w-5"
      aria-hidden="true"
    >
      <path d="M2 4.75A.75.75 0 0 1 2.75 4h14.5a.75.75 0 0 1 .6 1.2l-1.7 2.267V15a1 1 0 0 1-1 1h-9a1 1 0 0 1-1-1V7.467l-1.7-2.267a.75.75 0 0 1-.15-.45Z" />
    </svg>
  );
}
