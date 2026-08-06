import { API_BASE_URL, REQUEST_TIMEOUT_MS } from "./config";
import type { AskRequest, AskResponse } from "./types";

/** Thrown for any failure we want the UI to show as a friendly error bubble. */
export class AskAgentError extends Error {}

/**
 * Sends the customer's question to the backend RAG agent and returns its answer.
 *
 * All failure modes (network error, timeout, non-2xx, malformed body) are
 * normalized into an AskAgentError with a safe, user-facing message — callers
 * never need to inspect the underlying cause or worry about leaking internals.
 */
export async function askAgent(question: string): Promise<string> {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);

  try {
    const body: AskRequest = { question };

    const response = await fetch(`${API_BASE_URL}/ask`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
      signal: controller.signal,
    });

    if (!response.ok) {
      throw new AskAgentError(`Backend responded with status ${response.status}`);
    }

    const data: AskResponse = await response.json();

    if (typeof data.answer !== "string") {
      throw new AskAgentError("Backend response was missing an answer.");
    }

    return data.answer;
  } catch (err) {
    // Re-throw as our own error type with a message safe to show to users.
    // The original error (network failure, abort, parse error, etc.) is
    // intentionally not surfaced to the UI.
    if (err instanceof AskAgentError) {
      throw err;
    }
    throw new AskAgentError("Failed to reach the support assistant.");
  } finally {
    clearTimeout(timeoutId);
  }
}
