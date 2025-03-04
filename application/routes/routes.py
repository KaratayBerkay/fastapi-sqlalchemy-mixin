from fastapi import APIRouter


def get_routes() -> list[APIRouter]:
    from .auth.route import auth_route

    return [
        auth_route,
    ]


def get_safe_endpoint_urls() -> list[tuple[str, str]]:
    return [
        ('/', "GET"),
        ('/docs', "GET"),
        ('/redoc', "GET"),
        ('/openapi.json', "GET"),
        ('/auth/register', "POST"),
        ('/auth/login', "GET"),
        ('/metrics', "GET"),
    ]
