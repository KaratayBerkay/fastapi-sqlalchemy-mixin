from fastapi import APIRouter


def get_routes() -> list[APIRouter]:
    from .auth.route import auth_route
    from .notes.route import notes_route
    from .users.route import users_route

    return [
        auth_route,
        notes_route,
        users_route,
    ]


def get_safe_endpoint_urls() -> list[tuple[str, str]]:
    return [
        ("/", "GET"),
        ("/docs", "GET"),
        ("/redoc", "GET"),
        ("/openapi.json", "GET"),
        ("/auth/register", "POST"),
        ("/auth/login", "POST"),
        ("/metrics", "GET"),
    ]
