
from config.database import database


async def get_question_statistics(question_id: int):
    query = """
        SELECT
            question_id,

            COUNT(*) AS total_votes,

            SUM(
                CASE WHEN selected_option = 1
                THEN 1 ELSE 0 END
            ) AS option_1_votes,

            SUM(
                CASE WHEN selected_option = 2
                THEN 1 ELSE 0 END
            ) AS option_2_votes,

            SUM(
                CASE WHEN selected_option = 3
                THEN 1 ELSE 0 END
            ) AS option_3_votes,

            SUM(
                CASE WHEN selected_option = 4
                THEN 1 ELSE 0 END
            ) AS option_4_votes

        FROM votes

        WHERE question_id = :question_id

        GROUP BY question_id
    """

    return await database.fetch_one(
        query=query,
        values={"question_id": question_id}
    )


async def get_all_questions_statistics():
    query = """
        SELECT
            q.id AS question_id,
            q.title AS question_title,

            COUNT(v.id) AS total_votes,

            COUNT(
                CASE WHEN v.selected_option = 1
                THEN 1 END
            ) AS option_1_votes,

            COUNT(
                CASE WHEN v.selected_option = 2
                THEN 1 END
            ) AS option_2_votes,

            COUNT(
                CASE WHEN v.selected_option = 3
                THEN 1 END
            ) AS option_3_votes,

            COUNT(
                CASE WHEN v.selected_option = 4
                THEN 1 END
            ) AS option_4_votes

        FROM questions q

        LEFT JOIN votes v
            ON q.id = v.question_id

        GROUP BY q.id, q.title

        ORDER BY q.id
    """

    return await database.fetch_all(query=query)


async def get_user_vote_statistics(user_id: int):
    query = """
        SELECT
            v.id AS vote_id,
            v.question_id,
            q.title AS question_title,
            v.selected_option

        FROM votes v

        JOIN questions q
            ON q.id = v.question_id

        WHERE v.user_id = :user_id

        ORDER BY v.question_id
    """

    return await database.fetch_all(
        query=query,
        values={"user_id": user_id}
    )
