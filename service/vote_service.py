from pymysql.err import IntegrityError as MySQLIntegrityError
from sqlalchemy.exc import IntegrityError as SQLAlchemyIntegrityError
from clients.user_client import get_user
from config.database import database
from model.vote_request import CreateVoteRequest
from model.vote_response import VoteResponse
from repository import question_repository, vote_repository
from exceptions.vote_exceptions import (
    VoteAlreadyExistsError,
    UserNotRegisteredError
)
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
