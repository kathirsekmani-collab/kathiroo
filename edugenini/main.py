from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from config import settings
from schemas import (
    ErrorResponse,
    ExplainRequest,
    GenerateQuizRequest,
    LearnRequest,
    QARequest,
    SummarizeRequest,
)
from services.gemini_service import GeminiService
from services.explanation_module import ExplanationService
from services.quiz_module import QuizService
from services.summary_module import SummaryService
from services.learning_path import LearningPathService
from services.qna import QnAService


BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
TEMPLATE_DIR = BASE_DIR / "templates"

app = FastAPI(
    title="EduGenie",
    description="Google Gemini Powered Learning Assistant",
    version="1.0.0",
)

if STATIC_DIR.exists():
    app.mount(
        "/static",
        StaticFiles(directory=str(STATIC_DIR)),
        name="static",
    )

templates = Jinja2Templates(directory=str(TEMPLATE_DIR))


def _model_to_dict(model):
    if hasattr(model, "model_dump"):
        return model.model_dump()
    if hasattr(model, "dict"):
        return model.dict()
    return model


# ---------------------------------------------------------
# Services
# ---------------------------------------------------------

gemini = GeminiService()

explanation_service = ExplanationService(gemini)
qna_service = QnAService(gemini)
quiz_service = QuizService(gemini)
summary_service = SummaryService(gemini)
learning_service = LearningPathService(gemini)


# ---------------------------------------------------------
# Frontend
# ---------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"app_name": getattr(settings, "app_name", "EduGenie")},
    )


# ---------------------------------------------------------
# Health check
# ---------------------------------------------------------

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "app": getattr(settings, "app_name", "EduGenie"),
        "gemini_configured": getattr(gemini, "is_configured", False),
        "local_explainer_enabled": getattr(settings, "enable_local_explainer", False),
    }


# ---------------------------------------------------------
# Question Answering
# ---------------------------------------------------------

@app.post(
    "/qa",
    responses={500: {"model": ErrorResponse}},
)
async def qa(payload: QARequest):
    try:
        answer = await qna_service.answer(payload.question)
        return {"answer": answer}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


# ---------------------------------------------------------
# Explanation
# ---------------------------------------------------------

@app.post(
    "/explain",
    responses={500: {"model": ErrorResponse}},
)
async def explain(payload: ExplainRequest):
    try:
        explanation = await explanation_service.explain(
            payload.topic,
            payload.level,
        )
        return {"explanation": explanation}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


# ---------------------------------------------------------
# Quiz
# ---------------------------------------------------------

@app.post(
    "/quiz",
    responses={500: {"model": ErrorResponse}},
)
async def quiz(payload: GenerateQuizRequest):
    try:
        quiz = await quiz_service.generate(
            payload.content,
            payload.count,
        )
        return _model_to_dict(quiz)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


# ---------------------------------------------------------
# Summarization
# ---------------------------------------------------------

@app.post(
    "/summarize",
    responses={500: {"model": ErrorResponse}},
)
async def summarize(payload: SummarizeRequest):
    try:
        summary = await summary_service.summarize(
            payload.text,
            payload.max_bullets,
        )
        return {"summary": summary}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


# ---------------------------------------------------------
# Learning Recommendations
# ---------------------------------------------------------

@app.post(
    "/learn/recommendations",
    responses={500: {"model": ErrorResponse}},
)
async def learning_path(payload: LearnRequest):
    try:
        learning_path = await learning_service.recommend(
            payload.topic,
            payload.level,
            payload.weeks,
        )
        return _model_to_dict(learning_path)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc