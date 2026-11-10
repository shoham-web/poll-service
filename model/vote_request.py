from pydantic import BaseModel, Field


class CreateVoteRequest(BaseModel):
    user_id: int = Field(gt=0)
    question_id: int = Field(gt=0)
    selected_option: int = Field(ge=1, le=4)


class UpdateVoteRequest(BaseModel):
    selected_option: int = Field(ge=1, le=4)
