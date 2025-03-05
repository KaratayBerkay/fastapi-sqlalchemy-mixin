from fastapi import APIRouter, Request, Response
from validations.request.auth.auth import RequestLogin, RequestRegister


auth_route = APIRouter(prefix="/auth", tags=["Auth"])


@auth_route.get("/list", description="Login Route")
async def login(request: Request, login_data: RequestLogin, response: Response):
    print("headers", dict(request.headers))
    response.headers["X-Cat-Dog"] = "alone in the world"
    print("login_data", login_data)
    return {"message": "Login endpoint"}


@auth_route.post("/create", description="Register Route")
async def register(request: Request, register_data: RequestRegister, response: Response):
    print("headers", dict(request.headers))
    response.headers["X-Cat-Dog"] = "alone in the world"
    print("register_data", register_data)
    return {"message": "Register endpoint"}



@auth_route.post("/update", description="Register Route")
async def register(request: Request, register_data: RequestRegister, response: Response):
    print("headers", dict(request.headers))
    response.headers["X-Cat-Dog"] = "alone in the world"
    print("register_data", register_data)
    return {"message": "Register endpoint"}