
import asyncio

from config.database import database
from repository import (
    question_repository,
    vote_repository
)


async def main():
    await database.connect()
    question_id = None

    try:
    
        question_id = await question_repository.create_question(
            title="Favorite programming language?",
            option_1="Python",
            option_2="Java",
            option_3="C++",
            option_4="JavaScript"
        )


        vote_id = await vote_repository.create_vote(
            user_id=999999,
            question_id=question_id,
            selected_option=2
        )

        print("Created vote ID:", vote_id)


        vote = await vote_repository.get_vote_by_id(vote_id)
        assert vote is not None

        print("Vote:", dict(vote._mapping))


        existing_vote = (
            await vote_repository.get_vote_by_user_and_question(
                user_id=999999,
                question_id=question_id
            )
        )

        assert existing_vote is not None
        assert existing_vote.id == vote_id
        print("Existing vote found")


        await vote_repository.update_vote(
            vote_id=vote_id,
            selected_option=4
        )

        updated_vote = await vote_repository.get_vote_by_id(
            vote_id
        )

        assert updated_vote.selected_option == 4
        print("Updated option:", updated_vote.selected_option)


        count = await vote_repository.count_votes_by_user(
            999999
        )

        print("User votes count:", count)


        await vote_repository.delete_vote(vote_id)

        deleted_vote = await vote_repository.get_vote_by_id(
            vote_id
        )

        assert deleted_vote is None
        print("Vote deleted successfully")

    finally:
        if question_id is not None:
            await question_repository.delete_question(
                question_id
            )

        await database.disconnect()


asyncio.run(main())
