
from pydantic import BaseModel, Field


class VoteResponse(BaseModel):
    id: int
    user_id: int
    question_id: int
    selected_option: int = Field(ge=1, le=4)
