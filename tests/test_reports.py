from __future__ import annotations

import httpx
import pytest

from otwarte_dane_api import ServerError
from otwarte_dane_api.models.report import BrokenLinkEntry, BrokenLinkReport


@pytest.mark.respx(base_url="https://api.dane.gov.pl")
def test_get_broken_links_report_metadata(client, respx_mock, base_url):
    respx_mock.get("/reports/brokenlinks").mock(
        return_value=httpx.Response(
            200,
            json={
                "jsonapi": "1.0",
                "data": {
                    "id": "brokenlinks-report",
                    "type": "report",
                    "attributes": {
                        "title": "Broken links report",
                        "description": "Latest generated broken links report",
                        "file_url": "https://files.example/brokenlinks.csv",
                        "created": "2024-01-01T10:00:00Z",
                        "modified": "2024-01-02T10:00:00Z",
                        "status": "ready",
                        "rows_count": 2,
                    },
                },
                "meta": {"count": 1},
            },
        )
    )

    result = client.reports.get_broken_links_report()

    assert isinstance(result, BrokenLinkReport)
    assert result.id == "brokenlinks-report"
    assert result.title == "Broken links report"
    assert result.file_url == "https://files.example/brokenlinks.csv"


@pytest.mark.respx(base_url="https://api.dane.gov.pl")
def test_list_broken_links_entries(client, respx_mock, base_url):
    route = respx_mock.get("/reports/brokenlinks/data").mock(
        return_value=httpx.Response(
            200,
            json={
                "jsonapi": "1.0",
                "data": [
                    {
                        "id": "1",
                        "type": "broken-link-entry",
                        "attributes": {
                            "link": "https://broken.example/1",
                            "status_code": 404,
                            "resource_id": "res-1",
                            "dataset_id": "ds-1",
                            "last_checked": "2024-01-03T10:00:00Z",
                            "error_message": "Not Found",
                        },
                    },
                    {
                        "id": "2",
                        "type": "broken-link-entry",
                        "attributes": {
                            "link": "https://broken.example/2",
                            "status_code": 500,
                            "resource_id": "res-2",
                            "dataset_id": "ds-2",
                            "last_checked": "2024-01-03T11:00:00Z",
                            "error_message": "Server Error",
                        },
                    },
                ],
                "meta": {"count": 2},
                "links": {
                    "self": f"{base_url}/reports/brokenlinks/data?page=2&per_page=2&sort=link&q=broken",
                    "first": f"{base_url}/reports/brokenlinks/data?page=1&per_page=2&sort=link&q=broken",
                    "last": f"{base_url}/reports/brokenlinks/data?page=3&per_page=2&sort=link&q=broken",
                    "prev": f"{base_url}/reports/brokenlinks/data?page=1&per_page=2&sort=link&q=broken",
                    "next": f"{base_url}/reports/brokenlinks/data?page=3&per_page=2&sort=link&q=broken",
                },
            },
        )
    )

    result = client.reports.list_broken_links(page=2, per_page=2, sort="link", q="broken")

    request = route.calls.last.request
    assert request.url.params["page"] == "2"
    assert request.url.params["per_page"] == "2"
    assert request.url.params["sort"] == "link"
    assert request.url.params["q"] == "broken"
    assert result.meta.count == 2
    assert result.total == 2
    assert len(result.items) == 2
    assert isinstance(result[0], BrokenLinkEntry)
    assert result[0].link == "https://broken.example/1"
    assert result[0].status_code == 404
    assert result.links.next.endswith("page=3&per_page=2&sort=link&q=broken")


@pytest.mark.respx(base_url="https://api.dane.gov.pl")
def test_download_broken_links_returns_bytes(client, respx_mock):
    payload = b"col1,col2\nvalue1,value2\n"
    respx_mock.get("/reports/brokenlinks/csv").mock(
        return_value=httpx.Response(
            200,
            content=payload,
            headers={"Content-Type": "text/csv"},
        )
    )

    result = client.reports.download_broken_links("csv")

    assert result == payload


@pytest.mark.respx(base_url="https://api.dane.gov.pl")
def test_download_broken_links_uses_transport_retries(client, respx_mock):
    client._http.max_retries = 1
    client._http.retry_backoff = 0
    payload = b"ok\n"
    route = respx_mock.get("/reports/brokenlinks/csv").mock(
        side_effect=[
            httpx.Response(502, json={"detail": "temporary"}),
            httpx.Response(200, content=payload),
        ]
    )

    result = client.reports.download_broken_links("csv")

    assert route.call_count == 2
    assert result == payload


