from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover
    def load_dotenv(*_args, **_kwargs):
        return False


BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


@dataclass
class Settings:
    app_name: str = "EduGenie"
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.0-flash"
    enable_local_explainer: bool = False
    local_explanation_model: str = "MBZUAI/LaMini-Flan-T5-783M"

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            app_name=os.getenv("APP_NAME", "EduGenie"),
            gemini_api_key=os.getenv("GEMINI_API_KEY", ""),
            gemini_model=os.getenv("GEMINI_MODEL", "gemini-2.0-flash"),
            enable_local_explainer=os.getenv("ENABLE_LOCAL_EXPLAINER", "false").lower() in {"1", "true", "yes", "on"},
            local_explanation_model=os.getenv("LOCAL_EXPLANATION_MODEL", "MBZUAI/LaMini-Flan-T5-783M"),
        )


settings = Settings.from_env()
