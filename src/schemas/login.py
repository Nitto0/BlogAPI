from pydantic import BaseModel
from pydantic import EmailStr


class LoginSchema(BaseModel):
    email: EmailStr
    password: str
