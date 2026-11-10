from typing import Annotated
from pydantic import StringConstraints, BaseModel, model_validator

QuestionTitle = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=1,
        max_length=255
    )
]

QuestionOption = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=1,
        max_length=255
    )
]


class CreateQuestionRequest(BaseModel):
    title: QuestionTitle
    option_1: QuestionOption
    option_2: QuestionOption
    option_3: QuestionOption
    option_4: QuestionOption


from pydantic import model_validator


class UpdateQuestionRequest(BaseModel):
    title: QuestionTitle | None = None
    option_1: QuestionOption | None = None
    option_2: QuestionOption | None = None
    option_3: QuestionOption | None = None
    option_4: QuestionOption | None = None

    @model_validator(mode="after")
    def validate_update(self):
        data = self.model_dump(exclude_unset=True)

        if not data:
            raise ValueError("At least one field is required")

        if any(value is None for value in data.values()):
            raise ValueError("Fields cannot be null")

        return self
