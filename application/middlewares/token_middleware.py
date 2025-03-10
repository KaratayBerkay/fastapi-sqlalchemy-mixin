from fastapi import Request, Response


async def token_middleware(request: Request, call_next):
    from application.routes.routes import get_safe_endpoint_urls

    base_url = "/".join(request.url.path.split("/")[:3])
    safe_endpoints = [_[0] for _ in get_safe_endpoint_urls()]
    if base_url in safe_endpoints:
        return await call_next(request)

    token = request.headers.get("Authorization")
    if not token:
        return Response(content="Missing token", status_code=400)

    response = await call_next(request)
    return response
