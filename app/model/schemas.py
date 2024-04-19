from typing import Optional

from pydantic import BaseModel, EmailStr

"""
Define models that must be used when calling the API as well as the format
of the returned data
"""

############################################
# ## USER
############################################

class User(BaseModel):
    email: EmailStr

class UserCreate(User):
    name: str
    password: str

class UserLogin(User):
    email: EmailStr
    password: str

class UserOut(User):
    id: int
    name: str

############################################
# ## MINDMAP
############################################

class Mindmap(BaseModel):
    name: str
    description: str
    owner_id: int

class MindmapCreate(Mindmap):
    class ConfigDict:
        orm_mode = True

class MindmapOut(Mindmap):
    owner: UserOut
    class ConfigDict:
        orm_mode = True

############################################
# ## TOKEN (AUTHENTICATION)
############################################

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None