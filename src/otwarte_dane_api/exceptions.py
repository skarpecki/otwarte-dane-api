"""Exception hierarchy for the DANE.GOV.PL API client."""

from __future__ import annotations

from typing import Any, Optional


class ApiError(Exception):
    """Base error raised for any non-success API response."""

    def __init__(
        self,
        message: str,
        *,
        status_code: Optional[int] = None,
        url: Optional[str] = None,
        payload: Any = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.url = url
        self.payload = payload

    def __str__(self) -> str:  # pragma: no cover - trivial
        base = super().__str__()
        if self.status_code is not None:
            return f"[{self.status_code}] {base}"
        return base


class BadRequestError(ApiError):
    """HTTP 400 — malformed request or invalid parameters."""


class AuthenticationError(ApiError):
    """HTTP 401/403."""


class NotFoundError(ApiError):
    """HTTP 404."""


class RateLimitError(ApiError):
    """HTTP 429."""


class ServerError(ApiError):
    """HTTP 5xx."""


def error_for_status(status_code: int, message: str, *, url: str, payload: Any) -> ApiError:
    """Map an HTTP status code to the most specific ApiError subclass."""
    if status_code == 400:
        cls: type[ApiError] = BadRequestError
    elif status_code in (401, 403):
        cls = AuthenticationError
    elif status_code == 404:
        cls = NotFoundError
    elif status_code == 429:
        cls = RateLimitError
    elif 500 <= status_code < 600:
        cls = ServerError
    else:
        cls = ApiError
    return cls(message, status_code=status_code, url=url, payload=payload)
