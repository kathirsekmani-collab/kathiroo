from __future__ import annotations

from config import settings

try:
    from google import genai
except ImportError:  # pragma: no cover
    genai = None


class GeminiService:
    def __init__(self) -> None:
        self.api_key = settings.gemini_api_key
        self.model_name = settings.gemini_model
        self.client = None
        self._configured = bool(self.api_key)

        if self._configured and genai is not None:
            self.client = genai.Client(api_key=self.api_key)

    @property
    def is_configured(self) -> bool:
        return self._configured and self.client is not None

    async def generate_text(self, prompt: str) -> str:
        if not self.is_configured:
            raise RuntimeError(
                "Gemini API key is missing or the google-genai package is not installed. "
                "Add GEMINI_API_KEY to the .env file or use an alternative setup."
            )

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
        )

        text = getattr(response, "text", None)
        if text is not None:
            return text

        parts = []
        candidates = getattr(response, "candidates", []) or []
        for candidate in candidates:
            content = getattr(candidate, "content", None)
            if not content:
                continue
            for part in getattr(content, "parts", []) or []:
                value = getattr(part, "text", None)
                if value:
                    parts.append(value)

        if parts:
            return "".join(parts)

        return str(response)
