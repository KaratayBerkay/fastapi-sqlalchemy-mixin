from pydantic import BaseModel


class Login(BaseModel):
    email: str
    password: str


class Register(BaseModel):
    name: str
    surname: str
    password: str
    email: str
