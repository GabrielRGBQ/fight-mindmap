from pydantic import BaseModel, EmailStr

"""
Define models that must be used when calling the API as well as the format
of the returned data
"""

############################################
# ## USER
############################################

class User(BaseModel):
    name: str
    email: EmailStr