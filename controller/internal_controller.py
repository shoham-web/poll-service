from fastapi import APIRouter, status
from service import vote_service


router = APIRouter(
    prefix="/internal",
    tags=["Internal"]
)


@router.delete(
    "/users/{user_id}/votes",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_user_votes(user_id: int):

    await vote_service.delete_all_votes_by_user(
        user_id
    )
