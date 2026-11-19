
import asyncio

from config.database import database

from model.question_request import (
    CreateQuestionRequest,
    UpdateQuestionRequest
)

from service import question_service

from exceptions.question_exceptions import (
    QuestionNotFoundError,
    QuestionHasVotesError
)


async def main():
    await database.connect()

    try:
        question_data = CreateQuestionRequest(
            title="What is your favorite sport?",
            option_1="Football",
            option_2="Basketball",
            option_3="Tennis",
            option_4="Swimming"
        )

        question = await question_service.create_question(
            question_data
        )

        question_id = question.id

        print("Created:", question.model_dump())


        update_data = UpdateQuestionRequest(
            option_4="Boxing"
        )

        updated_question = await question_service.update_question(
            question_id,
            update_data
        )

        print("Updated:", updated_question.model_dump())

        questions = await question_service.get_all_questions()

        print("Total questions:", len(questions))

        await database.execute(
            query="""
                INSERT INTO votes (
                    user_id,
                    question_id,
                    selected_option
                )
                VALUES (
                    :user_id,
                    :question_id,
                    :selected_option
                )
            """,
            values={
                "user_id": 999999,
                "question_id": question_id,
                "selected_option": 1
            }
        )

        try:
            await question_service.update_question(
                question_id,
                UpdateQuestionRequest(
                    title="New question title"
                )
            )

            raise AssertionError(
                "Update should have been blocked"
            )

        except QuestionHasVotesError as error:
            print("Expected business error:", error)

        await question_service.delete_question(
            question_id
        )

        votes_count = await database.fetch_val(
            query="""
                SELECT COUNT(*)
                FROM votes
                WHERE question_id = :question_id
            """,
            values={"question_id": question_id}
        )

        assert votes_count == 0

        print("Votes after delete:", votes_count)

        try:
            await question_service.get_question_by_id(
                question_id
            )

            raise AssertionError(
                "Question should have been deleted"
            )

        except QuestionNotFoundError as error:
            print("Expected error:", error)

    finally:
        await database.disconnect()


asyncio.run(main())
