
import asyncio

from clients.user_client import get_user


async def main():
    user = await get_user(1)
    print("User:", user)
    print("Registered:", user["is_registered"])


asyncio.run(main())
