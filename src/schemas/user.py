from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import SecretStr
from pydantic import Field


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: SecretStr = Field(min_length=8, pattern=r".*[A-Z].*")
