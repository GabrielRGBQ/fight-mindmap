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
