
from config.database import database


async def create_question(
    title: str,
    option_1: str,
    option_2: str,
    option_3: str,
    option_4: str
) -> int:

    query = """
        INSERT INTO questions (
            title,
            option_1,
            option_2,
            option_3,
            option_4
        )
        VALUES (
            :title,
            :option_1,
            :option_2,
            :option_3,
            :option_4
        )
    """

    values = {
        "title": title,
        "option_1": option_1,
        "option_2": option_2,
        "option_3": option_3,
        "option_4": option_4
    }

    question_id = await database.execute(
        query=query,
        values=values
    )

    return question_id



async def get_question_by_id(question_id: int):

    query = """
        SELECT *
        FROM questions
        WHERE id = :question_id
    """

    result = await database.fetch_one(
        query=query,
        values={"question_id": question_id}
    )

    return result


async def get_all_questions():

    query = """
        SELECT *
        FROM questions
        ORDER BY id ASC
    """

    return await database.fetch_all(query=query)


async def update_question(
    question_id: int,
    values: dict
):

    query = """
        UPDATE questions
        SET
            title = :title,
            option_1 = :option_1,
            option_2 = :option_2,
            option_3 = :option_3,
            option_4 = :option_4
        WHERE id = :question_id
    """

    await database.execute(
        query=query,
        values={
            "question_id": question_id,
            **values
        }
    )


async def delete_question(question_id: int):

    query = """
        DELETE FROM questions
        WHERE id = :question_id
    """

    await database.execute(
        query=query,
        values={"question_id": question_id}
    )




async def count_votes_by_question( question_id: int) -> int:

    query = """
        SELECT COUNT(*)
        FROM votes
        WHERE question_id = :question_id
    """

    count = await database.fetch_val(
        query=query,
        values={"question_id": question_id}
    )

    return int(count)


async def get_question_for_update(question_id: int):

    query = """
        SELECT *
        FROM questions
        WHERE id = :question_id
        FOR UPDATE
    """

    return await database.fetch_one(
        query=query,
        values={"question_id": question_id}
    )
