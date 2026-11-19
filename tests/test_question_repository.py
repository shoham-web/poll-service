
import asyncio

from config.database import database
from repository import question_repository


async def main():
    await database.connect()

    try:
        question_id = await question_repository.create_question(
            title="What is your favorite sport?",
            option_1="Football",
            option_2="Basketball",
            option_3="Tennis",
            option_4="Swimming"
        )

        print("Created question ID:", question_id)


        question = await question_repository.get_question_by_id(
            question_id
        )

        print("Question:", dict(question._mapping))

        updated_values = {
            "title": "What sport do you prefer?",
            "option_1": "Football",
            "option_2": "Basketball",
            "option_3": "Tennis",
            "option_4": "Swimming"
        }

        await question_repository.update_question(
            question_id,
            updated_values
        )


        updated_question = await question_repository.get_question_by_id(
            question_id
        )

        print("Updated:", dict(updated_question._mapping))


        votes_count = await question_repository.count_votes_by_question(
            question_id
        )

        print("Votes count:", votes_count)


        questions = await question_repository.get_all_questions()

        print("Total questions:", len(questions))


        await question_repository.delete_question(question_id)

        deleted_question = await question_repository.get_question_by_id(
            question_id
        )

        print("After delete:", deleted_question)

    finally:
        await database.disconnect()


asyncio.run(main())
