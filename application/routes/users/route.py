from fastapi import APIRouter, Request, Response
from validations.request.auth.auth import RequestLogin, RequestRegister


users_route = APIRouter(prefix="/users", tags=["Users"])


@users_route.get("/list", description="List Users")
async def users_list(request: Request, login_data: RequestLogin, response: Response):
    print("headers", dict(request.headers))
    response.headers["X-Cat-Dog"] = "alone in the world"
    print("login_data", login_data)
    return {"message": "an endpoint"}


@users_route.post("/create", description="Create User with UUID")
async def users_create(request: Request, login_data: RequestLogin, response: Response):
    print("headers", dict(request.headers))
    response.headers["X-Cat-Dog"] = "alone in the world"
    print("login_data", login_data)
    return {"message": "an endpoint"}


@users_route.post("/update", description="Update User with UUID")
async def users_update(request: Request, login_data: RequestLogin, response: Response):
    print("headers", dict(request.headers))
    response.headers["X-Cat-Dog"] = "alone in the world"
    print("login_data", login_data)
    return {"message": "an endpoint"}
