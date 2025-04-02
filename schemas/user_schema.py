from sanic_ext import openapi
from pydantic import BaseModel
from typing import Optional


class UserSignUpSchema(BaseModel):
    e_mail: str

    class Config:
        from_attributes = True




@openapi.component
class UserSignInSchema(BaseModel):
    e_mail: str
    password: str

    class Config:
        from_attributes = True


class UserUpdateSchema(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    e_mail: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None

    class Config:
        from_attributes = True


class UserShow(BaseModel):
    id: str
    name: str
    surname: str
    e_mail: str
    password: str
    is_admin: bool

    class Config:
        from_attributes = True

class UserInsertSchema(BaseModel):
    name: str
    surname: str
    e_mail: str
    password: str

    class Config:
        from_attributes = True

class UserDeleteSchema(BaseModel):
    id: str
    class Config:
        from_attributes = True