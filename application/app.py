import time

import uvicorn

from controllers.route_controllers import RouteRegisterController
from controllers.open_api_controllers import create_openapi_schema
from controllers.alembic_controller import AlembicController

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from middlewares.token_middleware import token_middleware
from prometheus_fastapi_instrumentator import Instrumentator

from routes.routes import get_routes
from services.database.database import get_db


def create_app(set_alembic: bool = True):

    if set_alembic:  # Initialize AlembicController with active database session
        with get_db() as active_session:
            controller = AlembicController(session=active_session)
            controller.update_alembic()

    application = FastAPI(
        title="FastAPI Application",
        description="FastAPI Application with OpenAPI schema configuration, security scheme configuration for Bearer authentication, automatic router registration, response class configuration, and security requirements for protected endpoints.",
        version="0.1.0",
    )
    application.mount(
        "/application/static",
        StaticFiles(directory="application/static"),
        name="static",
    )
    application.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost", "http://localhost:8000"
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @application.middleware("http")
    async def add_token_middleware(request: Request, call_next):
        return await token_middleware(request, call_next)

    @application.get("/", description="Redirect Route", include_in_schema=False)
    async def redirect_to_docs():
        return RedirectResponse(url="/docs")

    route_register = RouteRegisterController(app=application, router_list=get_routes())
    application = route_register.register_routes()
    application.openapi = lambda _=application: create_openapi_schema(_)
    return application


app = create_app(set_alembic=True)                          # Create FastAPI application
Instrumentator().instrument(app=app).expose(app=app)        # Setup Prometheus metrics


if __name__ == "__main__":
    while True:
        time.sleep(5)

    # uvicorn_config = uvicorn.Config(
    #     app="app:app", host="0.0.0.0", port=8000, log_level="info", reload=True
    # )
    # uvicorn.Server(uvicorn_config).run()  # Run the application with Uvicorn Server
