from fastapi import FastAPI
from .routers import user

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(user.router)