"""Reports resource namespace."""

from __future__ import annotations

from typing import Any, Optional

from ..models.common import Document, Resource
from ..models.report import BrokenLinkEntry, BrokenLinkReport
from ..pagination import AsyncPaginator, Paginator
from ._base import _AsyncResource, _SyncResource, _build_params, _lang_params

_LIST_DOC = Document[list[Resource[BrokenLinkEntry]]]
_ONE_DOC = Document[Resource[BrokenLinkReport]]


class ReportsResource(_SyncResource):
    def get_broken_links_report(
        self,
        *,
        lang: Optional[str] = None,
    ) -> BrokenLinkReport:
        return self._get_entity(
            _ONE_DOC,
            BrokenLinkReport,
            "reports",
            "brokenlinks",
            params=_lang_params(lang),
        )

    def get_broken_links_report_raw(
        self,
        *,
        lang: Optional[str] = None,
    ) -> _ONE_DOC:
        return self._get_document(
            _ONE_DOC, "reports", "brokenlinks", params=_lang_params(lang)
        )

    def list_broken_links(
        self,
        *,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
        sort: Optional[str] = None,
        lang: Optional[str] = None,
        **filters: Any,
    ) -> Paginator[BrokenLinkEntry]:
        return self._get_paginator(
            _LIST_DOC,
            BrokenLinkEntry,
            "reports",
            "brokenlinks",
            "data",
            params=_build_params(
                page=page, per_page=per_page, sort=sort, lang=lang, filters=filters
            ),
        )

    def list_broken_links_raw(
        self,
        *,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
        sort: Optional[str] = None,
        lang: Optional[str] = None,
        **filters: Any,
    ) -> _LIST_DOC:
        return self._get_document(
            _LIST_DOC,
            "reports",
            "brokenlinks",
            "data",
            params=_build_params(
                page=page, per_page=per_page, sort=sort, lang=lang, filters=filters
            ),
        )

    def download_broken_links(self, extension: str) -> bytes:
        return self._get_bytes("reports", "brokenlinks", extension)


class AsyncReportsResource(_AsyncResource):
    async def get_broken_links_report(
        self,
        *,
        lang: Optional[str] = None,
    ) -> BrokenLinkReport:
        return await self._get_entity(
            _ONE_DOC,
            BrokenLinkReport,
            "reports",
            "brokenlinks",
            params=_lang_params(lang),
        )

    async def get_broken_links_report_raw(
        self,
        *,
        lang: Optional[str] = None,
    ) -> _ONE_DOC:
        return await self._get_document(
            _ONE_DOC, "reports", "brokenlinks", params=_lang_params(lang)
        )

    async def list_broken_links(
        self,
        *,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
        sort: Optional[str] = None,
        lang: Optional[str] = None,
        **filters: Any,
    ) -> AsyncPaginator[BrokenLinkEntry]:
        return await self._get_paginator(
            _LIST_DOC,
            BrokenLinkEntry,
            "reports",
            "brokenlinks",
            "data",
            params=_build_params(
                page=page, per_page=per_page, sort=sort, lang=lang, filters=filters
            ),
        )

    async def list_broken_links_raw(
        self,
        *,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
        sort: Optional[str] = None,
        lang: Optional[str] = None,
        **filters: Any,
    ) -> _LIST_DOC:
        return await self._get_document(
            _LIST_DOC,
            "reports",
            "brokenlinks",
            "data",
            params=_build_params(
                page=page, per_page=per_page, sort=sort, lang=lang, filters=filters
            ),
        )

    async def download_broken_links(self, extension: str) -> bytes:
        return await self._get_bytes("reports", "brokenlinks", extension)
