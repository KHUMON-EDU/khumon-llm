from typing import List

from pydantic import BaseModel

generation_schema_example = {
    "summary": 'Amazon Elastic Compute Cloud (EC2) is a central part of Amazon Web Services, which is a cloud computing platform provided by Amazon.com. EC2 allows users to rent virtual computers and run their own computer applications on them. Users can boot the virtual machines, called instances, from Amazon Machine Images (AMI) and configure them with desired software. This web service encourages scalable application deployment by providing users with the ability to create, start, and terminate server instances as needed. Users are billed on an hourly basis for the running servers, hence the term "elastic." EC2 also offers control over the geographical location of instances, allowing for latency optimization and high-level redundancy. In November 2010, Amazon transitioned its own website to use EC2 and AWS.',
    "problems": [
        {
            "problem_no": 1,
            "question": "Amazon Elastic Compute Cloud (EC2)은 무엇인가요?",
            "answer": "Amazon EC2는 사용자가 가상 컴퓨터를 임대하고 그 위에서 자신의 애플리케이션을 실행할 수 있는 클라우드 컴퓨팅 서비스입니다.",
        },
        {
            "problem_no": 2,
            "question": "EC2는 어떻게 확장 가능한 애플리케이션 배포를 가능하게 하나요?",
            "answer": "EC2는 사용자가 필요에 따라 서버 인스턴스를 생성, 시작 및 종료할 수 있도록 해주어 애플리케이션 배포의 확장성을 제공합니다.",
        },
        {
            "problem_no": 3,
            "question": "Amazon Machine Images (AMI)은 무엇인가요?",
            "answer": "AMI는 사용자가 EC2 인스턴스를 부팅하고 원하는 소프트웨어로 구성할 수 있는 가상 머신 템플릿입니다.",
        },
        {
            "problem_no": 4,
            "question": "EC2 사용에 대해 사용자는 어떻게 청구되나요?",
            "answer": "사용자는 실행 중인 서버 인스턴스에 대해 시간당 요금을 지불합니다.",
        },
        {
            "problem_no": 5,
            "question": 'EC2에서 "elastic"이라는 용어는 무엇을 의미하나요?',
            "answer": 'EC2에서 "elastic"이라는 용어는 수요에 따라 서버 인스턴스의 수를 쉽게 확장하거나 축소할 수 있는 능력을 의미합니다.',
        },
    ],
}


class ReuqestText(BaseModel):
    text: str


class Problem(BaseModel):
    problem_no: int
    question: str
    answer: str


class Generation(BaseModel):
    summary: str
    problems: List[Problem]
    model_config = {"json_schema_extra": {"examples": [generation_schema_example]}}


class RequestAssessment(BaseModel):
    question: str
    answer: str
    model_config = {"json_schema_extra": {"examples": [{
  "question": "Amazon Elastic Compute Cloud (EC2)은 무엇인가요?",
  "answer": "Amazon EC2는 사용자가 가상 컴퓨터를 임대하고 그 위에서 자신의 애플리케이션을 실행할 수 있는 클라우드 컴퓨팅 서비스입니다."
}]}}


class Assessment(BaseModel):
    assessment: str
    correct: bool
    model_config = {"json_schema_extra": {"examples": [{
  "assessment": "\n\n설명: 사용자님의 답변은 정확합니다. Amazon Elastic Compute Cloud(EC2)는 사용자가 가상 컴퓨팅 환경을 임대하여 사용할 수 있는 서비스로, 사용자는 이 가상 서버를 이용하여 자신의 애플리케이션을 실행하고 관리할 수 있습니다. EC2는 클라우드 컴퓨팅의 핵심 서비스 중 하나로, 유연한 컴퓨팅 파워를 제공합니다.",
  "correct": True
}]}}