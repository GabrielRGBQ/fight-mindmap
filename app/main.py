from fastapi import FastAPI
from .routers import user, authentication
# from .database import engine


# Create the tables in the database if they don't already exist
# It will be needed no longer when we start using alembic
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router)
app.include_router(authentication.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}
