from fastapi import APIRouter
from ..model import schemas

"""
User-related API calls
"""

router = APIRouter(prefix='/users', tags=['Users'])

@router.post("/", response_model=schemas.User)
async def create_user(user: schemas.User) -> schemas.User:
    """
    Create a new user
    """
    return user