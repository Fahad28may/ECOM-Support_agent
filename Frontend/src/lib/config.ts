// Central place to read environment-based configuration.
// Never hardcode the API URL in components — always import it from here.

const DEFAULT_LOCAL_API_BASE_URL = "http://127.0.0.1:8000";

/**
 * Base URL of the FastAPI support-agent backend.
 * Falls back to the local dev default if NEXT_PUBLIC_API_BASE_URL is not set.
 */
export const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL || DEFAULT_LOCAL_API_BASE_URL;

/** Max characters a customer can type in a single question. */
export const MAX_QUESTION_LENGTH = 500;

/** Abort the request if the backend hasn't responded within this window. */
export const REQUEST_TIMEOUT_MS = 30_000;

/** Minimum gap between two send attempts, to blunt rapid-fire submissions. */
export const SEND_DEBOUNCE_MS = 600;
