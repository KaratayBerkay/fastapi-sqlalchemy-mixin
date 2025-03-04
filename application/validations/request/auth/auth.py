from pydantic import BaseModel


class RequestLogin(BaseModel):

    email: str
    password: str

    model_config = {
        "json_schema_extra": {
            "examples": [{"email": "someemail@email.com", "password": "somepassword"}]
        }
    }


class RequestRegister(BaseModel):

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
