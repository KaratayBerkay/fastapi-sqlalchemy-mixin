from fastapi import APIRouter, Request, Response


auth_route = APIRouter(prefix="/auth", tags=["auth"])


@auth_route.get("/login", description="Login endpoint")
async def login(request: Request, response: Response):
    response.headers["X-Cat-Dog"] = "alone in the world"
    return {"message": "Login endpoint"}


@auth_route.post("/register", description="Register endpoint")
async def register(request: Request, response: Response):
    response.headers["X-Cat-Dog"] = "alone in the world"
    return {"message": "Register endpoint"}
