from pydantic import BaseModel, EmailStr, SecretStr, Field


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: SecretStr = Field(min_length=8, pattern=r".*[A-Z].*")
