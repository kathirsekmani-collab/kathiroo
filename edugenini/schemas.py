from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    detail: str


class QARequest(BaseModel):
    question: str = Field(..., min_length=1)


class ExplainRequest(BaseModel):
    topic: str = Field(..., min_length=1)
    level: str = Field(default="beginner")


class GenerateQuizRequest(BaseModel):
    content: str = Field(..., min_length=1)
    count: int = Field(default=5, ge=1, le=20)


class SummarizeRequest(BaseModel):
    text: str = Field(..., min_length=1)
    max_bullets: int = Field(default=5, ge=1, le=15)


class LearnRequest(BaseModel):
    topic: str = Field(..., min_length=1)
    level: str = Field(default="beginner")
    weeks: int = Field(default=4, ge=1, le=24)


class QuizQuestion(BaseModel):
    question: str
    options: List[str]
    correct_answer: str
    explanation: Optional[str] = None


class LearningPathPlan(BaseModel):
    topic: str
    level: str
    weeks: int
    plan: List[str]
