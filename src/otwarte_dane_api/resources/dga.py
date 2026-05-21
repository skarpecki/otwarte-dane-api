"""DGA aggregated info resource namespace."""

from __future__ import annotations

from typing import Any

from ..models.dga import DgaAggregatedResponse
from ._base import _AsyncResource, _SyncResource, _path


class DgaResource(_SyncResource):
    def get_aggregated_raw(self, *, lang: str | None = None, **filters: Any) -> dict[str, Any]:
        params = {"lang": lang, **filters}
        return self._http.get(_path("dga-aggregated"), params=params)

    def get_aggregated(
        self, *, lang: str | None = None, **filters: Any
    ) -> DgaAggregatedResponse:
        payload = self.get_aggregated_raw(lang=lang, **filters)
        return DgaAggregatedResponse.model_validate(payload)


class AsyncDgaResource(_AsyncResource):
    async def get_aggregated_raw(
        self, *, lang: str | None = None, **filters: Any
    ) -> dict[str, Any]:
        params = {"lang": lang, **filters}
        return await self._http.get(_path("dga-aggregated"), params=params)

    async def get_aggregated(
        self, *, lang: str | None = None, **filters: Any
    ) -> DgaAggregatedResponse:
        payload = await self.get_aggregated_raw(lang=lang, **filters)
        return DgaAggregatedResponse.model_validate(payload)
