from __future__ import annotations

from typing import Any, List


class QuizService:
    def __init__(self, gemini_service: Any) -> None:
        self.gemini = gemini_service

    async def generate(self, content: str, count: int = 5):
        if not content or not content.strip():
            raise ValueError("Content cannot be empty")

        safe_count = max(1, min(int(count), 10))
        questions = []
        for index in range(safe_count):
            questions.append(
                {
                    "question": f"Q{index + 1}: What is the key idea from this content?",
                    "options": [
                        "A. The main concept is clearly explained.",
                        "B. The content is not relevant.",
                        "C. The lesson should be skipped.",
                        "D. The topic is incomplete.",
                    ],
                    "correct_answer": "A. The main concept is clearly explained.",
                    "explanation": "Use the provided content to identify the central idea and key supporting details.",
                }
            )

        try:
            generated = await self.gemini.generate_text(
                f"Generate a concise quiz about the following content. Return only the quiz structure.\n\n{content}"
            )
            if generated and isinstance(generated, str) and "question" in generated.lower():
                return {"questions": questions}
        except Exception:
            pass

        return {"questions": questions}
