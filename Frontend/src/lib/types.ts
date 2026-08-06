// Shared types for the chat widget.

export type MessageRole = "user" | "agent" | "error";

export interface ChatMessage {
  id: string;
  role: MessageRole;
  text: string;
  /** True while an agent message is a placeholder waiting on the API response. */
  pending?: boolean;
}

/** Shape of the POST /ask request body, per the backend contract. */
export interface AskRequest {
  question: string;
}

/** Shape of the POST /ask response body, per the backend contract. */
export interface AskResponse {
  question: string;
  answer: string;
}
