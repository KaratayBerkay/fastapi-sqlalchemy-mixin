from pydantic import BaseModel
from uuid import uuid4


class RequestNotesList(BaseModel):

    title: str
    content: str
    user_uu_id: str

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "title": "sometitle",
                "content": "somecontent",
                "user_uu_id": str(uuid4())
            }]
        }
    }


class RequestNotesCreate(BaseModel):

    title: str
    content: str
    user_uu_id: str

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "title": "sometitle",
                "content": "somecontent",
                "user_uu_id": str(uuid4())
            }]
        }
    }
