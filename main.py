from contextlib import asynccontextmanager
from fastapi import FastAPI
from config.database import database
from controller.question_controller import router as question_router
from controller.vote_controller import router as vote_router
from controller.statistics_controller import router as statistics_router
from controller.internal_controller import  router as internal_router

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
app.include_router(vote_router)
app.include_router(statistics_router)
app.include_router(internal_router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}

