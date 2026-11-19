from fastapi import APIRouter, HTTPException, status
from model.question_request import (CreateQuestionRequest,UpdateQuestionRequest)
from model.question_response import QuestionResponse
from service import question_service
from exceptions.question_exceptions import (QuestionNotFoundError,QuestionHasVotesError)


router = APIRouter(
    prefix="/questions",
    tags=["Questions"]
)


@router.post("/",    response_model= QuestionResponse,status_code=status.HTTP_201_CREATED)
async def create_question(question_data: CreateQuestionRequest):
    return await question_service.create_question(question_data)



@router.get("/",response_model=list[QuestionResponse])
async def get_all_questions():
    return await question_service.get_all_questions()


@router.get("/{question_id}",response_model=QuestionResponse)
async def get_question(question_id: int):
    try:
        return await question_service.get_question_by_id(
            question_id
        )

    except QuestionNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        ) from error


@router.patch("/{question_id}",response_model=QuestionResponse)
async def update_question(question_id: int,question_data: UpdateQuestionRequest):
    try:
        return await question_service.update_question(
            question_id,
            question_data
        )

    except QuestionNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        ) from error

    except QuestionHasVotesError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error)
        ) from error


@router.delete("/{question_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_question(question_id: int):
    try:
        await question_service.delete_question(
            question_id
        )

    except QuestionNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        ) from error
