from typing import Any

from fastapi import APIRouter

router = APIRouter()

@router.post("/pdf", response_model=[])
def get_quiz_by_pdf() -> Any:
    return "pdf"


@router.post("/video", response_model=[])
def get_quiz_by_video() -> Any:
    return "video"