from pydantic import BaseModel, Field


class QuestionStatisticsResponse(BaseModel):
    question_id: int
    total_votes: int = Field(ge=0)
    option_1_votes: int = Field(ge=0)
    option_2_votes: int = Field(ge=0)
    option_3_votes: int = Field(ge=0)
    option_4_votes: int = Field(ge=0)


class AllQuestionsStatisticsResponse(
    QuestionStatisticsResponse
):
    question_title: str
    option_1: str
    option_2: str
    option_3: str
    option_4: str


class UserVoteDetail(BaseModel):
    vote_id: int
    question_id: int
    question_title: str
    selected_option: int = Field(ge=1, le=4)


class UserStatisticsResponse(BaseModel):
    user_id: int
    questions_answered: int = Field(ge=0)
    votes: list[UserVoteDetail]
