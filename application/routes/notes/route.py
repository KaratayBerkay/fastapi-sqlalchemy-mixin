from fastapi import APIRouter, Request, Response
from application.validations.request.auth.auth import RequestLogin, RequestRegister
from application.validations.request.list_options.list_options import ListOptions
from application.schemas.notes.model import Notes, Tags, Comments


notes_route = APIRouter(prefix="/notes", tags=["Notes"])


@notes_route.get("/list", description="List Notes")
async def notes_list(request: Request, login_data: ListOptions, response: Response):
    print("headers", dict(request.headers))
    response.headers["X-Cat-Dog"] = "alone in the world"
    print("login_data", login_data)
    return {"message": "an endpoint"}


@notes_route.post("/create", description="Create Note with UUID")
async def notes_create(request: Request, login_data: RequestLogin, response: Response):
    print("headers", dict(request.headers))
    response.headers["X-Cat-Dog"] = "alone in the world"
    print("login_data", login_data)
    return {"message": "an endpoint"}


@notes_route.post("/update", description="Update Note with UUID")
async def notes_update(request: Request, login_data: RequestLogin, response: Response):
    print("headers", dict(request.headers))
    response.headers["X-Cat-Dog"] = "alone in the world"
    print("login_data", login_data)
    return {"message": "an endpoint"}
