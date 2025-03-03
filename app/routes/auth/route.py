from fastapi import APIRouter


auth_route = APIRouter(prefix="/auth", tags=["auth"])


@auth_route.get("/login", description="Login endpoint")
async def login():
    return {"message": "Login endpoint"}


@auth_route.post("/register", description="Register endpoint")
async def register():
    return {"message": "Register endpoint"}
