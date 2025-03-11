from fastapi import APIRouter, Request, Response

from application.controllers.auth_controllers import PasswordModule
from application.validations.request.auth.auth import RequestLogin, RequestRegister
from application.controllers.token_controllers import jwt_controller
from application.schemas.users.model import User


auth_route = APIRouter(prefix="/auth", tags=["Auth"])


@auth_route.post("/login", description="Login Route")
async def login(request: Request, login_data: RequestLogin, response: Response):
    headers = dict(request.headers)
    db_session = User.new_session()
    active_user = User.filter_one(User.email == login_data.email, db=db_session)
    if not active_user.count:
        return {
            "completed": False,
            "message": "User not found",
            "info": {
                "host": headers.get("host", "Not Found"),
                "user_agent": headers.get("user-agent", "Not Found"),
            },
        }
    active_user_data = active_user.data
    active_user_dict = active_user_data.get_dict(exclude_list=[User.hashed_password])
    password_dict = dict(password=login_data.password, salt=login_data.email, id_=active_user_data.uu_id)
    hashed_password = PasswordModule.create_hashed_password(**password_dict)
    if hashed_password != active_user_data.hashed_password:
        return {
            "completed": False,
            "message": "Password is incorrect",
            "user": active_user_dict,
            "info": {
                "host": headers.get("host", "Not Found"),
                "user_agent": headers.get("user-agent", "Not Found"),
            },
        }
    access_token = jwt_controller.create_access_token(
        payload={
            "email": login_data.email,
            "info": {
                "host": headers.get("host", "Not Found"),
                "user_agent": headers.get("user-agent", "Not Found"),
            },
        }
    )
    response.headers["Authorization"] = access_token
    return {
        "completed": True, "message": "Access Token Created", "user": active_user_dict, "access_token": access_token
    }


@auth_route.post("/register", description="Register Route")
async def register(
    register_data: RequestRegister, request: Request, response: Response
):
    new_session = User.new_session()
    dict_user = register_data.model_dump()
    dict_user['hashed_password'] = "some_password_before_hashing"
    user_created = User.find_or_create(
        **dict_user, exclude_args=[User.hashed_password], db=new_session
    )
    if user_created.meta_data.created:
        password_dict = dict(password=register_data.password, salt=register_data.email, id_=user_created.uu_id)
        hashed_password = PasswordModule.create_hashed_password(**password_dict)
        user_created.update(db=new_session, hashed_password=hashed_password)
        user_created.save(db=new_session)

    return_message = f"User email: {user_created.email} is already registered successfully. You can login with it."
    if completed := user_created.meta_data.created:
        return_message = f"User email: {user_created.email} is now registered. You can login now."
    return {
        "completed": completed,
        "message": return_message,
        "data": user_created.get_dict(exclude_list=[User.hashed_password])
    }
