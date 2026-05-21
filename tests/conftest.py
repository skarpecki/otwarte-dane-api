"""Shared pytest fixtures."""

from __future__ import annotations

import pytest

from otwarte_dane_api import AsyncOtwarteDaneClient, OtwarteDaneClient
from otwarte_dane_api._http import DEFAULT_BASE_URL

BASE_URL = DEFAULT_BASE_URL.rstrip("/")


@pytest.fixture
def client():
    c = OtwarteDaneClient()
    try:
        yield c
    finally:
        c.close()


@pytest.fixture
async def async_client():
    c = AsyncOtwarteDaneClient()
    try:
        yield c
    finally:
        await c.aclose()


@pytest.fixture
def base_url() -> str:
    return BASE_URL


def envelope(data, *, meta=None, links=None, count=None):
    """Build a JSON:API style envelope used by the API."""
    body = {"jsonapi": "1.0", "data": data}
    m = dict(meta or {})
    if count is not None:
        m.setdefault("count", count)
    if m:
        body["meta"] = m
    if links is not None:
        body["links"] = links
    return body
