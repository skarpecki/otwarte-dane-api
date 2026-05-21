from __future__ import annotations

import pytest
import respx
from httpx import Response

from conftest import envelope
from otwarte_dane_api.models.history import HistoryEntry


@respx.mock
def test_list_histories_returns_flat_entities(client, base_url):
    route = respx.get(
        f"{base_url}/histories", params={"page": "1", "per_page": "2"}
    ).mock(
        return_value=Response(
            200,
            json=envelope(
                [
                    {
                        "id": "1",
                        "type": "history",
                        "attributes": {
                            "action": "create",
                            "table_name": "dataset",
                            "message": "Created dataset",
                            "change_user_id": "7",
                            "row_id": 11,
                            "change_timestamp": "2024-01-02T03:04:05Z",
                            "difference": {"title": [None, "Dataset"]},
                        },
                    },
                    {
                        "id": "2",
                        "type": "history",
                        "attributes": {
                            "action": "update",
                            "table_name": "resource",
                        },
                    },
                ],
                count=2,
            ),
        )
    )

    result = client.histories.list(page=1, per_page=2)

    assert route.called
    assert len(result) == 2
    assert isinstance(result[0], HistoryEntry)
    assert result[0].id == "1"
    assert result[0].action == "create"
    assert result[0].difference == {"title": [None, "Dataset"]}
    assert result.total == 2
    assert [entry.action for entry in result] == ["create", "update"]


@respx.mock
def test_paginator_next_page_for_histories(client, base_url):
    route = respx.get(f"{base_url}/histories")
    route.side_effect = [
        Response(
            200,
            json=envelope(
                [
                    {
                        "id": "1",
                        "type": "history",
                        "attributes": {"action": "create"},
                    }
                ],
                count=2,
                links={
                    "next": f"{base_url}/histories?page=2",
                    "self": f"{base_url}/histories?page=1",
                },
            ),
        ),
        Response(
            200,
            json=envelope(
                [
                    {
                        "id": "2",
                        "type": "history",
                        "attributes": {"action": "update"},
                    }
                ],
                count=2,
                links={"self": f"{base_url}/histories?page=2"},
            ),
        ),
    ]

    result = client.histories.list(page=1)
    ids = [item.id for item in result]
    assert result.next_page() is True
    ids.extend(item.id for item in result)

    assert ids == ["1", "2"]
    assert route.call_count == 2


@respx.mock
def test_list_histories_passes_filters(client, base_url):
    route = respx.get(f"{base_url}/histories").mock(
        return_value=Response(200, json=envelope([], count=0))
    )

    client.histories.list(
        per_page=5,
        sort="-change_timestamp",
        lang="pl",
        action={"match": "create"},
        change_user_id={"term": "7"},
        row_id={"gte": "10"},
    )

    assert route.called
    params = route.calls.last.request.url.params
    assert params.get("per_page") == "5"
    assert params.get("sort") == "-change_timestamp"
    assert params.get("lang") == "pl"
    assert params.get("action") == "{'match': 'create'}"
    assert params.get("change_user_id") == "{'term': '7'}"
    assert params.get("row_id") == "{'gte': '10'}"


@respx.mock
def test_get_history_by_id(client, base_url):
    route = respx.get(f"{base_url}/histories/42").mock(
        return_value=Response(
            200,
            json=envelope(
                {
                    "id": "42",
                    "type": "history",
                    "attributes": {
                        "action": "delete",
                        "table_name": "dataset",
                        "message": "Removed dataset",
                    },
                }
            ),
        )
    )

    result = client.histories.get(42)

    assert route.called
    assert result.id == "42"
    assert result.action == "delete"
    assert result.message == "Removed dataset"


@pytest.mark.asyncio
@respx.mock
async def test_async_list_histories(async_client, base_url):
    route = respx.get(f"{base_url}/histories", params={"page": "1"}).mock(
        return_value=Response(
            200,
            json=envelope(
                [
                    {
                        "id": "1",
                        "type": "history",
                        "attributes": {"action": "create"},
                    }
                ],
                count=1,
            ),
        )
    )

    result = await async_client.histories.list(page=1)

    assert route.called
    assert len(result) == 1
    assert result[0].id == "1"
    assert result[0].action == "create"
