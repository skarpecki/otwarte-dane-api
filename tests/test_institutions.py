from __future__ import annotations

import pytest
import respx
from httpx import Response

from conftest import envelope


@respx.mock
def test_list_institutions_returns_flat_entities(client, base_url):
    route = respx.get(f"{base_url}/institutions", params={"page": "1", "per_page": "2"}).mock(
        return_value=Response(
            200,
            json=envelope(
                [
                    {"id": "1", "type": "institution", "attributes": {"title": "Foo", "slug": "foo"}},
                    {"id": "2", "type": "institution", "attributes": {"title": "Bar", "slug": "bar"}},
                ],
                count=2,
            ),
        )
    )

    page = client.institutions.list(page=1, per_page=2)

    assert route.called
    assert len(page) == 2
    assert page[0].id == "1"
    assert page[0].type == "institution"
    assert page[0].title == "Foo"
    assert page[1].title == "Bar"
    assert page.total == 2
    assert [e.title for e in page] == ["Foo", "Bar"]


@respx.mock
def test_list_institutions_passes_filters(client, base_url):
    route = respx.get(
        f"{base_url}/institutions",
        params={"q": "health", "per_page": "5", "sort": "title"},
    ).mock(return_value=Response(200, json=envelope([], count=0)))

    client.institutions.list(q="health", per_page=5, sort="title")

    assert route.called


@respx.mock
def test_get_institution_returns_flat_entity(client, base_url):
    route = respx.get(f"{base_url}/institutions/42").mock(
        return_value=Response(
            200,
            json=envelope({"id": "42", "type": "institution", "attributes": {"title": "Answer"}}),
        )
    )

    inst = client.institutions.get(42)

    assert route.called
    assert inst.id == "42"
    assert inst.type == "institution"
    assert inst.title == "Answer"


@respx.mock
def test_list_datasets_for_institution_returns_typed_entities(client, base_url):
    route = respx.get(f"{base_url}/institutions/42/datasets").mock(
        return_value=Response(
            200,
            json=envelope(
                [{"id": "10", "type": "dataset", "attributes": {"title": "Dataset 1"}}],
                count=1,
            ),
        )
    )

    page = client.institutions.list_datasets(42)

    assert route.called
    assert len(page) == 1
    assert page[0].id == "10"
    assert page[0].type == "dataset"
    assert page[0].title == "Dataset 1"


@respx.mock
def test_get_raw_returns_full_document(client, base_url):
    respx.get(f"{base_url}/institutions/7").mock(
        return_value=Response(
            200,
            json=envelope({"id": "7", "type": "institution", "attributes": {"title": "Raw"}}),
        )
    )

    doc = client.institutions.get_raw(7)

    assert doc.data is not None
    assert doc.data.id == "7"
    assert doc.data.attributes is not None
    assert doc.data.attributes.title == "Raw"


@respx.mock
def test_next_page_walks_pages_manually(client, base_url):
    respx.get(f"{base_url}/institutions", params={"page": "1", "per_page": "2"}).mock(
        return_value=Response(
            200,
            json=envelope(
                [
                    {"id": "1", "type": "institution", "attributes": {"title": "A"}},
                    {"id": "2", "type": "institution", "attributes": {"title": "B"}},
                ],
                count=4,
                links={"next": "https://api.dane.gov.pl/institutions?page=2&per_page=2"},
            ),
        )
    )
    respx.get(f"{base_url}/institutions", params={"page": "2", "per_page": "2"}).mock(
        return_value=Response(
            200,
            json=envelope(
                [
                    {"id": "3", "type": "institution", "attributes": {"title": "C"}},
                    {"id": "4", "type": "institution", "attributes": {"title": "D"}},
                ],
                count=4,
            ),
        )
    )

    page = client.institutions.list(page=1, per_page=2)
    titles = [e.title for e in page]
    assert page.next_page() is True
    titles.extend(e.title for e in page)
    assert titles == ["A", "B", "C", "D"]


@respx.mock
@pytest.mark.asyncio
async def test_async_list_and_get(async_client, base_url):
    respx.get(f"{base_url}/institutions", params={"page": "1", "per_page": "2"}).mock(
        return_value=Response(
            200,
            json=envelope(
                [
                    {"id": "1", "type": "institution", "attributes": {"title": "Foo"}},
                    {"id": "2", "type": "institution", "attributes": {"title": "Bar"}},
                ],
                count=2,
            ),
        )
    )
    respx.get(f"{base_url}/institutions/9").mock(
        return_value=Response(
            200,
            json=envelope({"id": "9", "type": "institution", "attributes": {"title": "Nine"}}),
        )
    )

    page = await async_client.institutions.list(page=1, per_page=2)
    assert [e.title for e in page] == ["Foo", "Bar"]
    assert page.total == 2

    inst = await async_client.institutions.get(9)
    assert inst.id == "9"
    assert inst.title == "Nine"
