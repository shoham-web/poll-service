from pymysql.err import IntegrityError as MySQLIntegrityError
from sqlalchemy.exc import IntegrityError as SQLAlchemyIntegrityError
from clients.user_client import get_user
from config.database import database
from model.vote_request import CreateVoteRequest, UpdateVoteRequest
from model.vote_response import VoteResponse
from repository import question_repository, vote_repository
from exceptions.vote_exceptions import (VoteAlreadyExistsError,UserNotRegisteredError, VoteNotFoundError, VoteAccessDeniedError)
from exceptions.question_exceptions import QuestionNotFoundError


async def validate_registered_user(user_id: int) -> dict:

    user = await get_user(user_id)

    if not user["is_registered"]:
        raise UserNotRegisteredError(
            f"User {user_id} is not registered"
        )

    return user


async def create_vote(
    vote_data: CreateVoteRequest
) -> VoteResponse:

    await validate_registered_user(vote_data.user_id)

    async with database.transaction():

        question = await question_repository.get_question_for_update(
            vote_data.question_id
        )

        if question is None:
            raise QuestionNotFoundError(
                "Question was not found"
            )

        existing_vote = (
            await vote_repository.get_vote_by_user_and_question(
                vote_data.user_id,
                vote_data.question_id
            )
        )

        if existing_vote is not None:
            raise VoteAlreadyExistsError(
                "User already voted on this question"
            )

        try:
            vote_id = await vote_repository.create_vote(
                user_id=vote_data.user_id,
                question_id=vote_data.question_id,
                selected_option=vote_data.selected_option
            )

        except (
            MySQLIntegrityError,
            SQLAlchemyIntegrityError
        ) as error:

            original_error = getattr(error, "orig", error)

            if original_error.args and original_error.args[0] == 1062:
                raise VoteAlreadyExistsError(
                    "User already voted on this question"
                ) from error

            raise

        saved_vote = await vote_repository.get_vote_by_id(
            vote_id
        )

        return VoteResponse.model_validate(
            dict(saved_vote._mapping)
        )


async def get_vote_by_id(
    vote_id: int
) -> VoteResponse:

    vote = await vote_repository.get_vote_by_id(
        vote_id
    )

    if vote is None:
        raise VoteNotFoundError(
            f"Vote with ID {vote_id} was not found"
        )

    return VoteResponse.model_validate(
        dict(vote._mapping)
    )


async def update_vote(
    vote_id: int,
    requesting_user_id: int,
    vote_data: UpdateVoteRequest
) -> VoteResponse:

    await validate_registered_user(requesting_user_id)

    async with database.transaction():

        vote = await vote_repository.get_vote_for_update(
            vote_id
        )

        if vote is None:
            raise VoteNotFoundError(
                f"Vote with ID {vote_id} was not found"
            )

        if vote.user_id != requesting_user_id:
            raise VoteAccessDeniedError(
                "This vote belongs to another user"
            )

        await vote_repository.update_vote(
            vote_id=vote_id,
            selected_option=vote_data.selected_option
        )

        updated_vote = await vote_repository.get_vote_by_id(
            vote_id
        )

        return VoteResponse.model_validate(
            dict(updated_vote._mapping)
        )


async def delete_vote(
    vote_id: int,
    requesting_user_id: int
) -> None:

    async with database.transaction():

        vote = await vote_repository.get_vote_for_update(
            vote_id
        )

        if vote is None:
            raise VoteNotFoundError(
                f"Vote with ID {vote_id} was not found"
            )

        if vote.user_id != requesting_user_id:
            raise VoteAccessDeniedError(
                "This vote belongs to another user"
            )

        await vote_repository.delete_vote(
            vote_id
        )


async def delete_all_votes_by_user(
    user_id: int
) -> None:

    async with database.transaction():

        await vote_repository.delete_votes_by_user_id(
            user_id
        )
