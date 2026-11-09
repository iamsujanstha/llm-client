
import json
import os
import httpx
from typing import Iterator


class LLMClient:
    """Thin wrapper around any OpenAI-compatible /v1/chat/completions endpoint."""

    def __init__(self):
        # Base URL defaults to a local llama.cpp / Ollama server.
        # Override with LLM_BASE_URL to point at any OpenAI-compatible API.
        self.base_url = os.getenv(
            "LLM_BASE_URL",
            "http://127.0.0.1:8080/v1"
        )

        # Model name is required — the server needs it to route the request.
        self.model = os.getenv("LLM_MODEL")

        if not self.model:
            raise ValueError("LLM_MODEL environment variable is required")

        # httpx.Client keeps a connection pool open across calls,
        # avoiding a fresh TCP + TLS handshake per request.
        # 60s timeout because LLM inference can be slow on CPU.
        self.client = httpx.Client(timeout=60.0)

    def chat(self, messages: list[dict], temperature=0.7, max_tokens=200):
        """Send messages and return the full response at once (non-streaming)."""

        # Payload follows the OpenAI chat completions schema —
        # any compatible server (Ollama, vLLM, llama.cpp) accepts this.
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        try:
            response = self.client.post(
                f"{self.base_url}/chat/completions",
                json=payload,      # httpx auto-sets Content-Type: application/json
            )

            # Raises HTTPStatusError on 4xx/5xx so we don't silently use bad data.
            response.raise_for_status()
            result = response.json()

            # OpenAI format nests the answer inside choices[0].message.content.
            return result["choices"][0]["message"]["content"]

        except httpx.TimeoutException as exc:
            raise RuntimeError("LLM request timed out") from exc

        except httpx.HTTPStatusError as exc:
            # Surface the server's error body — helps debug model-not-found, etc.
            raise RuntimeError(
                f"LLM server returned {exc.response.status_code}: "
                f"{exc.response.text}"
            ) from exc

        except (httpx.RequestError, KeyError, IndexError, ValueError) as exc:
            # RequestError  — network/DNS failure
            # KeyError/IndexError — unexpected response shape
            # ValueError — JSON decode failure
            raise RuntimeError(f"LLM request failed: {exc}") from exc

    def stream_chat(
        self,
        messages: list[dict],
        temperature: float = 0.7,
        max_tokens: int = 200,
    ) -> Iterator[str]:
        """Yield tokens as they arrive — gives the user instant feedback."""

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": True,     # tells the server to send Server-Sent Events (SSE)
        }

        try:
            # client.stream() keeps the connection open and reads chunks lazily,
            # instead of buffering the entire response in memory.
            with self.client.stream(
                "POST",
                f"{self.base_url}/chat/completions",
                json=payload,
            ) as response:

                response.raise_for_status()

                # SSE protocol: each event is a line starting with "data: ".
                for line in response.iter_lines():

                    # Skip empty keep-alive lines and non-data lines.
                    if not line or not line.startswith("data:"):
                        continue

                    data = line[len("data:"):].strip()

                    # "data: [DONE]" signals the server has finished generating.
                    if data == "[DONE]":
                        break

                    chunk = json.loads(data)

                    # Streaming chunks use "delta" instead of "message" —
                    # each delta contains only the new token(s).
                    content = (
                        chunk.get("choices", [{}])[0]
                        .get("delta", {})
                        .get("content")
                    )

                    if content:
                        yield content

        except httpx.TimeoutException as exc:
            raise RuntimeError("Streaming request timed out") from exc

        except httpx.HTTPStatusError as exc:
            raise RuntimeError(
                f"HTTP error {exc.response.status_code}"
            ) from exc

        except (httpx.RequestError, json.JSONDecodeError) as exc:
            # JSONDecodeError — server sent malformed SSE chunk
            raise RuntimeError(
                f"Streaming failed: {exc}"
            ) from exc

    def close(self):
        """Close the underlying connection pool. Call when done."""
        self.client.close()