def test_download_broken_links_rejects_invalid_extension(client):
    with pytest.raises(ValueError):
        client.reports.download_broken_links("../csv")
    with pytest.raises(ValueError):
        client.reports.download_broken_links("..\\csv")


@pytest.mark.respx(base_url="https://api.dane.gov.pl")
def test_download_broken_links_raises_api_error(client, respx_mock):
    client._http.max_retries = 0
    respx_mock.get("/reports/brokenlinks/csv").mock(
        return_value=httpx.Response(503, json={"detail": "unavailable"})
    )

    with pytest.raises(ServerError) as exc_info:
        client.reports.download_broken_links("csv")

    assert exc_info.value.status_code == 503
    assert exc_info.value.payload == {"detail": "unavailable"}


@pytest.mark.respx(base_url="https://api.dane.gov.pl")
def test_paginator_next_page_for_broken_links(client, respx_mock, base_url):
    page_1 = {
        "jsonapi": "1.0",
        "data": [
            {
                "id": "1",
                "type": "broken-link-entry",
                "attributes": {
                    "link": "https://broken.example/1",
                    "status_code": 404,
                    "resource_id": "res-1",
                    "dataset_id": "ds-1",
                    "last_checked": "2024-01-03T10:00:00Z",
                    "error_message": "Not Found",
                },
            }
        ],
        "meta": {"count": 2},
        "links": {
            "self": f"{base_url}/reports/brokenlinks/data?page=1&per_page=1",
            "first": f"{base_url}/reports/brokenlinks/data?page=1&per_page=1",
            "last": f"{base_url}/reports/brokenlinks/data?page=2&per_page=1",
            "next": f"{base_url}/reports/brokenlinks/data?page=2&per_page=1",
        },
    }
    page_2 = {
        "jsonapi": "1.0",
        "data": [
            {
                "id": "2",
                "type": "broken-link-entry",
                "attributes": {
                    "link": "https://broken.example/2",
                    "status_code": 500,
                    "resource_id": "res-2",
                    "dataset_id": "ds-2",
                    "last_checked": "2024-01-03T11:00:00Z",
                    "error_message": "Server Error",
                },
            }
        ],
        "meta": {"count": 2},
        "links": {
            "self": f"{base_url}/reports/brokenlinks/data?page=2&per_page=1",
            "first": f"{base_url}/reports/brokenlinks/data?page=1&per_page=1",
            "last": f"{base_url}/reports/brokenlinks/data?page=2&per_page=1",
            "prev": f"{base_url}/reports/brokenlinks/data?page=1&per_page=1",
        },
    }
    respx_mock.get("/reports/brokenlinks/data", params={"page": "1", "per_page": "1"}).mock(
        return_value=httpx.Response(200, json=page_1)
    )
    respx_mock.get("/reports/brokenlinks/data", params={"page": "2", "per_page": "1"}).mock(
        return_value=httpx.Response(200, json=page_2)
    )

    result = client.reports.list_broken_links(page=1, per_page=1)
    links = [entry.link for entry in result]
    assert result.next_page() is True
    links.extend(entry.link for entry in result)

    assert links == ["https://broken.example/1", "https://broken.example/2"]


@pytest.mark.asyncio
@pytest.mark.respx(base_url="https://api.dane.gov.pl")
async def test_async_list_broken_links(async_client, respx_mock):
    respx_mock.get("/reports/brokenlinks/data").mock(
        return_value=httpx.Response(
            200,
            json={
                "jsonapi": "1.0",
                "data": [
                    {
                        "id": "1",
                        "type": "broken-link-entry",
                        "attributes": {
                            "link": "https://broken.example/1",
                            "status_code": 404,
                            "resource_id": "res-1",
                            "dataset_id": "ds-1",
                            "last_checked": "2024-01-03T10:00:00Z",
                            "error_message": "Not Found",
                        },
                    }
                ],
                "meta": {"count": 1},
            },
        )
    )

    result = await async_client.reports.list_broken_links(page=1, per_page=1)

    assert len(result.items) == 1
    assert result[0].link == "https://broken.example/1"
