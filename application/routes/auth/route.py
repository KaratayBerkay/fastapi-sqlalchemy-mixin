from fastapi import APIRouter, Request, Response
from application.validations.request.auth.auth import RequestLogin, RequestRegister
from application.controllers.token_controllers import jwt_controller
from application.schemas.users.model import User

auth_route = APIRouter(prefix="/auth", tags=["Auth"])


@auth_route.post("/login", description="Login Route")
async def login(request: Request, login_data: RequestLogin, response: Response):

    headers = dict(request.headers)
    # todo find user requested and add to payload
    db_session = User.new_session()
    active_user = User.filter_one(User.email == login_data.email, db=db_session)
    print("query", active_user.query)
    print("data", active_user.data)
    print("as_dict", active_user.as_dict)
    print("count", active_user.count)
    print("total_count", active_user.total_count)
    print("is_list", active_user.is_list)
    if not active_user.count:
        return {
            "message": "User not found",
            "info": {
                "host": headers.get("host", "Not Found"),
                "user_agent": headers.get("user-agent", "Not Found"),
            },
        }
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
    return {"message": "Register endpoint", "headers": headers}
