from __future__ import annotations

import pytest
import respx
from httpx import Response

from otwarte_dane_api.models.showcase import Showcase
from tests.conftest import envelope


def make_showcase(showcase_id: str = "447") -> dict:
    return {
        "id": showcase_id,
        "type": "showcase",
        "attributes": {
            "title": "Example showcase",
            "notes": "Example notes",
            "slug": "example-showcase",
            "url": "https://example.com/showcase",
            "image_url": "https://example.com/image.png",
            "image_thumb_url": "https://example.com/thumb.png",
            "license_type": "CC-BY-4.0",
            "license_logo_url": "https://example.com/license.svg",
            "main_page_position": 3,
            "modified": "2024-01-02T03:04:05Z",
            "created": "2024-01-01T00:00:00Z",
            "views_count": 42,
            "illustrative_graphics_url": "https://example.com/graphic.png",
            "illustrative_graphics_alt": "Graphic alt",
            "has_chart": True,
            "has_map": False,
            "has_table": True,
            "has_image": True,
            "author": "Jane Doe",
            "category": "Transport",
            "image_alt": "Image alt",
            "tags": ["tag-1", "tag-2"],
            "keywords": ["keyword-1", "keyword-2"],
            "external_datasets": [
                {"url": "https://example.com/dataset", "title": "Dataset"}
            ],
        },
        "links": {"self": f"https://api.dane.gov.pl/showcases/{showcase_id}"},
    }


@respx.mock
def test_list_showcases_returns_typed(client, base_url):
    route = respx.get(f"{base_url}/showcases").mock(
        return_value=Response(200, json=envelope([make_showcase()], count=1))
    )

    result = client.showcases.list()

    assert route.called
    assert result.meta is not None
    assert result.meta.count == 1
    assert len(result.items) == 1
    assert isinstance(result[0], Showcase)
    assert result[0].title == "Example showcase"
    assert result[0].external_datasets[0].title == "Dataset"


@respx.mock
def test_paginator_next_page_for_showcases(client, base_url):
    route = respx.get(f"{base_url}/showcases")
    route.side_effect = [
        Response(
            200,
            json=envelope(
                [make_showcase("447")],
                count=2,
                links={
                    "next": f"{base_url}/showcases?page=2",
                    "self": f"{base_url}/showcases?page=1",
                },
            ),
        ),
        Response(
            200,
            json=envelope(
                [make_showcase("448")],
                count=2,
                links={"self": f"{base_url}/showcases?page=2"},
            ),
        ),
    ]

    result = client.showcases.list(page=1)
    ids = [item.id for item in result]
    assert result.next_page() is True
    ids.extend(item.id for item in result)

    assert ids == ["447", "448"]
    assert route.call_count == 2


@respx.mock
def test_list_showcases_passes_filters(client, base_url):
    route = respx.get(f"{base_url}/showcases").mock(
        return_value=Response(200, json=envelope([], count=0))
    )

    client.showcases.list(q="tram", per_page=5, sort="-modified")

    assert route.called
    request = route.calls.last.request
    assert request.url.params.get("q") == "tram"
    assert request.url.params.get("per_page") == "5"
    assert request.url.params.get("sort") == "-modified"


@respx.mock
def test_get_showcase_by_id(client, base_url):
    route = respx.get(f"{base_url}/showcases/447").mock(
        return_value=Response(200, json=envelope(make_showcase("447")))
    )

    result = client.showcases.get(447)

    assert route.called
    assert result.id == "447"
    assert result.slug == "example-showcase"


@respx.mock
@pytest.mark.asyncio
async def test_async_list_showcases_smoke(async_client, base_url):
    route = respx.get(f"{base_url}/showcases").mock(
        return_value=Response(200, json=envelope([make_showcase()], count=1))
    )

    result = await async_client.showcases.list(lang="en")

    assert route.called
    assert route.calls.last.request.url.params.get("lang") == "en"
    assert result.items[0].title == "Example showcase"
