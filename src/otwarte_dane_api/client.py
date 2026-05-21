"""High-level sync / async clients."""

from __future__ import annotations

from typing import Any, Mapping, Optional

from ._http import (
    DEFAULT_API_VERSION,
    DEFAULT_BASE_URL,
    DEFAULT_TIMEOUT,
    AsyncHttpTransport,
    HttpTransport,
)
from .resources import (
    AsyncDatasetsResource,
    AsyncDgaResource,
    AsyncHistoriesResource,
    AsyncInstitutionsResource,
    AsyncReportsResource,
    AsyncResourcesResource,
    AsyncSearchResource,
    AsyncShowcasesResource,
    DatasetsResource,
    DgaResource,
    HistoriesResource,
    InstitutionsResource,
    ReportsResource,
    ResourcesResource,
    SearchResource,
    ShowcasesResource,
)


class OtwarteDaneClient:
    """Synchronous client for the DANE.GOV.PL Open Data API."""

    def __init__(
        self,
        *,
        base_url: str = DEFAULT_BASE_URL,
        api_version: str = DEFAULT_API_VERSION,
        lang: Optional[str] = None,
        timeout: float = DEFAULT_TIMEOUT,
        headers: Optional[Mapping[str, str]] = None,
        transport: Optional[HttpTransport] = None,
    ) -> None:
        self._http = transport or HttpTransport(
            base_url=base_url,
            api_version=api_version,
            lang=lang,
            timeout=timeout,
            headers=headers,
        )
        self.institutions = InstitutionsResource(self._http)
        self.datasets = DatasetsResource(self._http)
        self.resources = ResourcesResource(self._http)
        self.showcases = ShowcasesResource(self._http)
        self.histories = HistoriesResource(self._http)
        self.search = SearchResource(self._http)
        self.dga = DgaResource(self._http)
        self.reports = ReportsResource(self._http)

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> "OtwarteDaneClient":
        return self

    def __exit__(self, *exc_info: Any) -> None:
        self.close()


class AsyncOtwarteDaneClient:
    """Asynchronous client for the DANE.GOV.PL Open Data API."""

    def __init__(
        self,
        *,
        base_url: str = DEFAULT_BASE_URL,
        api_version: str = DEFAULT_API_VERSION,
        lang: Optional[str] = None,
        timeout: float = DEFAULT_TIMEOUT,
        headers: Optional[Mapping[str, str]] = None,
        transport: Optional[AsyncHttpTransport] = None,
    ) -> None:
        self._http = transport or AsyncHttpTransport(
            base_url=base_url,
            api_version=api_version,
            lang=lang,
            timeout=timeout,
            headers=headers,
        )
        self.institutions = AsyncInstitutionsResource(self._http)
        self.datasets = AsyncDatasetsResource(self._http)
        self.resources = AsyncResourcesResource(self._http)
        self.showcases = AsyncShowcasesResource(self._http)
        self.histories = AsyncHistoriesResource(self._http)
        self.search = AsyncSearchResource(self._http)
        self.dga = AsyncDgaResource(self._http)
        self.reports = AsyncReportsResource(self._http)

    async def aclose(self) -> None:
        await self._http.aclose()

    async def __aenter__(self) -> "AsyncOtwarteDaneClient":
        return self

    async def __aexit__(self, *exc_info: Any) -> None:
        await self.aclose()
