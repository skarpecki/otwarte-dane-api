"""Showcases resource namespace."""

from __future__ import annotations

from typing import Any

from ..models.common import Document, Resource
from ..models.showcase import Showcase
from ..pagination import AsyncPaginator, Paginator
from ._base import ResourceId, _AsyncResource, _SyncResource, _build_params, _lang_params

_LIST_DOC = Document[list[Resource[Showcase]]]
_ONE_DOC = Document[Resource[Showcase]]


class ShowcasesResource(_SyncResource):
    def list(self, *, page=None, per_page=None, sort=None, lang=None, **filters: Any) -> Paginator[Showcase]:
        return self._get_paginator(
            _LIST_DOC,
            Showcase,
            "showcases",
            params=_build_params(
                page=page, per_page=per_page, sort=sort, lang=lang, filters=filters
            ),
        )

    def get(self, showcase_id: ResourceId, *, lang=None) -> Showcase:
        return self._get_entity(
            _ONE_DOC, Showcase, "showcases", showcase_id, params=_lang_params(lang)
        )

    def list_raw(self, *, page=None, per_page=None, sort=None, lang=None, **filters: Any) -> _LIST_DOC:
        return self._get_document(
            _LIST_DOC,
            "showcases",
            params=_build_params(
                page=page, per_page=per_page, sort=sort, lang=lang, filters=filters
            ),
        )

    def get_raw(self, showcase_id: ResourceId, *, lang=None) -> _ONE_DOC:
        return self._get_document(
            _ONE_DOC, "showcases", showcase_id, params=_lang_params(lang)
        )


class AsyncShowcasesResource(_AsyncResource):
    async def list(self, *, page=None, per_page=None, sort=None, lang=None, **filters: Any) -> AsyncPaginator[Showcase]:
        return await self._get_paginator(
            _LIST_DOC,
            Showcase,
            "showcases",
            params=_build_params(
                page=page, per_page=per_page, sort=sort, lang=lang, filters=filters
            ),
        )

    async def get(self, showcase_id: ResourceId, *, lang=None) -> Showcase:
        return await self._get_entity(
            _ONE_DOC, Showcase, "showcases", showcase_id, params=_lang_params(lang)
        )

    async def list_raw(self, *, page=None, per_page=None, sort=None, lang=None, **filters: Any) -> _LIST_DOC:
        return await self._get_document(
            _LIST_DOC,
            "showcases",
            params=_build_params(
                page=page, per_page=per_page, sort=sort, lang=lang, filters=filters
            ),
        )

    async def get_raw(self, showcase_id: ResourceId, *, lang=None) -> _ONE_DOC:
        return await self._get_document(
            _ONE_DOC, "showcases", showcase_id, params=_lang_params(lang)
        )
