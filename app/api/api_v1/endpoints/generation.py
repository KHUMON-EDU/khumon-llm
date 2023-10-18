from typing import Any

from fastapi import APIRouter, UploadFile

from app.generation import Generator
from app.schemas.generation import Generation, ReuqestText
from app.utils import PreProcessor, parsing_generation_output

router = APIRouter()
generator = Generator()

@router.post("/text", response_model=Generation)
def generation_by_text(req: ReuqestText) -> Any:
    """
    Generate a response that includes a summary and questions from a text.\n
    A text (string) is required in the request body.
    """
    result = generator.run(req.text)
    problems = parsing_generation_output(result["generation"])

    return {"summary": result["summary"], "problems": problems}

@router.post("/pdf", response_model=Generation)
def generation_by_pdf(upload_file: UploadFile) -> Any:
    """
    Generate a response that includes a summary and questions from a PDF file.\n
    A multipart PDF file is required in the request body.
    """
    source = upload_file.file.read()
    pdf_preprocessor = PreProcessor(mode="pdf")
    docs =  pdf_preprocessor.run(source)
    result = generator.run(docs)
    problems = parsing_generation_output(result["generation"])

    return {"summary": result["summary"], "problems": problems}


@router.post("/video", response_model=Generation)
async def generation_by_video(upload_file: UploadFile) -> Any:
    """
    Generate a response that includes a summary and questions from a VIDEO file.\n
    A multipart VIDEO file is required in the request body.\n
    Currently, only MP4 video file format is supported.
    """
    source = upload_file.file.read()
    video_preprocessor = PreProcessor(mode="video")
    docs =  video_preprocessor.run(source)
    result = generator.run(docs)
    problems = parsing_generation_output(result["generation"])

    return {"summary": result["summary"], "problems": problems}