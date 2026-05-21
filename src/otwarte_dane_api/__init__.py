"""Typed Python client for DANE.GOV.PL Open Data API."""

from .client import AsyncOtwarteDaneClient, OtwarteDaneClient
from .exceptions import (
    ApiError,
    AuthenticationError,
    BadRequestError,
    NotFoundError,
    RateLimitError,
    ServerError,
)

__all__ = [
    "OtwarteDaneClient",
    "AsyncOtwarteDaneClient",
    "ApiError",
    "BadRequestError",
    "AuthenticationError",
    "NotFoundError",
    "RateLimitError",
    "ServerError",
]

__version__ = "0.1.0"
