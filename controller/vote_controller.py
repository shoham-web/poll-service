
from fastapi import (APIRouter,Depends,HTTPException,Query,status)
from model.vote_request import (CreateVoteRequest,UpdateVoteRequest)
from model.vote_response import VoteResponse
from service import vote_service
from exceptions.vote_exceptions import (VoteNotFoundError,VoteAlreadyExistsError,UserNotRegisteredError,VoteAccessDeniedError)
from exceptions.question_exceptions import QuestionNotFoundError
from exceptions.user_client_exceptions import (RemoteUserNotFoundError,UserServiceUnavailableError)


router = APIRouter(
    prefix="/votes",
    tags=["Votes"],
)


@router.post(
    "/",
    response_model=VoteResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_vote(vote_data: CreateVoteRequest):

    try:
        return await vote_service.create_vote(vote_data)

    except VoteAlreadyExistsError as error:
        raise HTTPException(
            status_code=409,
            detail=str(error)
        ) from error

    except UserNotRegisteredError as error:
        raise HTTPException(
            status_code=403,
            detail=str(error)
        ) from error

    except (
        RemoteUserNotFoundError,
        QuestionNotFoundError
    ) as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        ) from error

    except UserServiceUnavailableError as error:
        raise HTTPException(
            status_code=503,
            detail=str(error)
        ) from error


@router.get(
    "/{vote_id}",
    response_model=VoteResponse
)
async def get_vote(vote_id: int):

    try:
        return await vote_service.get_vote_by_id(vote_id)

    except VoteNotFoundError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        ) from error


@router.patch(
    "/{vote_id}",
    response_model=VoteResponse
)
async def update_vote(
    vote_id: int,
    vote_data: UpdateVoteRequest,
    requesting_user_id: int = Query(gt=0)
):
    try:
        return await vote_service.update_vote(
            vote_id=vote_id,
            requesting_user_id=requesting_user_id,
            vote_data=vote_data
        )

    except VoteNotFoundError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        ) from error

    except (
        VoteAccessDeniedError,
        UserNotRegisteredError
    ) as error:
        raise HTTPException(
            status_code=403,
            detail=str(error)
        ) from error

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


@router.delete(
    "/{vote_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_vote(
    vote_id: int,
    requesting_user_id: int = Query(gt=0)
):
    try:
        await vote_service.delete_vote(
            vote_id=vote_id,
            requesting_user_id=requesting_user_id
        )

    except VoteNotFoundError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        ) from error

    except VoteAccessDeniedError as error:
        raise HTTPException(
            status_code=403,
            detail=str(error)
        ) from error
