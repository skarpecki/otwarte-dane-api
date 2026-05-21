"""Resources namespace."""

from __future__ import annotations

from typing import Any

from ..models.common import Document, Resource as ApiResource
from ..models.resource import DataResource, TableRow
from ..pagination import AsyncPaginator, Paginator
from ._base import ResourceId, _AsyncResource, _SyncResource, _build_params, _lang_params

_LIST_DOC = Document[list[ApiResource[DataResource]]]
_ONE_DOC = Document[ApiResource[DataResource]]
_DATA_LIST_DOC = Document[list[ApiResource[TableRow]]]
_DATA_ONE_DOC = Document[ApiResource[TableRow]]


class ResourcesResource(_SyncResource):
    def list(self, *, page=None, per_page=None, sort=None, lang=None, **filters: Any) -> Paginator[DataResource]:
        return self._get_paginator(
            _LIST_DOC,
            DataResource,
            "resources",
            params=_build_params(
                page=page, per_page=per_page, sort=sort, lang=lang, filters=filters
            ),
        )

    def get(self, resource_id: ResourceId, *, lang=None) -> DataResource:
        return self._get_entity(
            _ONE_DOC, DataResource, "resources", resource_id, params=_lang_params(lang)
        )

    def get_data(self, resource_id: ResourceId, *, page=None, per_page=None, sort=None, lang=None, **filters: Any) -> Paginator[TableRow]:
        return self._get_paginator(
            _DATA_LIST_DOC,
            TableRow,
            "resources",
            resource_id,
            "data",
            params=_build_params(
                page=page, per_page=per_page, sort=sort, lang=lang, filters=filters
            ),
        )

    def get_row(self, resource_id: ResourceId, row_id: ResourceId) -> TableRow:
        return self._get_entity(
            _DATA_ONE_DOC, TableRow, "resources", resource_id, "data", row_id
        )

    def list_raw(self, *, page=None, per_page=None, sort=None, lang=None, **filters: Any) -> _LIST_DOC:
        return self._get_document(
            _LIST_DOC,
            "resources",
            params=_build_params(
                page=page, per_page=per_page, sort=sort, lang=lang, filters=filters
            ),
        )

    def get_raw(self, resource_id: ResourceId, *, lang=None) -> _ONE_DOC:
        return self._get_document(
            _ONE_DOC, "resources", resource_id, params=_lang_params(lang)
        )

    def get_data_raw(self, resource_id: ResourceId, *, page=None, per_page=None, sort=None, lang=None, **filters: Any) -> _DATA_LIST_DOC:
        return self._get_document(
            _DATA_LIST_DOC,
            "resources",
            resource_id,
            "data",
            params=_build_params(
                page=page, per_page=per_page, sort=sort, lang=lang, filters=filters
            ),
        )

    def get_row_raw(self, resource_id: ResourceId, row_id: ResourceId) -> _DATA_ONE_DOC:
        return self._get_document(_DATA_ONE_DOC, "resources", resource_id, "data", row_id)


class AsyncResourcesResource(_AsyncResource):
    async def list(self, *, page=None, per_page=None, sort=None, lang=None, **filters: Any) -> AsyncPaginator[DataResource]:
        return await self._get_paginator(
            _LIST_DOC,
            DataResource,
            "resources",
            params=_build_params(
                page=page, per_page=per_page, sort=sort, lang=lang, filters=filters
            ),
        )

    async def get(self, resource_id: ResourceId, *, lang=None) -> DataResource:
        return await self._get_entity(
            _ONE_DOC, DataResource, "resources", resource_id, params=_lang_params(lang)
        )

    async def get_data(self, resource_id: ResourceId, *, page=None, per_page=None, sort=None, lang=None, **filters: Any) -> AsyncPaginator[TableRow]:
        return await self._get_paginator(
            _DATA_LIST_DOC,
            TableRow,
            "resources",
            resource_id,
            "data",
            params=_build_params(
                page=page, per_page=per_page, sort=sort, lang=lang, filters=filters
            ),
        )

    async def get_row(self, resource_id: ResourceId, row_id: ResourceId) -> TableRow:
        return await self._get_entity(
            _DATA_ONE_DOC, TableRow, "resources", resource_id, "data", row_id
        )

    async def list_raw(self, *, page=None, per_page=None, sort=None, lang=None, **filters: Any) -> _LIST_DOC:
        return await self._get_document(
            _LIST_DOC,
            "resources",
            params=_build_params(
                page=page, per_page=per_page, sort=sort, lang=lang, filters=filters
            ),
        )

    async def get_raw(self, resource_id: ResourceId, *, lang=None) -> _ONE_DOC:
        return await self._get_document(
            _ONE_DOC, "resources", resource_id, params=_lang_params(lang)
        )

    async def get_data_raw(self, resource_id: ResourceId, *, page=None, per_page=None, sort=None, lang=None, **filters: Any) -> _DATA_LIST_DOC:
        return await self._get_document(
            _DATA_LIST_DOC,
            "resources",
            resource_id,
            "data",
            params=_build_params(
                page=page, per_page=per_page, sort=sort, lang=lang, filters=filters
            ),
        )

    async def get_row_raw(self, resource_id: ResourceId, row_id: ResourceId) -> _DATA_ONE_DOC:
        return await self._get_document(
            _DATA_ONE_DOC, "resources", resource_id, "data", row_id
        )
