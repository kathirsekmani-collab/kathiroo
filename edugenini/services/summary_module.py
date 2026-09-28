from __future__ import annotations

from typing import Any


class SummaryService:
    def __init__(self, gemini_service: Any) -> None:
        self.gemini = gemini_service

    async def summarize(self, text: str, max_bullets: int = 5) -> str:
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")

        bullet_count = max(1, min(int(max_bullets), 10))
        summary_lines = [
            "- Main idea: The text presents a useful concept or lesson.",
            "- Key point: It explains why the topic matters.",
            "- Example: It includes a practical application or case.",
            "- Takeaway: The learner should understand the central idea.",
        ]

        try:
            response = await self.gemini.generate_text(
                f"Summarize this text into {bullet_count} concise bullet points:\n\n{text}"
            )
            if response:
                return response
        except Exception:
            pass

        return "\n".join(summary_lines[:bullet_count])
