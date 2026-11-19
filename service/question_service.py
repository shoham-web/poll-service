from model.question_request import ( CreateQuestionRequest, UpdateQuestionRequest)
from model.question_response import QuestionResponse
from repository import question_repository
from exceptions.question_exceptions import ( QuestionNotFoundError,QuestionHasVotesError)
from repository.question_repository import get_question_by_id
from config.database import database


async def create_question(question_data: CreateQuestionRequest) -> QuestionResponse:

    question_id = await question_repository.create_question(
        title=question_data.title,
        option_1=question_data.option_1,
        option_2=question_data.option_2,
        option_3=question_data.option_3,
        option_4=question_data.option_4
    )

    return await get_question_by_id(question_id)



async def get_question_by_id(question_id: int) -> QuestionResponse:

    question = await question_repository.get_question_by_id(question_id)

    if question is None:
        raise QuestionNotFoundError(f"Question with ID {question_id} was not found")
    return QuestionResponse.model_validate(dict(question._mapping) )


async def get_all_questions() -> list[QuestionResponse]:

    questions = await question_repository.get_all_questions()
    result = []

    for question in questions:
        question_response = QuestionResponse.model_validate(
            dict(question._mapping)
        )

        result.append(question_response)

    return result


async def update_question(
    question_id: int,
    question_data: UpdateQuestionRequest
) -> QuestionResponse:

    async with database.transaction():

        question = await question_repository.get_question_for_update(
            question_id
        )

        if question is None:
            raise QuestionNotFoundError(
                f"Question with ID {question_id} was not found"
            )

        votes_count = await question_repository.count_votes_by_question(
            question_id
        )

        if votes_count > 0:
            raise QuestionHasVotesError(
                "Cannot update a question with existing votes"
            )

        current_data = dict(question._mapping)

        update_data = question_data.model_dump(
            exclude_unset=True
        )

        updated_values = {
            field: update_data.get(
                field, current_data[field]
            )
            for field in (
                "title",
                "option_1",
                "option_2",
                "option_3",
                "option_4"
            )
        }

        await question_repository.update_question(
            question_id,
            updated_values
        )

        return await get_question_by_id(question_id)


async def delete_question(question_id: int) -> None:

    async with database.transaction():

        question = await question_repository.get_question_for_update(
            question_id
        )

        if question is None:
            raise QuestionNotFoundError(
                f"Question with ID {question_id} was not found"
            )

        await question_repository.delete_question(
            question_id
        )
