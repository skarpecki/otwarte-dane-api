"""Base classes for resource namespaces."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Mapping, Type, TypeVar

from pydantic import BaseModel

from ..models.flatten import flatten_resource
from ..pagination import AsyncPaginator, Paginator, build_page_params

if TYPE_CHECKING:
    from .._http import AsyncHttpTransport, HttpTransport

ResourceId = str | int
T = TypeVar("T", bound=BaseModel)


def _path(*parts: ResourceId) -> str:
    segments: list[str] = []
    for part in parts:
        segment = str(part).strip("/")
        if not segment:
            raise ValueError("Path segments must be non-empty")
        if any(separator in segment for separator in ("/", "\\", "?", "#")):
            raise ValueError(f"Invalid path segment: {segment!r}")
        segments.append(segment)
    return "/" + "/".join(segments)


def _build_params(
    *,
    page: int | None = None,
    per_page: int | None = None,
    sort: str | None = None,
    lang: str | None = None,
    filters: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    params = build_page_params(page=page, per_page=per_page, sort=sort, extra=filters)
    if lang is not None:
        params["lang"] = lang
    return params


def _lang_params(lang: str | None = None) -> dict[str, str] | None:
    return {"lang": lang} if lang is not None else None


def _flatten_as(attr_cls: Type[T]):
    def _flatten(resource: Any) -> T:
        return flatten_resource(resource, attr_cls)

    return _flatten


class _SyncResource:
    def __init__(self, http: "HttpTransport") -> None:
        self._http = http

    def _get_document(
        self,
        document_cls: Any,
        *path_parts: ResourceId,
        params: Mapping[str, Any] | None = None,
    ) -> Any:
        payload = self._http.get(_path(*path_parts), params=params)
        return document_cls.model_validate(payload)

    def _get_entity(
        self,
        document_cls: Any,
        attr_cls: Type[T],
        *path_parts: ResourceId,
        params: Mapping[str, Any] | None = None,
    ) -> T:
        return flatten_resource(
            self._get_document(document_cls, *path_parts, params=params).data,
            attr_cls,
        )

    def _get_paginator(
        self,
        document_cls: Any,
        attr_cls: Type[T],
        *path_parts: ResourceId,
        params: Mapping[str, Any],
    ) -> Paginator[T]:
        return Paginator(
            http=self._http,
            path=_path(*path_parts),
            params=params,
            document_cls=document_cls,
            transform=_flatten_as(attr_cls),
        )

    def _get_bytes(
        self,
        *path_parts: ResourceId,
        params: Mapping[str, Any] | None = None,
    ) -> bytes:
        return self._http.get_bytes(_path(*path_parts), params=params)


class _AsyncResource:
    def __init__(self, http: "AsyncHttpTransport") -> None:
        self._http = http

    async def _get_document(
        self,
        document_cls: Any,
        *path_parts: ResourceId,
        params: Mapping[str, Any] | None = None,
    ) -> Any:
        payload = await self._http.get(_path(*path_parts), params=params)
        return document_cls.model_validate(payload)

    async def _get_entity(
        self,
        document_cls: Any,
        attr_cls: Type[T],
        *path_parts: ResourceId,
        params: Mapping[str, Any] | None = None,
    ) -> T:
        return flatten_resource(
            (await self._get_document(document_cls, *path_parts, params=params)).data,
            attr_cls,
        )

    async def _get_paginator(
        self,
        document_cls: Any,
        attr_cls: Type[T],
        *path_parts: ResourceId,
        params: Mapping[str, Any],
    ) -> AsyncPaginator[T]:
        return await AsyncPaginator.create(
            http=self._http,
            path=_path(*path_parts),
            params=params,
            document_cls=document_cls,
            transform=_flatten_as(attr_cls),
        )

    async def _get_bytes(
        self,
        *path_parts: ResourceId,
        params: Mapping[str, Any] | None = None,
    ) -> bytes:
        return await self._http.get_bytes(_path(*path_parts), params=params)
