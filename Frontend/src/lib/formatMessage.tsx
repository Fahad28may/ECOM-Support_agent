import type { ReactNode } from "react";

/**
 * Renders untrusted agent text as React nodes, supporting only **bold** and
 * line breaks. This never touches dangerouslySetInnerHTML or parses HTML —
 * every piece of text is emitted as a plain React text node, which React
 * escapes automatically. So even if the backend answer contains something
 * like "<script>", it renders as literal visible text, not markup.
 */
export function formatMessageText(text: string): ReactNode {
  const lines = text.split("\n");

  return lines.map((line, lineIndex) => (
    <span key={lineIndex}>
      {renderBoldSegments(line)}
      {lineIndex < lines.length - 1 && <br />}
    </span>
  ));
}

/** Splits a single line on **bold** markers and wraps matches in <strong>. */
function renderBoldSegments(line: string): ReactNode[] {
  const segments = line.split(/(\*\*[^*]+\*\*)/g).filter(Boolean);

  return segments.map((segment, index) => {
    const isBold = segment.startsWith("**") && segment.endsWith("**");
    if (isBold) {
      const inner = segment.slice(2, -2);
      return <strong key={index}>{inner}</strong>;
    }
    return <span key={index}>{segment}</span>;
  });
}
