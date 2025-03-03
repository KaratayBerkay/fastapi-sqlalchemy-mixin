from pydantic import BaseModel


class RequestLogin(BaseModel):
    email: str
    password: str


class RequestRegister(BaseModel):
    name: str
    surname: str
    password: str
    email: str
