"""Search resource namespace."""

from __future__ import annotations

from typing import Any, Optional, Sequence

from ..models.common import Document, Resource
from ..models.search import SearchResult, SearchResultAttributes
from ..pagination import AsyncPaginator, Paginator, build_page_params
from ._base import _AsyncResource, _SyncResource


def _build_search_params(
    q: str,
    *,
    models: Optional[Sequence[str]] = None,
    page: Optional[int] = None,
    per_page: Optional[int] = None,
    sort: Optional[str] = None,
    lang: Optional[str] = None,
    filters: dict[str, Any],
) -> dict[str, Any]:
    extra: dict[str, Any] = {"q": q, **filters}
    if models:
        extra["model"] = ",".join(models)
    if lang is not None:
        extra["lang"] = lang
    return build_page_params(page=page, per_page=per_page, sort=sort, extra=extra)


_LIST_DOC = Document[list[Resource[SearchResultAttributes]]]


class SearchResource(_SyncResource):
    def query(
        self,
        q: str,
        *,
        models: Optional[Sequence[str]] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
        sort: Optional[str] = None,
        lang: Optional[str] = None,
        **filters: Any,
    ) -> Paginator[SearchResult]:
        return self._get_paginator(
            _LIST_DOC,
            SearchResult,
            "search",
            params=_build_search_params(
                q,
                models=models,
                page=page,
                per_page=per_page,
                sort=sort,
                lang=lang,
                filters=filters,
            ),
        )

    def query_raw(
        self,
        q: str,
        *,
        models: Optional[Sequence[str]] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
        sort: Optional[str] = None,
        lang: Optional[str] = None,
        **filters: Any,
    ) -> Document[list[Resource[SearchResultAttributes]]]:
        return self._get_document(
            _LIST_DOC,
            "search",
            params=_build_search_params(
                q,
                models=models,
                page=page,
                per_page=per_page,
                sort=sort,
                lang=lang,
                filters=filters,
            ),
        )


class AsyncSearchResource(_AsyncResource):
    async def query(
        self,
        q: str,
        *,
        models: Optional[Sequence[str]] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
        sort: Optional[str] = None,
        lang: Optional[str] = None,
        **filters: Any,
    ) -> AsyncPaginator[SearchResult]:
        return await self._get_paginator(
            _LIST_DOC,
            SearchResult,
            "search",
            params=_build_search_params(
                q,
                models=models,
                page=page,
                per_page=per_page,
                sort=sort,
                lang=lang,
                filters=filters,
            ),
        )

    async def query_raw(
        self,
        q: str,
        *,
        models: Optional[Sequence[str]] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
        sort: Optional[str] = None,
        lang: Optional[str] = None,
        **filters: Any,
    ) -> Document[list[Resource[SearchResultAttributes]]]:
        return await self._get_document(
            _LIST_DOC,
            "search",
            params=_build_search_params(
                q,
                models=models,
                page=page,
                per_page=per_page,
                sort=sort,
                lang=lang,
                filters=filters,
            ),
        )
