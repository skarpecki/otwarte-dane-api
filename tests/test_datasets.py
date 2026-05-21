from __future__ import annotations

import pytest
import respx
from httpx import Response

from conftest import envelope


@respx.mock
def test_list_datasets_returns_typed_resources(client, base_url):
    route = respx.get(f"{base_url}/datasets", params={"page": "1", "per_page": "2"}).mock(
        return_value=Response(
            200,
            json=envelope(
                [
                    {
                        "id": "1",
                        "type": "dataset",
                        "attributes": {
                            "title": "Population",
                            "slug": "population",
                            "notes": "Population dataset",
                            "category": {"title": "Demography"},
                            "tags": [{"name": "population"}],
                            "source": {"title": "GUS", "url": "https://stat.gov.pl"},
                            "downloads_count": 10,
                            "has_dynamic_data": True,
                        },
                    },
                    {
                        "id": "2",
                        "type": "dataset",
                        "attributes": {"title": "Addresses", "slug": "addresses"},
                    },
                ],
                count=2,
            ),
        )
    )

    result = client.datasets.list(page=1, per_page=2)

    assert route.called
    assert result.items is result.data
    assert result.items[0].title == "Population"
    assert result.items[0].category.title == "Demography"
    assert result.items[0].tags[0].name == "population"
    assert result.items[0].source.title == "GUS"
    assert result.items[0].downloads_count == 10
    assert result.items[0].has_dynamic_data is True
    assert result.meta is not None
    assert result.meta.count == 2


@respx.mock
def test_list_datasets_filters_passed(client, base_url):
    route = respx.get(f"{base_url}/datasets").mock(
        return_value=Response(200, json=envelope([], count=0))
    )

    client.datasets.list(q="health", per_page=5, sort="title")

    assert route.called
    params = route.calls.last.request.url.params
    assert params.get("q") == "health"
    assert params.get("per_page") == "5"
    assert params.get("sort") == "title"


@respx.mock
def test_get_dataset_by_id(client, base_url):
    route = respx.get(f"{base_url}/datasets/42").mock(
        return_value=Response(
            200,
            json=envelope(
                {
                    "id": "42",
                    "type": "dataset",
                    "attributes": {"title": "Answer dataset", "slug": "answer-dataset"},
                }
            ),
        )
    )

    result = client.datasets.get(42)

    assert route.called
    assert result.id == "42"
    assert result.slug == "answer-dataset"


@respx.mock
def test_list_resources_for_dataset(client, base_url):
    route = respx.get(f"{base_url}/datasets/42/resources").mock(
        return_value=Response(
            200,
            json=envelope(
                [
            {
                "id": "r1",
                "type": "resource",
                "attributes": {"title": "CSV file", "format": "csv"},
                "links": {"self": f"{base_url}/resources/r1"},
            }
                ],
                count=1,
            ),
        )
    )

    result = client.datasets.list_resources(42)

    assert route.called
    assert len(result.items) == 1
    assert result.items[0].id == "r1"
    assert result.items[0].type == "resource"
    assert result.items[0].title == "CSV file"
    assert result.items[0].format == "csv"
    assert not hasattr(result.items[0], "links")

    raw = client.datasets.list_resources_raw(42)
    assert raw.data[0].links.self_ == f"{base_url}/resources/r1"


@respx.mock
def test_list_resources_next_page_follows_response_link(client, base_url):
    first = envelope(
        [
            {
                "id": "r1",
                "type": "resource",
                "attributes": {"title": "First CSV", "format": "csv"},
            }
        ],
        count=2,
        links={"next": f"{base_url}/datasets/42/resources?page=7&per_page=1"},
    )
    second = envelope(
        [
            {
                "id": "r2",
                "type": "resource",
                "attributes": {"title": "Second CSV", "format": "csv"},
            }
        ],
        count=2,
    )
    first_route = respx.get(
        f"{base_url}/datasets/42/resources", params={"page": "1", "per_page": "1"}
    ).mock(return_value=Response(200, json=first))
    second_route = respx.get(
        f"{base_url}/datasets/42/resources", params={"page": "7", "per_page": "1"}
    ).mock(return_value=Response(200, json=second))

    page = client.datasets.list_resources(42, page=1, per_page=1)

    assert first_route.called
    assert page[0].id == "r1"
    assert page.next_page_url.endswith("page=7&per_page=1")
    assert page.links.next.endswith("page=7&per_page=1")
    assert page.next_page() is True
    assert second_route.called
    assert page[0].id == "r2"


@respx.mock
def test_list_showcases_for_dataset(client, base_url):
    route = respx.get(f"{base_url}/datasets/42/showcases").mock(
        return_value=Response(
            200,
            json=envelope(
                [
                    {
                        "id": "s1",
                        "type": "showcase",
                        "attributes": {"title": "Map showcase"},
                    }
                ],
                count=1,
            ),
        )
    )

    result = client.datasets.list_showcases(42)

    assert route.called
    assert len(result.items) == 1
    assert result.items[0].id == "s1"
    assert result.items[0].type == "showcase"
    assert result.items[0].title == "Map showcase"


@respx.mock
def test_paginator_iteration_and_total(client, base_url):
    respx.get(f"{base_url}/datasets").mock(
        return_value=Response(
            200,
            json=envelope(
                [
                    {
                        "id": "1",
                        "type": "dataset",
                        "attributes": {"title": "Population", "slug": "population"},
                    },
                    {
                        "id": "2",
                        "type": "dataset",
                        "attributes": {"title": "Addresses", "slug": "addresses"},
                    },
                ],
                count=2,
            ),
        )
    )

    page = client.datasets.list()

    assert [ds.title for ds in page] == ["Population", "Addresses"]
    assert page.total == 2


@respx.mock
def test_paginator_next_page_manual(client, base_url):
    route = respx.get(f"{base_url}/datasets").mock(
        side_effect=[
            Response(
                200,
                json=envelope(
                    [
                        {
                            "id": "1",
                            "type": "dataset",
                            "attributes": {"title": "Population", "slug": "population"},
                        }
                    ],
                    count=2,
                    links={"next": f"{base_url}/datasets?page=2"},
                ),
            ),
            Response(
                200,
                json=envelope(
                    [
                        {
                            "id": "2",
                            "type": "dataset",
                            "attributes": {"title": "Addresses", "slug": "addresses"},
                        }
                    ],
                    count=2,
                ),
            ),
        ]
    )

    page = client.datasets.list(page=1)
    ids = [ds.id for ds in page]
    assert page.next_page() is True
    ids.extend(ds.id for ds in page)

    assert ids == ["1", "2"]
    assert route.call_count == 2


@pytest.mark.asyncio
@respx.mock
async def test_async_list_datasets(async_client, base_url):
    route = respx.get(f"{base_url}/datasets", params={"page": "1", "per_page": "2"}).mock(
        return_value=Response(
            200,
            json=envelope(
                [
                    {
                        "id": "1",
                        "type": "dataset",
                        "attributes": {"title": "Async dataset", "slug": "async-dataset"},
                    }
                ],
                count=1,
            ),
        )
    )

    result = await async_client.datasets.list(page=1, per_page=2)

    assert route.called
    assert len(result.items) == 1
    assert result.items[0].title == "Async dataset"
