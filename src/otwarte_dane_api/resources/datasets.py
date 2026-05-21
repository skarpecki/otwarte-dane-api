"""Datasets resource namespace."""

from __future__ import annotations

from typing import Any

from ..models.common import Document, Resource
from ..models.dataset import Dataset
from ..models.resource import DataResource
from ..models.showcase import Showcase
from ..pagination import AsyncPaginator, Paginator
from ._base import ResourceId, _AsyncResource, _SyncResource, _build_params, _lang_params

_LIST_DOC = Document[list[Resource[Dataset]]]
_ONE_DOC = Document[Resource[Dataset]]
_RES_LIST_DOC = Document[list[Resource[DataResource]]]
_SHOWCASE_LIST_DOC = Document[list[Resource[Showcase]]]


class DatasetsResource(_SyncResource):
    def list(self, *, page=None, per_page=None, sort=None, lang=None, **filters: Any) -> Paginator[Dataset]:
        return self._get_paginator(
            _LIST_DOC,
            Dataset,
            "datasets",
            params=_build_params(
                page=page, per_page=per_page, sort=sort, lang=lang, filters=filters
            ),
        )

    def get(self, dataset_id: ResourceId, *, lang=None) -> Dataset:
        return self._get_entity(
            _ONE_DOC, Dataset, "datasets", dataset_id, params=_lang_params(lang)
        )

    def list_resources(self, dataset_id: ResourceId, *, page=None, per_page=None, sort=None, lang=None, **filters: Any) -> Paginator[DataResource]:
        return self._get_paginator(
            _RES_LIST_DOC,
            DataResource,
            "datasets",
            dataset_id,
            "resources",
            params=_build_params(
                page=page, per_page=per_page, sort=sort, lang=lang, filters=filters
            ),
        )

    def list_showcases(self, dataset_id: ResourceId, *, page=None, per_page=None, sort=None, lang=None, **filters: Any) -> Paginator[Showcase]:
        return self._get_paginator(
            _SHOWCASE_LIST_DOC,
            Showcase,
            "datasets",
            dataset_id,
            "showcases",
            params=_build_params(
                page=page, per_page=per_page, sort=sort, lang=lang, filters=filters
            ),
        )

    def list_raw(self, *, page=None, per_page=None, sort=None, lang=None, **filters: Any) -> _LIST_DOC:
        return self._get_document(
            _LIST_DOC,
            "datasets",
            params=_build_params(
                page=page, per_page=per_page, sort=sort, lang=lang, filters=filters
            ),
        )

    def get_raw(self, dataset_id: ResourceId, *, lang=None) -> _ONE_DOC:
        return self._get_document(
            _ONE_DOC, "datasets", dataset_id, params=_lang_params(lang)
        )

    def list_resources_raw(self, dataset_id: ResourceId, *, page=None, per_page=None, sort=None, lang=None, **filters: Any) -> _RES_LIST_DOC:
        return self._get_document(
            _RES_LIST_DOC,
            "datasets",
            dataset_id,
            "resources",
            params=_build_params(
                page=page, per_page=per_page, sort=sort, lang=lang, filters=filters
            ),
        )

    def list_showcases_raw(self, dataset_id: ResourceId, *, page=None, per_page=None, sort=None, lang=None, **filters: Any) -> _SHOWCASE_LIST_DOC:
        return self._get_document(
            _SHOWCASE_LIST_DOC,
            "datasets",
            dataset_id,
            "showcases",
            params=_build_params(
                page=page, per_page=per_page, sort=sort, lang=lang, filters=filters
            ),
        )


class AsyncDatasetsResource(_AsyncResource):
    async def list(self, *, page=None, per_page=None, sort=None, lang=None, **filters: Any) -> AsyncPaginator[Dataset]:
        return await self._get_paginator(
            _LIST_DOC,
            Dataset,
            "datasets",
            params=_build_params(
                page=page, per_page=per_page, sort=sort, lang=lang, filters=filters
            ),
        )

    async def get(self, dataset_id: ResourceId, *, lang=None) -> Dataset:
        return await self._get_entity(
            _ONE_DOC, Dataset, "datasets", dataset_id, params=_lang_params(lang)
        )

    async def list_resources(self, dataset_id: ResourceId, *, page=None, per_page=None, sort=None, lang=None, **filters: Any) -> AsyncPaginator[DataResource]:
        return await self._get_paginator(
            _RES_LIST_DOC,
            DataResource,
            "datasets",
            dataset_id,
            "resources",
            params=_build_params(
                page=page, per_page=per_page, sort=sort, lang=lang, filters=filters
            ),
        )

    async def list_showcases(self, dataset_id: ResourceId, *, page=None, per_page=None, sort=None, lang=None, **filters: Any) -> AsyncPaginator[Showcase]:
        return await self._get_paginator(
            _SHOWCASE_LIST_DOC,
            Showcase,
            "datasets",
            dataset_id,
            "showcases",
            params=_build_params(
                page=page, per_page=per_page, sort=sort, lang=lang, filters=filters
            ),
        )

    async def list_raw(self, *, page=None, per_page=None, sort=None, lang=None, **filters: Any) -> _LIST_DOC:
        return await self._get_document(
            _LIST_DOC,
            "datasets",
            params=_build_params(
                page=page, per_page=per_page, sort=sort, lang=lang, filters=filters
            ),
        )

    async def get_raw(self, dataset_id: ResourceId, *, lang=None) -> _ONE_DOC:
        return await self._get_document(
            _ONE_DOC, "datasets", dataset_id, params=_lang_params(lang)
        )

    async def list_resources_raw(self, dataset_id: ResourceId, *, page=None, per_page=None, sort=None, lang=None, **filters: Any) -> _RES_LIST_DOC:
        return await self._get_document(
            _RES_LIST_DOC,
            "datasets",
            dataset_id,
            "resources",
            params=_build_params(
                page=page, per_page=per_page, sort=sort, lang=lang, filters=filters
            ),
        )

    async def list_showcases_raw(self, dataset_id: ResourceId, *, page=None, per_page=None, sort=None, lang=None, **filters: Any) -> _SHOWCASE_LIST_DOC:
        return await self._get_document(
            _SHOWCASE_LIST_DOC,
            "datasets",
            dataset_id,
            "showcases",
            params=_build_params(
                page=page, per_page=per_page, sort=sort, lang=lang, filters=filters
            ),
        )
