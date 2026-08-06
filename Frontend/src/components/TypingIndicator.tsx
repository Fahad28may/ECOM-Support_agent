/** Three bouncing dots shown in an agent bubble while a response is pending. */
export function TypingIndicator() {
  return (
    <span className="inline-flex items-center gap-1" aria-hidden="true">
      <span className="typing-dot h-1.5 w-1.5 rounded-full bg-ink-muted [animation-delay:0ms]" />
      <span className="typing-dot h-1.5 w-1.5 rounded-full bg-ink-muted [animation-delay:150ms]" />
      <span className="typing-dot h-1.5 w-1.5 rounded-full bg-ink-muted [animation-delay:300ms]" />
    </span>
  );
}
