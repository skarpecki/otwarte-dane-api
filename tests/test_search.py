from __future__ import annotations

from urllib.parse import parse_qs, urlparse

import pytest
import respx
from httpx import Response

from otwarte_dane_api.models.dataset import Dataset
from otwarte_dane_api.models.search import SearchResult
from tests.conftest import envelope


@respx.mock

def test_search_returns_mixed_resource_types(client, base_url):
    route = respx.get(f"{base_url}/search").mock(
        return_value=Response(
            200,
            json=envelope(
                [
                    {
                        "id": "dataset-1",
                        "type": "dataset",
                        "attributes": {"title": "Dataset"},
                    },
                    {
                        "id": "resource-1",
                        "type": "resource",
                        "attributes": {"title": "Resource"},
                    },
                ]
            ),
        )
    )

    result = client.search.query("foo")

    assert route.called
    assert len(result.items) == 2
    assert isinstance(result[0], SearchResult)
    assert result[0].title == "Dataset"
    assert result[0]["type"] == "dataset"
    assert result[0]["id"] == "dataset-1"
    assert result[0]["title"] == "Dataset"
    assert result[0].get("missing") is None
    assert result[0].as_dataset().model_dump()["title"] == "Dataset"
    assert isinstance(result[0].as_dataset(), Dataset)
    assert result[1]["type"] == "resource"
    assert result[1]["id"] == "resource-1"
    assert result[1]["title"] == "Resource"


@respx.mock

def test_search_models_filter_is_joined(client, base_url):
    route = respx.get(f"{base_url}/search").mock(
        return_value=Response(200, json=envelope([]))
    )

    client.search.query("foo", models=["dataset", "resource"])

    assert route.called
    assert route.calls.last.request.url.params.get("model") == "dataset,resource"


@respx.mock

def test_search_passes_pagination_and_sort(client, base_url):
    route = respx.get(f"{base_url}/search").mock(
        return_value=Response(200, json=envelope([], meta={"count": 0}))
    )

    result = client.search.query("foo", page=2, per_page=50, sort="-date")

    params = route.calls.last.request.url.params
    assert params.get("q") == "foo"
    assert params.get("page") == "2"
    assert params.get("per_page") == "50"
    assert params.get("sort") == "-date"
    assert result.meta is not None
    assert result.meta.count == 0


@pytest.mark.asyncio
@respx.mock
async def test_async_search_query(async_client, base_url):
    route = respx.get(f"{base_url}/search").mock(
        return_value=Response(
            200,
            json=envelope([
                {"id": "news-1", "type": "news", "attributes": {"title": "News"}}
            ]),
        )
    )

    result = await async_client.search.query("foo")

    assert route.called
    assert len(result.items) == 1
    assert result.items[0]["type"] == "news"
    assert result.items[0]["id"] == "news-1"
    assert result.items[0]["title"] == "News"


@respx.mock
def test_paginator_next_page_for_search(client, base_url):
    def responder(request):
        params = parse_qs(urlparse(str(request.url)).query)
        page = params.get("page", ["1"])[0]
        if page == "1":
            return Response(
                200,
                json=envelope(
                    [{"id": "dataset-1", "type": "dataset", "attributes": {"title": "First"}}],
                    links={"next": f"{base_url}/search?page=2"},
                    meta={"count": 2},
                ),
            )
        return Response(
            200,
            json=envelope(
                [{"id": "dataset-2", "type": "dataset", "attributes": {"title": "Second"}}],
                meta={"count": 2},
            ),
        )

    route = respx.get(f"{base_url}/search").mock(side_effect=responder)

    result = client.search.query("foo")
    items = list(result)
    assert result.next_page() is True
    items.extend(result)

    assert route.call_count == 2
    assert [item["id"] for item in items] == ["dataset-1", "dataset-2"]
    assert [item["title"] for item in items] == ["First", "Second"]
