from config.database import database


async def create_vote(
    user_id: int,
    question_id: int,
    selected_option: int
) -> int:

    query = """
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
    """

    values = {
        "user_id": user_id,
        "question_id": question_id,
        "selected_option": selected_option
    }

    vote_id = await database.execute(
        query=query,
        values=values
    )

    return vote_id


async def get_vote_by_id(vote_id: int):

    query = """
        SELECT *
        FROM votes
        WHERE id = :vote_id
    """

    return await database.fetch_one(
        query=query,
        values={"vote_id": vote_id}
    )


async def get_vote_by_user_and_question(
    user_id: int,
    question_id: int
):

    query = """
        SELECT *
        FROM votes
        WHERE user_id = :user_id
          AND question_id = :question_id
    """

    return await database.fetch_one(
        query=query,
        values={
            "user_id": user_id,
            "question_id": question_id
        }
    )


async def update_vote(
    vote_id: int,
    selected_option: int
):

    query = """
        UPDATE votes
        SET selected_option = :selected_option
        WHERE id = :vote_id
    """

    await database.execute(
        query=query,
        values={
            "vote_id": vote_id,
            "selected_option": selected_option
        }
    )


async def delete_vote(vote_id: int):

    query = """
        DELETE FROM votes
        WHERE id = :vote_id
    """

    await database.execute(
        query=query,
        values={"vote_id": vote_id}
    )


async def get_votes_by_user(user_id: int):

    query = """
        SELECT *
        FROM votes
        WHERE user_id = :user_id
        ORDER BY question_id ASC
    """

    return await database.fetch_all(
        query=query,
        values={"user_id": user_id}
    )


async def count_votes_by_user(user_id: int) -> int:

    query = """
        SELECT COUNT(*)
        FROM votes
        WHERE user_id = :user_id
    """

    count = await database.fetch_val(
        query=query,
        values={"user_id": user_id}
    )

    return int(count)


async def delete_votes_by_user(user_id: int):

    query = """
        DELETE FROM votes
        WHERE user_id = :user_id
    """

    await database.execute(
        query=query,
        values={"user_id": user_id}
    )


async def get_vote_for_update(vote_id: int):

    query = """
        SELECT *
        FROM votes
        WHERE id = :vote_id
        FOR UPDATE
    """

    return await database.fetch_one(
        query=query,
        values={"vote_id": vote_id}
    )
