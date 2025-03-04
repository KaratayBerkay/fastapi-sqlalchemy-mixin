import routes

from fastapi import FastAPI
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from middlewares.token_middleware import token_middleware
from controllers.route_controllers import RouteRegisterController


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


route_register = RouteRegisterController(app=app, router_list=list(routes.__all__))


@app.middleware("http")
async def add_token_middleware(request: Request, call_next):
    return await token_middleware(request, call_next)
