from pydantic import BaseModel


class Login(BaseModel):
    email: str
    password: str

    model_config = {
        "json_schema_extra": {
            "examples": [{"email": "someemail@email.com", "password": "somepassword"}]
        }
    }


class Register(BaseModel):
    name: str
    surname: str
    password: str
    email: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "someemail@email.com",
                    "password": "somepassword",
                    "surname": "somesurname",
                    "name": "somename",
                }
            ]
        }
    }
