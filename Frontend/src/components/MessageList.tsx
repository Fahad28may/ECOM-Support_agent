"use client";

import { useEffect, useRef } from "react";
import type { ChatMessage } from "@/lib/types";
import { MessageBubble } from "./MessageBubble";

interface MessageListProps {
  messages: ChatMessage[];
}

/**
 * Scrollable message history. Auto-scrolls to the newest message and
 * announces new content politely for screen reader users.
 */
export function MessageList({ messages }: MessageListProps) {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth", block: "end" });
  }, [messages]);

  return (
    <div
      className="flex-1 overflow-y-auto px-4 py-6 sm:px-6"
      tabIndex={0}
      aria-label="Conversation with the store assistant"
    >
      <ul
        role="log"
        aria-live="polite"
        aria-relevant="additions"
        className="mx-auto flex w-full max-w-2xl flex-col gap-3"
      >
        {messages.map((message) => (
          <MessageBubble key={message.id} message={message} />
        ))}
      </ul>
      <div ref={bottomRef} />
    </div>
  );
}
