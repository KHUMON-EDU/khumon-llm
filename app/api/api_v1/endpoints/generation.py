from typing import Any
from functools import wraps

from fastapi import APIRouter, HTTPException, UploadFile

from app.generation import Generator
from app.schemas.generation import Generation, ReuqestText, generation_schema_example
from app.utils import PreProcessor, parsing_generation_output

router = APIRouter()
generator = Generator()

support_video_types = ["video/mp4"]
support_pdf_types = ["application/pdf"]

def live_mode(func):
    @wraps(func)
    def wrapper_live_mode(*args, **kwargs):
        if kwargs['live_mode']:
            func(*args, **kwargs)
        else:
            return generation_schema_example
    return wrapper_live_mode


@router.post("/text", response_model=Generation)
@live_mode
def generation_by_text(req: ReuqestText, live_mode: bool = True) -> Any:
    """
    Generate a response that includes a summary and questions from a text.\n
    A text (string) is required in the request body.
    """

    result = generator.run(req.text)
    problems = parsing_generation_output(result["generation"])

    return {"summary": result["summary"], "problems": problems}


@router.post("/pdf", response_model=Generation)
@live_mode
def generation_by_pdf(upload_file: UploadFile, live_mode: bool = True) -> Any:
    """
    Generate a response that includes a summary and questions from a PDF file.\n
    A multipart PDF file is required in the request body.
    """

    if not (upload_file.content_type == "application/pdf"):
        raise HTTPException(
            status_code=415, detail="Content type must be application/pdf."
        )
    source = upload_file.file.read()
    pdf_preprocessor = PreProcessor(mode="pdf")
    docs = pdf_preprocessor.run(source)
    result = generator.run(docs)
    problems = parsing_generation_output(result["generation"])

    return {"summary": result["summary"], "problems": problems}


@router.post("/video", response_model=Generation)
@live_mode
async def generation_by_video(upload_file: UploadFile, live_mode: bool = True) -> Any:
    """
    Generate a response that includes a summary and questions from a VIDEO file.\n
    A multipart VIDEO file is required in the request body.\n
    Currently, only MP4 video file format is supported.
    """

    if upload_file.content_type not in support_video_types:
        raise HTTPException(
            status_code=415, detail=f"Content type must be {support_video_types}."
        )

    source = upload_file.file.read()
    video_preprocessor = PreProcessor(mode="video")
    docs = video_preprocessor.run(source)
    result = generator.run(docs)
    problems = parsing_generation_output(result["generation"])

    return {"summary": result["summary"], "problems": problems}
