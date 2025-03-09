from typing import Dict, Any

from fastapi import FastAPI
from fastapi.routing import APIRoute
from fastapi.openapi.utils import get_openapi


class OpenAPISchemaCreator:
    """
    OpenAPI schema creator and customizer for FastAPI applications.
    """

    def __init__(self, app: FastAPI):
        """
        Initialize the OpenAPI schema creator.

        Args:
            app: FastAPI application instance
        """
        from routes.routes import get_routes, get_safe_endpoint_urls

        self.app = app
        self.safe_endpoint_list: list[tuple[str, str]] = get_safe_endpoint_urls()
        self.routers_list = self.app.routes

    @staticmethod
    def _create_security_schemes() -> Dict[str, Any]:
        """
        Create security scheme definitions.

        Returns:
            Dict[str, Any]: Security scheme configurations
        """

        return {
            "BearerAuth": {
                "type": "apiKey",
                "in": "header",
                "name": "Authorization",
                "description": "Enter: **'Bearer &lt;JWT&gt;'**, where JWT is the access token",
            }
        }

    def configure_route_security(
        self, path: str, method: str, schema: Dict[str, Any]
    ) -> None:
        """
        Configure security requirements for a specific route.

        Args:
            path: Route path
            method: HTTP method
            schema: OpenAPI schema to modify
        """
        if not schema.get("paths", {}).get(path, {}).get(method):
            return

        # Check if endpoint is in safe list
        endpoint_path = f"{path}:{method}"
        list_of_safe_endpoints = [
            f"{e[0]}:{str(e[1]).lower()}" for e in self.safe_endpoint_list
        ]
        print(
            "endpoint_path",
            endpoint_path,
            "list_of_safe_endpoints",
            list_of_safe_endpoints,
        )
        if endpoint_path not in list_of_safe_endpoints:
            if "security" not in schema["paths"][path][method]:
                schema["paths"][path][method]["security"] = []
            schema["paths"][path][method]["security"].append({"BearerAuth": []})

    def create_schema(self) -> Dict[str, Any]:
        """
        Create the complete OpenAPI schema.

        Returns:
            Dict[str, Any]: Complete OpenAPI schema
        """
        openapi_schema = get_openapi(
            title="Fastapi API Backend",
            description="Fastapi API Backend for Docker API Services",
            version="1.1.1",
            routes=self.app.routes,
        )

        # Add security schemes
        if "components" not in openapi_schema:
            openapi_schema["components"] = {}

        openapi_schema["components"][
            "securitySchemes"
        ] = self._create_security_schemes()

        # Configure route security and responses
        for route in self.app.routes:
            if isinstance(route, APIRoute) and route.include_in_schema:
                path = str(route.path)
                methods = [str(method).lower() for method in route.methods]
                for method in methods:
                    self.configure_route_security(path, method, openapi_schema)

        # Add custom documentation extensions
        openapi_schema["x-documentation"] = {
            "postman_collection": "/docs/postman",
            "swagger_ui": "/docs",
            "redoc": "/redoc",
        }
        return openapi_schema


def create_openapi_schema(app: FastAPI) -> Dict[str, Any]:
    """
    Create OpenAPI schema for a FastAPI application.

    Args:
        app: FastAPI application instance

    Returns:
        Dict[str, Any]: Complete OpenAPI schema
    """
    if app.openapi_schema:
        return app.openapi_schema

    creator = OpenAPISchemaCreator(app)
    app.openapi_schema = creator.create_schema()
    return app.openapi_schema
