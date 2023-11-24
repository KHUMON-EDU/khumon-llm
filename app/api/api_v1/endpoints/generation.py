from typing import Any

from fastapi import APIRouter, UploadFile

from app.generation import Generator
from app.generation.answer import check_answer
from app.schemas.generation import Generation, ReuqestText, Assessment, RequestAssessment
from app.utils import PreProcessor, parsing_generation_output
from app.utils.decorators import live_mode, validate_content

router = APIRouter()
generator = Generator()

support_video_types = ["video/mp4"]
support_pdf_types = ["application/pdf"]


@router.post("/text", response_model=Generation)
@live_mode
def generation_by_text(req: ReuqestText, live_mode: bool = True) -> Any:
    """
    Generate a response that includes a summary and questions from a text.\n
    A text (string) is required in the request body.
    """

    result = generator.run(req.text)
    summary =  result["summary"]
    problems = parsing_generation_output(result["generation"])

    return {"summary": summary, "problems": problems}


@router.post("/pdf", response_model=Generation)
@validate_content(support_pdf_types)
def generation_by_pdf(upload_file: UploadFile, live_mode: bool = True) -> Any:
    """
    Generate a response that includes a summary and questions from a PDF file.\n
    A multipart PDF file is required in the request body.
    """
    source = upload_file.file.read()
    pdf_preprocessor = PreProcessor(mode="pdf")
    docs = pdf_preprocessor.run(source)
    result = generator.run(docs)
    summary =  result["summary"]
    problems = parsing_generation_output(result["generation"])

    return {"summary": summary, "problems": problems}


@router.post("/video", response_model=Generation)
def generation_by_video(upload_file: UploadFile, live_mode: bool = True) -> Any:
    """
    Generate a response that includes a summary and questions from a VIDEO file.\n
    A multipart VIDEO file is required in the request body.\n
    Currently, only MP4 video file format is supported.
    """
    source = upload_file.file.read()
    video_preprocessor = PreProcessor(mode="video")
    docs = video_preprocessor.run(source)
    result = generator.run(docs)
    summary =  result["summary"]
    problems = parsing_generation_output(result["generation"])

    return {"summary": summary, "problems": problems}

@router.post("/assessment", response_model=Assessment)
def check_answer_by_problem(req: RequestAssessment):
    question = req.question
    user_answer = req.answer
    assessment = check_answer(question, user_answer)
    correct = True

    if "[CHECK: TRUE]" in assessment:
        correct = True
        assessment = assessment.replace("[CHECK: TRUE]", "")
    else:
        correct = False
        assessment = assessment.replace("[CHECK: FALSE]", "")

    return {"assessment": assessment, "correct": correct}
