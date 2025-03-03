import routes

from fastapi import FastAPI
from fastapi import Request
from middlewares.token_middleware import token_middleware
from controllers.route_controllers import RouteRegisterController


app = FastAPI()


route_register = RouteRegisterController(app=app, router_list=list(routes.__all__))


@app.middleware("http")
async def add_token_middleware(request: Request, call_next):
    return await token_middleware(request, call_next)
