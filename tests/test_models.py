
from pydantic import ValidationError

from model.question_request import CreateQuestionRequest
from model.vote_request import CreateVoteRequest


def test_question():
    question = CreateQuestionRequest(
        title="What is your favorite sport?",
        option_1="Football",
        option_2="Basketball",
        option_3="Tennis",
        option_4="Swimming"
    )

    print("Question:", question.model_dump())


def test_invalid_vote():
    try:
        vote = CreateVoteRequest(
            user_id=5,
            question_id=1,
            selected_option=7
        )

        print(vote.model_dump())

    except ValidationError as error:
        print("Validation failed:")
        print(error)


test_question()
test_invalid_vote()
