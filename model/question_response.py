
from pydantic import BaseModel

from model.question_request import (
    QuestionTitle,
    QuestionOption
)


class QuestionResponse(BaseModel):
    id: int
    title: QuestionTitle
    option_1: QuestionOption
    option_2: QuestionOption
    option_3: QuestionOption
    option_4: QuestionOption
