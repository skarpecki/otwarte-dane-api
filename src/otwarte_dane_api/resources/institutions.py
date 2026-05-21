"""Institutions resource namespace."""

from __future__ import annotations

from typing import Any

from ..models.common import Document, Resource
from ..models.dataset import Dataset
from ..models.institution import Institution
from ..pagination import AsyncPaginator, Paginator
from ._base import ResourceId, _AsyncResource, _SyncResource, _build_params, _lang_params

_LIST_DOC = Document[list[Resource[Institution]]]
_ONE_DOC = Document[Resource[Institution]]
_SUB_LIST_DOC = Document[list[Resource[Dataset]]]


class InstitutionsResource(_SyncResource):
    def list(self, *, page=None, per_page=None, sort=None, lang=None, **filters: Any) -> Paginator[Institution]:
        return self._get_paginator(
            _LIST_DOC,
            Institution,
            "institutions",
            params=_build_params(
                page=page, per_page=per_page, sort=sort, lang=lang, filters=filters
            ),
        )

    def get(self, institution_id: ResourceId, *, lang=None) -> Institution:
        return self._get_entity(
            _ONE_DOC,
            Institution,
            "institutions",
            institution_id,
            params=_lang_params(lang),
        )

    def list_datasets(self, institution_id: ResourceId, *, page=None, per_page=None, sort=None, lang=None, **filters: Any) -> Paginator[Dataset]:
        return self._get_paginator(
            _SUB_LIST_DOC,
            Dataset,
            "institutions",
            institution_id,
            "datasets",
            params=_build_params(
                page=page, per_page=per_page, sort=sort, lang=lang, filters=filters
            ),
        )

    def list_raw(self, *, page=None, per_page=None, sort=None, lang=None, **filters: Any) -> _LIST_DOC:
        return self._get_document(
            _LIST_DOC,
            "institutions",
            params=_build_params(
                page=page, per_page=per_page, sort=sort, lang=lang, filters=filters
            ),
        )

    def get_raw(self, institution_id: ResourceId, *, lang=None) -> _ONE_DOC:
        return self._get_document(
            _ONE_DOC, "institutions", institution_id, params=_lang_params(lang)
        )

    def list_datasets_raw(self, institution_id: ResourceId, *, page=None, per_page=None, sort=None, lang=None, **filters: Any) -> _SUB_LIST_DOC:
        return self._get_document(
            _SUB_LIST_DOC,
            "institutions",
            institution_id,
            "datasets",
            params=_build_params(
                page=page, per_page=per_page, sort=sort, lang=lang, filters=filters
            ),
        )


class AsyncInstitutionsResource(_AsyncResource):
    async def list(self, *, page=None, per_page=None, sort=None, lang=None, **filters: Any) -> AsyncPaginator[Institution]:
        return await self._get_paginator(
            _LIST_DOC,
            Institution,
            "institutions",
            params=_build_params(
                page=page, per_page=per_page, sort=sort, lang=lang, filters=filters
            ),
        )

    async def get(self, institution_id: ResourceId, *, lang=None) -> Institution:
        return await self._get_entity(
            _ONE_DOC,
            Institution,
            "institutions",
            institution_id,
            params=_lang_params(lang),
        )

    async def list_datasets(self, institution_id: ResourceId, *, page=None, per_page=None, sort=None, lang=None, **filters: Any) -> AsyncPaginator[Dataset]:
        return await self._get_paginator(
            _SUB_LIST_DOC,
            Dataset,
            "institutions",
            institution_id,
            "datasets",
            params=_build_params(
                page=page, per_page=per_page, sort=sort, lang=lang, filters=filters
            ),
        )

    async def list_raw(self, *, page=None, per_page=None, sort=None, lang=None, **filters: Any) -> _LIST_DOC:
        return await self._get_document(
            _LIST_DOC,
            "institutions",
            params=_build_params(
                page=page, per_page=per_page, sort=sort, lang=lang, filters=filters
            ),
        )

    async def get_raw(self, institution_id: ResourceId, *, lang=None) -> _ONE_DOC:
        return await self._get_document(
            _ONE_DOC, "institutions", institution_id, params=_lang_params(lang)
        )

    async def list_datasets_raw(self, institution_id: ResourceId, *, page=None, per_page=None, sort=None, lang=None, **filters: Any) -> _SUB_LIST_DOC:
        return await self._get_document(
            _SUB_LIST_DOC,
            "institutions",
            institution_id,
            "datasets",
            params=_build_params(
                page=page, per_page=per_page, sort=sort, lang=lang, filters=filters
            ),
        )
