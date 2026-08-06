import { formatMessageText } from "@/lib/formatMessage";
import type { ChatMessage } from "@/lib/types";
import { TypingIndicator } from "./TypingIndicator";

interface MessageBubbleProps {
  message: ChatMessage;
}

/** A single chat bubble, styled distinctly per role (user / agent / error). */
export function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === "user";
  const isError = message.role === "error";

  return (
    <li
      className={`flex animate-message-in ${isUser ? "justify-end" : "justify-start"}`}
    >
      <div
        className={[
          "max-w-[85%] rounded-2xl px-4 py-2.5 text-[0.925rem] leading-relaxed shadow-sm sm:max-w-[75%]",
          isUser
            ? "rounded-br-sm bg-accent text-white"
            : isError
              ? "rounded-bl-sm border border-error-border bg-error-soft text-error"
              : "rounded-bl-sm border border-border bg-surface text-ink",
        ].join(" ")}
      >
        {message.pending ? <TypingIndicator /> : formatMessageText(message.text)}
      </div>
    </li>
  );
}
