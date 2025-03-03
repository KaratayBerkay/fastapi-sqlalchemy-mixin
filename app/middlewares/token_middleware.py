from fastapi import Request, Response


async def token_middleware(request: Request, call_next):
    token = request.headers.get("Authorization")
    if not token:
        return Response(content="Missing token", status_code=400)

    response = await call_next(request)
    return response
