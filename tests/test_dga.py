from __future__ import annotations

import httpx
import pytest

from otwarte_dane_api.models import DgaAggregatedResponse


@pytest.mark.respx
def test_get_dga_aggregated_returns_data(client, base_url, respx_mock):
    route = respx_mock.get(f"{base_url}/dga-aggregated").mock(
        return_value=httpx.Response(
            200,
            json={
                "resource_slug": "dga-resource-slug",
                "dataset_id": 123,
                "resource_id": 456,
                "dataset_slug": "dga-dataset-slug",
            },
        )
    )

    result = client.dga.get_aggregated()

    assert route.called
    assert isinstance(result, DgaAggregatedResponse)
    assert result.resource_slug == "dga-resource-slug"
    assert result.dataset_id == 123
    assert result.resource_id == 456
    assert result.dataset_slug == "dga-dataset-slug"


@pytest.mark.respx
def test_get_dga_aggregated_passes_lang(client, base_url, respx_mock):
    route = respx_mock.get(f"{base_url}/dga-aggregated").mock(
        return_value=httpx.Response(
            200,
            json={
                "resource_slug": "resource",
                "dataset_id": 1,
                "resource_id": 2,
                "dataset_slug": "dataset",
            },
        )
    )

    client.dga.get_aggregated(lang="pl")

    assert route.called
    assert route.calls.last.request.url.params.get("lang") == "pl"


@pytest.mark.respx
def test_get_aggregated_raw_returns_dict(client, base_url, respx_mock):
    payload = {
        "resource_slug": "raw-resource",
        "dataset_id": 10,
        "resource_id": 20,
        "dataset_slug": "raw-dataset",
        "extra": {"nested": True},
    }
    route = respx_mock.get(f"{base_url}/dga-aggregated").mock(
        return_value=httpx.Response(200, json=payload)
    )

    result = client.dga.get_aggregated_raw()

    assert route.called
    assert isinstance(result, dict)
    assert result == payload
    assert set(result) == set(payload)


@pytest.mark.asyncio
@pytest.mark.respx
async def test_get_dga_aggregated_async_smoke(async_client, base_url, respx_mock):
    route = respx_mock.get(f"{base_url}/dga-aggregated").mock(
        return_value=httpx.Response(
            200,
            json={
                "resource_slug": "async-resource",
                "dataset_id": 11,
                "resource_id": 22,
                "dataset_slug": "async-dataset",
            },
        )
    )

    result = await async_client.dga.get_aggregated(lang="en")

    assert route.called
    assert route.calls.last.request.url.params.get("lang") == "en"
    assert result.resource_id == 22
