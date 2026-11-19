
import asyncio

from config.database import database
from model.vote_request import CreateVoteRequest
from repository import question_repository
from service.vote_service import create_vote

TEST_USER_ID = 1


async def main():
    await database.connect()

    try:
        question_id = await question_repository.create_question(
            title="Favorite programming language?",
            option_1="Python",
            option_2="Java",
            option_3="C++",
            option_4="Go"
        )

        vote_data = CreateVoteRequest(
            user_id=TEST_USER_ID,
            question_id=question_id,
            selected_option=2
        )

        vote = await create_vote(vote_data)

        print("Created vote:", vote.model_dump())

    finally:
        await database.disconnect()


asyncio.run(main())
