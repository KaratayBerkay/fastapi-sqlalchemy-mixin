from fastapi import APIRouter, Request, Response
from validations.request.auth.auth import RequestLogin, RequestRegister
from controllers.token_controllers import jwt_controller

auth_route = APIRouter(prefix="/auth", tags=["Auth"])


@auth_route.post("/login", description="Login Route")
async def login(request: Request, login_data: RequestLogin, response: Response):
    headers = dict(request.headers)

    access_token = jwt_controller.create_access_token(
        payload={
            "username": login_data.email,
            "info": {
                "host": headers.get("host", "Not Found"),
                "user_agent": headers.get("user-agent", "Not Found"),
            },
        }
    )
    response.headers["Authorization"] = access_token
    return {"message": "Access Token Created", "headers": headers}


@auth_route.post("/register", description="Register Route")
async def register(
    request: Request, register_data: RequestRegister, response: Response
):
    headers = dict(request.headers)
    response.headers["X-Cat-Dog"] = "alone in the world"
    return {"message": "Register endpoint", "headers": headers}
