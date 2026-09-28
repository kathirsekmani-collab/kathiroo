from __future__ import annotations

from typing import Any


class ExplanationService:
    def __init__(self, gemini_service: Any) -> None:
        self.gemini = gemini_service

    async def explain(self, topic: str, level: str = "beginner") -> str:
        if not topic or not topic.strip():
            raise ValueError("Topic cannot be empty")

        prompt = (
            f"Explain the topic '{topic}' for a {level} learner in simple, structured language. "
            "Include key concepts, examples, and a short summary."
        )
        try:
            return await self.gemini.generate_text(prompt)
        except Exception:
            return (
                f"This is a demo explanation for '{topic}'. Configure Gemini to generate a real explanation."
            )
