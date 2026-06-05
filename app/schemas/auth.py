from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserRegister(BaseModel):
    name: str = Field(..., min_length=2, max_length=20)
    surname: str = Field(..., min_length=2, max_length=20)
    middle_name: str = Field(..., min_length=2, max_length=20)
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=4, max_length=20)
    password_repeat: str = Field(..., min_length=4, max_length=20)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=20)
    surname: str | None = Field(None, min_length=2, max_length=20)
    middle_name: str | None = Field(None, min_length=2, max_length=20)
    email: EmailStr | None = Field(None)


class UserResponse(BaseModel):
    id: int
    name: str
    surname: str
    middle_name: str
    email: EmailStr
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
