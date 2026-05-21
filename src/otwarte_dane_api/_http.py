"""HTTP transport for the DANE.GOV.PL API client."""

from __future__ import annotations

import time
from typing import Any, Mapping, Optional

import httpx

from .exceptions import error_for_status

DEFAULT_BASE_URL = "https://api.dane.gov.pl/"
DEFAULT_API_VERSION = "1.4"
DEFAULT_TIMEOUT = 30.0


def _build_default_headers(api_version: str, lang: Optional[str]) -> dict[str, str]:
    headers = {
        "Accept": "application/vnd.api+json",
        "X-API-VERSION": api_version,
        "User-Agent": "otwarte-dane-api-python/0.1",
    }
    if lang:
        headers["Accept-Language"] = lang
    return headers


def _decode_payload(response: httpx.Response) -> Any:
    if not response.content:
        return None
    try:
        return response.json()
    except ValueError:
        return response.text


def _raise_for_status(response: httpx.Response) -> None:
    if response.is_success:
        return
    payload = _decode_payload(response)
    if isinstance(payload, dict):
        errors = payload.get("errors")
        if isinstance(errors, list) and errors:
            first = errors[0]
            if isinstance(first, dict):
                message = first.get("title") or first.get("detail") or response.reason_phrase
            else:
                message = str(first)
        else:
            message = payload.get("detail") or response.reason_phrase
    else:
        message = str(payload) if payload else response.reason_phrase
    raise error_for_status(
        response.status_code, message, url=str(response.request.url), payload=payload
    )


def _clean_params(params: Optional[Mapping[str, Any]]) -> Optional[dict[str, Any]]:
    cleaned = {key: value for key, value in (params or {}).items() if value is not None}
    return cleaned or None


class HttpTransport:
    """Synchronous httpx transport wrapper with simple retry on 5xx."""

    def __init__(
        self,
        *,
        base_url: str = DEFAULT_BASE_URL,
        api_version: str = DEFAULT_API_VERSION,
        lang: Optional[str] = None,
        timeout: float = DEFAULT_TIMEOUT,
        headers: Optional[Mapping[str, str]] = None,
        client: Optional[httpx.Client] = None,
        max_retries: int = 2,
        retry_backoff: float = 0.5,
    ) -> None:
        merged_headers = _build_default_headers(api_version, lang)
        if headers:
            merged_headers.update(headers)
        self._owns_client = client is None
        self._client = client or httpx.Client(
            base_url=base_url, headers=merged_headers, timeout=timeout
        )
        self.max_retries = max_retries
        self.retry_backoff = retry_backoff

    def _request(self, path: str, *, params: Optional[Mapping[str, Any]] = None) -> httpx.Response:
        last_exc: Optional[Exception] = None
        for attempt in range(self.max_retries + 1):
            try:
                response = self._client.get(path, params=_clean_params(params))
            except httpx.TransportError as exc:
                last_exc = exc
                if attempt >= self.max_retries:
                    raise
                time.sleep(self.retry_backoff * (2**attempt))
                continue
            if response.status_code >= 500 and attempt < self.max_retries:
                time.sleep(self.retry_backoff * (2**attempt))
                continue
            _raise_for_status(response)
            return response
        if last_exc is not None:  # pragma: no cover - defensive
            raise last_exc
        raise RuntimeError("unreachable")

    def get(self, path: str, *, params: Optional[Mapping[str, Any]] = None) -> Any:
        return _decode_payload(self._request(path, params=params))

    def get_bytes(self, path: str, *, params: Optional[Mapping[str, Any]] = None) -> bytes:
        return self._request(path, params=params).content

    def close(self) -> None:
        if self._owns_client:
            self._client.close()

    def __enter__(self) -> "HttpTransport":
        return self

    def __exit__(self, *exc_info: Any) -> None:
        self.close()


class AsyncHttpTransport:
    """Async httpx transport wrapper with simple retry on 5xx."""

    def __init__(
        self,
        *,
        base_url: str = DEFAULT_BASE_URL,
        api_version: str = DEFAULT_API_VERSION,
        lang: Optional[str] = None,
        timeout: float = DEFAULT_TIMEOUT,
        headers: Optional[Mapping[str, str]] = None,
        client: Optional[httpx.AsyncClient] = None,
        max_retries: int = 2,
        retry_backoff: float = 0.5,
    ) -> None:
        merged_headers = _build_default_headers(api_version, lang)
        if headers:
            merged_headers.update(headers)
        self._owns_client = client is None
        self._client = client or httpx.AsyncClient(
            base_url=base_url, headers=merged_headers, timeout=timeout
        )
        self.max_retries = max_retries
        self.retry_backoff = retry_backoff

    async def _request(
        self, path: str, *, params: Optional[Mapping[str, Any]] = None
    ) -> httpx.Response:
        import asyncio

        last_exc: Optional[Exception] = None
        for attempt in range(self.max_retries + 1):
            try:
                response = await self._client.get(path, params=_clean_params(params))
            except httpx.TransportError as exc:
                last_exc = exc
                if attempt >= self.max_retries:
                    raise
                await asyncio.sleep(self.retry_backoff * (2**attempt))
                continue
            if response.status_code >= 500 and attempt < self.max_retries:
                await asyncio.sleep(self.retry_backoff * (2**attempt))
                continue
            _raise_for_status(response)
            return response
        if last_exc is not None:  # pragma: no cover - defensive
            raise last_exc
        raise RuntimeError("unreachable")

    async def get(self, path: str, *, params: Optional[Mapping[str, Any]] = None) -> Any:
        return _decode_payload(await self._request(path, params=params))

    async def get_bytes(
        self, path: str, *, params: Optional[Mapping[str, Any]] = None
    ) -> bytes:
        return (await self._request(path, params=params)).content

    async def aclose(self) -> None:
        if self._owns_client:
            await self._client.aclose()

    async def __aenter__(self) -> "AsyncHttpTransport":
        return self

    async def __aexit__(self, *exc_info: Any) -> None:
        await self.aclose()
