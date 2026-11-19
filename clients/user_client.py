import os
import httpx
from dotenv import load_dotenv
from exceptions.user_client_exceptions import (RemoteUserNotFoundError,UserServiceUnavailableError)

load_dotenv()

USER_SERVICE_URL = os.getenv(
    "USER_SERVICE_URL",
    "http://127.0.0.1:8000"
)


async def get_user(user_id: int) -> dict:

    url = f"{USER_SERVICE_URL}/users/{user_id}"

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(url)
            print("Request URL:", url)
            print("Status Code:", response.status_code)
            print("Response Body:", response.text)

    except httpx.RequestError as error:
        raise UserServiceUnavailableError(
            "Could not communicate with User Service"
        ) from error

    if response.status_code == 404:
        raise RemoteUserNotFoundError(
            f"User with ID {user_id} was not found"
        )

    if response.status_code != 200:
        raise UserServiceUnavailableError(
            "User Service returned an unexpected response"
        )

    try:
        user = response.json()

        if (
            not isinstance(user, dict)
            or type(user.get("is_registered")) is not bool
            or user.get("id") != user_id
        ):
            raise ValueError("Invalid user response")

        return user

    except (ValueError, TypeError) as error:
        raise UserServiceUnavailableError(
            "User Service returned invalid user data"
        ) from error
