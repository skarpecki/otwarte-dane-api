# otwarte-dane-api

A typed, batteries-included Python client for the [DANE.GOV.PL Open Data API](https://api.dane.gov.pl/doc) (OpenAPI 1.4) — the Polish government's open-data portal.

Built on `httpx` + `pydantic v2`. Sync **and** async clients, full type hints, JSON:API envelope decoded into generic `Document[Resource[Model]]` models, automatic retry on 5xx, and zero authentication required for read-only endpoints.

---

## Table of contents
- [Install](#install)
- [Build a wheel](#build-a-wheel)
- [Quickstart](#quickstart)
- [Async usage](#async-usage)
- [Configuration](#configuration)
- [Response model](#response-model)
- [Pagination](#pagination)
- [Error handling](#error-handling)
- [Resource namespaces](#resource-namespaces)
  - [`client.institutions`](#clientinstitutions)
  - [`client.datasets`](#clientdatasets)
  - [`client.resources`](#clientresources)
  - [`client.showcases`](#clientshowcases)
  - [`client.histories`](#clienthistories)
  - [`client.search`](#clientsearch)
  - [`client.dga`](#clientdga)
  - [`client.reports`](#clientreports)
- [Tests](#tests)
- [License](#license)

---

## Install

```bash
pip install otwarte-dane-api          # once published
# or, from a local checkout:
pip install -e ".[dev]"
```

Requires Python 3.9+.

## Build a wheel

```bash
pip install build
python -m build --wheel --sdist
# -> dist/otwarte_dane_api-0.1.0-py3-none-any.whl
# -> dist/otwarte_dane_api-0.1.0.tar.gz
```

## Quickstart

```python
from otwarte_dane_api import OtwarteDaneClient

with OtwarteDaneClient() as client:
    # `get` returns a flat entity — id, type and all attributes on one object
    ds = client.datasets.get(123)
    print(ds.id, ds.title, ds.views_count)

    # `list` returns one page: iterable, has .total / .meta / .links.
    page = client.datasets.list(per_page=5, sort="-views_count")
    print("total datasets:", page.total)
    for ds in page:
        print(ds.id, ds.title, ds.views_count)
```

## Async usage

```python
import asyncio
from otwarte_dane_api import AsyncOtwarteDaneClient

async def main():
    async with AsyncOtwarteDaneClient(lang="pl") as client:
        page = await client.institutions.list(per_page=10)
        print(page.total, "institutions total")
        for inst in page:
            print(inst.id, inst.title)

asyncio.run(main())
```

## Configuration

Both `OtwarteDaneClient` and `AsyncOtwarteDaneClient` accept:

| Argument | Default | Purpose |
|---|---|---|
| `base_url` | `https://api.dane.gov.pl/` | Override for staging / mocks. |
| `api_version` | `"1.4"` | Sent as `X-API-VERSION` header. |
| `lang` | `None` | Default `Accept-Language` (e.g. `"pl"`, `"en"`). Can be overridden per call. |
| `timeout` | `30.0` | Per-request timeout in seconds. |
| `headers` | `None` | Extra headers merged into every request. |
| `transport` | `None` | Pre-built `HttpTransport` / `AsyncHttpTransport` (advanced). |

Example with custom config:

```python
client = OtwarteDaneClient(
    lang="en",
    timeout=15.0,
    headers={"User-Agent": "my-research-bot/1.0"},
)
```

## Response model

Each `list()` returns a **`Paginator[Entity]`**; each `get()` returns a flat **`Entity`** (a pydantic model whose fields include the JSON:API `id`, `type`, and all attributes merged into one object).

### Paginator
```python
page = client.datasets.list(per_page=5)

# current-page entities
page.items             # preferred: list[Dataset]
page.data              # backward-compatible alias for page.items
len(page)              # item count on current page
page[0]                # first entity (flat)
for ds in page: ...    # iterate current page

# envelope metadata, preserved
page.total             # int | None — value of meta.count
page.meta              # Meta (server_time, aggregations, ...)
page.links             # Links (next, prev, first, last, self)
page.next_page_url     # str | None — same value as page.links.next
page.page_number       # current page index
page.has_next()        # bool

# manually advance
page.next_page()      # in-place advance, returns False at end

# escape hatch
page.raw               # the underlying Document (full JSON:API envelope)
```

### Flat entities
Each entity is a pydantic model with `id`, `type`, and the typed attribute fields all flattened onto it:

```python
ds = client.datasets.get(123)
ds.id              # "123"
ds.type            # "dataset"
ds.title           # str
ds.views_count     # int | None
ds.model_dump()    # plain dict
```

`extra="allow"` is set, so unknown fields from newer API versions are still accessible via attribute or `.model_extra`.

### Escape hatch: full JSON:API envelope
Need `meta.aggregations`, `included` sideloads, resource-level `links`, or `relationships`? Every method has a `_raw` sibling that returns the unflattened `Document[Resource[Model]]`:

```python
doc = client.datasets.get_raw(123)
doc.data.id
doc.data.attributes.title
doc.data.links.self_
doc.data.relationships
doc.meta.aggregations

page = client.datasets.list_raw(per_page=5)
page.data           # list[Resource[Dataset]]
page.meta.aggregations
```

Flattened entities returned by regular methods include only the JSON:API `id`, `type`, and API `attributes`. JSON:API resource metadata such as item-level `links` and `relationships` stays on the raw envelope.

The `Document`, `Resource`, `Meta`, `Links`, `Relationship` models live in `otwarte_dane_api.models`.
Public entity models use domain names such as `Dataset`, `Institution`, `DataResource`, `Showcase`, `HistoryEntry`, `TableRow`, `BrokenLinkReport`, and `BrokenLinkEntry`. The older `*Attributes` names remain compatibility aliases.

## Pagination

Every `list()` returns a single page. Drive additional pages manually with `next_page()` so API calls remain explicit and predictable:

```python
with OtwarteDaneClient() as client:
    page = client.datasets.list(per_page=100)
    while True:
        for ds in page:
            print(ds.title)
        if not page.next_page():
            break
```

Async equivalent:

```python
page = await client.datasets.list(per_page=100)
while True:
    async for ds in page:
        print(ds.title)
    if not await page.next_page():
        break
```

## Error handling

Non-2xx responses raise a subclass of `ApiError`:

```python
from otwarte_dane_api import (
    OtwarteDaneClient,
    ApiError, BadRequestError, NotFoundError,
    AuthenticationError, RateLimitError, ServerError,
)

with OtwarteDaneClient() as client:
    try:
        client.datasets.get(99_999_999)
    except NotFoundError as exc:
        print("missing:", exc.status_code, exc.url)
    except RateLimitError:
        print("slow down...")
    except ApiError as exc:
        print("api error:", exc.status_code, exc.payload)
```

The transport auto-retries up to 2 times on 5xx responses with exponential back-off (0.5s, 1.0s).

---

## Resource namespaces

The client exposes 8 namespaces, mirroring the API:

### `client.institutions`

```python
# List with filtering / sorting — Paginator of flat Institution
page = client.institutions.list(
    per_page=20,
    sort="title",
    q="ministerstwo",   # full-text query
)
for inst in page:
    print(inst.id, inst.title, inst.city)

# Single institution — flat Institution
inst = client.institutions.get(1)
print(inst.regon, inst.website)

# Datasets owned by an institution — Paginator of flat Dataset
datasets = client.institutions.list_datasets(1, per_page=50)
for ds in datasets:
    print(ds.id, ds.title)
```

### `client.datasets`

```python
# List with filters: q, sort, per_page, page, institution[id], category[id], ...
page = client.datasets.list(
    q="budżet",
    sort="-modified",
    per_page=10,
    **{"institution[id]": 1},
)
for ds in page:
    print(ds.id, ds.title, ds.modified)

# Single dataset
ds = client.datasets.get(123)
print(ds.title, ds.license_name)

# Resources (files) attached to a dataset — Paginator of flat DataResource
files = client.datasets.list_resources(123, per_page=50)
for f in files:
    print(f.id, f.format, f.file_url)

# Showcases (apps/visualisations) that use a dataset — Paginator of flat Showcase
apps = client.datasets.list_showcases(123)
for s in apps:
    print(s.id, s.title)
```

### `client.resources`

`resources` here means individual *data files* attached to datasets (CSV, JSON, XLSX, etc.).

```python
# List resource files
page = client.resources.list(per_page=10, sort="-data_date")
for r in page:
    print(r.id, r.format, r.file_url)

# Single resource metadata — flat
res = client.resources.get(456)
print(res.format, res.file_url, res.openness_score)
# `res.type` is the JSON:API discriminator; if the API also sends an
# attributes.type value, it is preserved as `res.attribute_type`.

# Tabular data — Paginator over flat TableRow
rows = client.resources.get_data(456, per_page=100)
for row in rows:
    print(row.id, row.model_dump())

# A single row by ID — flat
row = client.resources.get_row(456, 1)
print(row.id, row.model_dump())
```

### `client.showcases`

```python
page = client.showcases.list(per_page=5, sort="-views_count", q="mapa")
for sc in page:
    print(sc.id, sc.title, sc.url)

sc = client.showcases.get(7)
print(sc.notes, sc.author)
```

### `client.histories`

Change-log entries describing edits to portal data.

```python
page = client.histories.list(per_page=25, sort="-change_timestamp")
for h in page:
    print(h.change_timestamp, h.action, h.table_name)

entry = client.histories.get(99)
print(entry.difference)
```

### `client.search`

Cross-resource full-text search returning heterogeneous results. Each hit is a typed `SearchResult` carrying `id`, `type`, and that entity's attributes merged together. Attribute access is preferred, while dict-style access remains available for compatibility.

```python
# Search across all entity types
page = client.search.query("powietrze", per_page=20)
for hit in page:
    print(hit.type, hit.id, hit.title)

# Restrict to specific models
page = client.search.query(
    "powietrze",
    models=["dataset", "resource"],
    sort="-score",
)
```

Use `hit.type` to dispatch and access entity-specific fields directly. For example, `hit.as_dataset()` re-validates a dataset hit as `Dataset`.

### `client.dga`

Aggregated statistics related to the EU Data Governance Act.

```python
info = client.dga.get_aggregated(lang="pl")
print(info.model_dump())

# Raw server response (untouched dict) — escape hatch
raw = client.dga.get_aggregated_raw(lang="pl")
```

### `client.reports`

Broken-links portal report.

```python
# Report metadata — flat
report = client.reports.get_broken_links_report()
print(report.title, report.file_url)

# Paginator of flat BrokenLinkEntry
page = client.reports.list_broken_links(per_page=100)
for entry in page:
    print(entry.model_dump())

# Download the report file in a given format (csv, tsv, xlsx, ...)
csv_bytes = client.reports.download_broken_links("csv")
with open("brokenlinks.csv", "wb") as f:
    f.write(csv_bytes)
```

---

## End-to-end example: dump every dataset of an institution as CSV

```python
import csv
from otwarte_dane_api import OtwarteDaneClient

INSTITUTION_ID = 1

with OtwarteDaneClient(lang="pl") as client, open("out.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["id", "title", "modified", "views_count"])

    page = client.datasets.list(per_page=100, **{"institution[id]": INSTITUTION_ID})
    while True:
        for ds in page:
            writer.writerow([ds.id, ds.title, ds.modified, ds.views_count])
        if not page.next_page():
            break
```

## Tests

```bash
.\.venv\Scripts\python.exe -m pytest        # all respx-mocked, no network
.\.venv\Scripts\python.exe -m ruff check src tests
```

The test suite uses `respx` to mock httpx, so it runs offline and does not hit the real API.

## License

MIT.
