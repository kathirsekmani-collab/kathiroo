from __future__ import annotations

from typing import Any, List


class LearningPathService:
    def __init__(self, gemini_service: Any) -> None:
        self.gemini = gemini_service

    async def recommend(self, topic: str, level: str = "beginner", weeks: int = 4):
        if not topic or not topic.strip():
            raise ValueError("Topic cannot be empty")

        result = {
            "topic": topic,
            "level": level,
            "weeks": max(1, int(weeks)),
            "plan": [
                "Week 1: Understand the fundamentals and core vocabulary.",
                "Week 2: Practice key examples and simple exercises.",
                "Week 3: Apply the concept in real scenarios.",
                "Week 4: Review, assess progress, and reinforce weak areas.",
            ],
        }

        try:
            generated = await self.gemini.generate_text(
                f"Create a {weeks}-week learning plan for '{topic}' at {level} level."
            )
            if generated and isinstance(generated, str):
                result["plan"] = [line.strip(" -") for line in generated.splitlines() if line.strip()][:max(1, min(weeks, 8))]
                if not result["plan"]:
                    result["plan"] = [
                        "Week 1: Understand the fundamentals and core vocabulary.",
                        "Week 2: Practice key examples and simple exercises.",
                        "Week 3: Apply the concept in real scenarios.",
                        "Week 4: Review, assess progress, and reinforce weak areas.",
                    ]
        except Exception:
            pass

        return result
