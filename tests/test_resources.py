from __future__ import annotations

import httpx
import pytest
import respx

from otwarte_dane_api.models.resource import DataResource, TableRow


def envelope(data, *, meta=None, links=None, count=None):
    body = {"jsonapi": "1.0", "data": data}
    merged_meta = dict(meta or {})
    if count is not None:
        merged_meta.setdefault("count", count)
    if merged_meta:
        body["meta"] = merged_meta
    if links is not None:
        body["links"] = links
    return body


RESOURCE_ATTRIBUTES = {
    "title": "Population by region",
    "description": "Resource description",
    "format": "csv",
    "file_url": "https://files.example.test/resource.csv",
    "download_url": "https://files.example.test/resource.csv?download=1",
    "link": "https://example.test/resources/7",
    "csv_file_url": "https://files.example.test/resource-normalized.csv",
    "jsonld_file_url": "https://files.example.test/resource.jsonld",
    "openness_score": 5,
    "views_count": 12,
    "downloads_count": 34,
    "data_date": "2024-01-01",
    "file_size": 2048,
    "has_chart": True,
    "has_map": False,
    "has_table": True,
    "has_dynamic_data": True,
    "has_high_value_data": True,
    "has_research_data": False,
    "is_chart_creation_blocked": False,
    "license_code": "cc-by-4.0",
    "license_name": "CC BY 4.0",
    "modified": "2024-01-02T00:00:00Z",
    "created": "2024-01-01T00:00:00Z",
    "verified": "2024-01-03T00:00:00Z",
    "type": "file",
    "language": "pl",
    "regions": [{"name": "Mazowieckie"}],
    "supplements": [{"title": "Data dictionary", "format": "pdf"}],
    "special_signs": [{"name": "high_value"}],
}


def test_list_resources_returns_typed_attributes(client, base_url):
    payload = envelope(
        [
            {
                "id": "7",
                "type": "resource",
                "attributes": RESOURCE_ATTRIBUTES,
            }
        ],
        count=1,
    )

    with respx.mock(assert_all_called=True) as router:
        route = router.get(f"{base_url}/resources").mock(
            return_value=httpx.Response(200, json=payload)
        )

        result = client.resources.list(page=1, per_page=10)

    assert route.called
    assert len(result.items) == 1
    assert isinstance(result[0], DataResource)
    assert result[0].title == "Population by region"
    assert result[0].type == "resource"
    assert result[0].attribute_type == "file"
    assert result[0].downloads_count == 34
    assert result[0].regions[0].name == "Mazowieckie"
    assert result[0].supplements[0].title == "Data dictionary"
    assert result[0].special_signs[0].name == "high_value"
    assert result.meta is not None
    assert result.meta.count == 1
    assert result.total == 1


def test_get_resource_by_id(client, base_url):
    payload = envelope(
        {
            "id": "7",
            "type": "resource",
            "attributes": RESOURCE_ATTRIBUTES,
        }
    )

    with respx.mock(assert_all_called=True) as router:
        router.get(f"{base_url}/resources/7").mock(
            return_value=httpx.Response(200, json=payload)
        )

        result = client.resources.get(7)

    assert isinstance(result, DataResource)
    assert result.id == "7"
    assert result.format == "csv"


def test_get_resource_data_rows(client, base_url):
    payload = envelope(
        [
            {
                "id": "3",
                "type": "row",
                "attributes": {"city": "Warsaw", "population": 10},
            },
            {
                "id": "4",
                "type": "row",
                "attributes": {"city": "Krakow", "population": 20},
            },
        ],
        meta={
            "count": 2,
            "headers_map": {"city": "City", "population": "Population"},
            "data_schema": {"city": "string", "population": "integer"},
        },
    )

    with respx.mock(assert_all_called=True) as router:
        route = router.get(
            f"{base_url}/resources/7/data",
            params={"page": "1", "per_page": "10"},
        ).mock(return_value=httpx.Response(200, json=payload))

        result = client.resources.get_data(7, page=1, per_page=10)

    assert route.called
    rows = list(result)
    assert len(rows) == 2
    assert isinstance(rows[0], TableRow)
    assert rows[0].city == "Warsaw"
    assert rows[1].population == 20
    assert result.meta is not None
    assert result.meta.count == 2


def test_get_resource_data_row(client, base_url):
    payload = envelope(
        {
            "id": "3",
            "type": "row",
            "attributes": {"city": "Warsaw", "population": 10},
        }
    )

    with respx.mock(assert_all_called=True) as router:
        router.get(f"{base_url}/resources/7/data/3").mock(
            return_value=httpx.Response(200, json=payload)
        )

        result = client.resources.get_row(7, 3)

    assert isinstance(result, TableRow)
    assert result.id == "3"
    assert result.population == 10


@respx.mock
def test_paginator_next_page_for_data(client, base_url):
    respx.get(f"{base_url}/resources/7/data", params={"page": "1"}).mock(
        return_value=httpx.Response(
            200,
            json=envelope(
                [
                    {"id": "3", "type": "row", "attributes": {"city": "Warsaw", "population": 10}},
                ],
                count=2,
                links={
                    "self": f"{base_url}/resources/7/data?page=1",
                    "next": f"{base_url}/resources/7/data?page=2",
                },
            ),
        )
    )
    respx.get(f"{base_url}/resources/7/data", params={"page": "2"}).mock(
        return_value=httpx.Response(
            200,
            json=envelope(
                [
                    {"id": "4", "type": "row", "attributes": {"city": "Krakow", "population": 20}},
                ],
                count=2,
                links={"self": f"{base_url}/resources/7/data?page=2"},
            ),
        )
    )

    page = client.resources.get_data(7, page=1)
    ids = [row.id for row in page]
    assert page.next_page() is True
    ids.extend(row.id for row in page)

    assert ids == ["3", "4"]


@pytest.mark.asyncio
async def test_async_list_resources_smoke(async_client, base_url):
    payload = envelope(
        [
            {
                "id": "7",
                "type": "resource",
                "attributes": RESOURCE_ATTRIBUTES,
            }
        ],
        count=1,
    )

    with respx.mock(assert_all_called=True) as router:
        router.get(f"{base_url}/resources").mock(
            return_value=httpx.Response(200, json=payload)
        )

        result = await async_client.resources.list()

    assert len(result.items) == 1
    assert isinstance(result[0], DataResource)
    assert result[0].title == "Population by region"
