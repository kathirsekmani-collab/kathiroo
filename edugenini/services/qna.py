from __future__ import annotations

from typing import Any


class QnAService:
    def __init__(self, gemini_service: Any) -> None:
        self.gemini = gemini_service

    async def answer(self, question: str) -> str:
        if not question or not question.strip():
            raise ValueError("Question cannot be empty")

        try:
            return await self.gemini.generate_text(
                f"Answer the following question clearly and concisely: {question}"
            )
        except Exception:
            return (
                "This is a demo answer. Please configure a Gemini API key in the .env file "
                "to enable real Q&A responses."
            )
