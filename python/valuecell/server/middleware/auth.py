"""Basic HTTP Authentication middleware for ValueCell."""

import base64
import os
from typing import Callable

from fastapi import HTTPException, Request, status
from fastapi.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware


class BasicAuthMiddleware(BaseHTTPMiddleware):
    """Basic HTTP Authentication middleware."""

    def __init__(self, app, username: str, password: str):
        """Initialize middleware with credentials."""
        super().__init__(app)
        self.username = username
        self.password = password
        self.credentials = base64.b64encode(
            f"{username}:{password}".encode()
        ).decode()

    async def dispatch(self, request: Request, call_next: Callable):
        """Check authentication before processing request."""
        # Skip auth for health check
        if request.url.path == "/api/v1/health":
            return await call_next(request)

        # Get authorization header
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Basic "):
            return Response(
                status_code=status.HTTP_401_UNAUTHORIZED,
                headers={"WWW-Authenticate": 'Basic realm="ValueCell"'},
                content="Authentication required",
            )

        # Verify credentials
        try:
            provided_credentials = auth_header.split(" ")[1]
            if provided_credentials != self.credentials:
                raise HTTPException(status_code=401)
        except Exception:
            return Response(
                status_code=status.HTTP_401_UNAUTHORIZED,
                headers={"WWW-Authenticate": 'Basic realm="ValueCell"'},
                content="Invalid credentials",
            )

        # Process request
        response = await call_next(request)
        return response


def get_auth_credentials():
    """Get authentication credentials from environment."""
    username = os.getenv("AUTH_USERNAME", "admin")
    password = os.getenv("AUTH_PASSWORD")

    if not password:
        raise ValueError(
            "AUTH_PASSWORD environment variable must be set for authentication"
        )

    return username, password
