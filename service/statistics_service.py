from repository import statistics_repository,question_repository
from model.statistics_response import QuestionStatisticsResponse
from exceptions.question_exceptions import QuestionNotFoundError
from model.statistics_response import (
    QuestionStatisticsResponse,
    AllQuestionsStatisticsResponse
)
from clients.user_client import get_user

from model.statistics_response import (
    UserVoteDetail,
    UserStatisticsResponse
)


async def get_question_statistics(
    question_id: int
) -> QuestionStatisticsResponse:

    question = await question_repository.get_question_by_id(
        question_id
    )

    if question is None:
        raise QuestionNotFoundError(
            f"Question {question_id} was not found"
        )

    stats = await (
        statistics_repository.get_question_statistics(
            question_id
        )
    )

    if stats is None:
        return QuestionStatisticsResponse(
            question_id=question_id,
            total_votes=0,
            option_1_votes=0,
            option_2_votes=0,
            option_3_votes=0,
            option_4_votes=0
        )

    return QuestionStatisticsResponse.model_validate(
        dict(stats._mapping)
    )


async def get_all_questions_statistics(
) -> list[AllQuestionsStatisticsResponse]:

    rows = await (
        statistics_repository.get_all_questions_statistics()
    )

    return [
        AllQuestionsStatisticsResponse.model_validate(
            dict(row._mapping)
        )
        for row in rows
    ]

async def get_user_statistics(
    user_id: int
) -> UserStatisticsResponse:

    # Verify that the user exists in User Service
    await get_user(user_id)

    rows = await (
        statistics_repository.get_user_vote_statistics(
            user_id
        )
    )

    votes = [
        UserVoteDetail.model_validate(
            dict(row._mapping)
        )
        for row in rows
    ]

    return UserStatisticsResponse(
        user_id=user_id,
        questions_answered=len({
            vote.question_id for vote in votes
        }),
        votes=votes
    )
