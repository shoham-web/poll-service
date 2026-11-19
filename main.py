from contextlib import asynccontextmanager
from fastapi import FastAPI
from config.database import database
from controller.question_controller import router as question_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    print("Poll Service connected to MySQL")

    try:
        yield
    finally:
        await database.disconnect()
        print("Poll Service disconnected from MySQL")


app = FastAPI(
    title="Poll System - Poll Service",
    lifespan=lifespan
)

app.include_router(question_router)


@app.get("/health")
async def health_check():
    return {"status": "ok"}
