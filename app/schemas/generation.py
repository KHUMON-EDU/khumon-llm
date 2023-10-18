from typing import List

from pydantic import BaseModel


class ReuqestText(BaseModel):
    text: str

class Problem(BaseModel):
    problem_no: int
    question: str
    answer: str

class Generation(BaseModel):
    summary: str
    problems: List[Problem]
