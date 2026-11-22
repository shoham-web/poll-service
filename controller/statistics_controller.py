from fastapi import APIRouter, HTTPException
from service import statistics_service
from model.statistics_response import QuestionStatisticsResponse, AllQuestionsStatisticsResponse
from exceptions.question_exceptions import  QuestionNotFoundError
from exceptions.user_client_exceptions import (
    RemoteUserNotFoundError,
    UserServiceUnavailableError
)

from model.statistics_response import UserStatisticsResponse


router = APIRouter(
    prefix="/statistics",
    tags=["Statistics"]
)


@router.get(
    "/questions/{question_id}",
    response_model=QuestionStatisticsResponse
)
async def get_question_statistics(question_id: int):

    try:
        return await (
            statistics_service.get_question_statistics(
                question_id
            )
        )

    except QuestionNotFoundError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        ) from error


@router.get(
    "/questions",
    response_model=list[AllQuestionsStatisticsResponse]
)
async def get_all_questions_statistics():

    return await (
        statistics_service.get_all_questions_statistics()
    )


@router.get(
    "/users/{user_id}",
    response_model=UserStatisticsResponse
)
async def get_user_statistics(user_id: int):

    try:
        return await (
            statistics_service.get_user_statistics(
                user_id
            )
        )

    except RemoteUserNotFoundError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        ) from error

    except UserServiceUnavailableError as error:
        raise HTTPException(
            status_code=503,
            detail=str(error)
        ) from error
