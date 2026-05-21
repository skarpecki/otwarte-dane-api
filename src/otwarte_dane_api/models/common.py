"""Shared JSON:API envelope models."""

from __future__ import annotations

from typing import Any, Generic, Optional, TypeVar

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


class _Base(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)


class Links(_Base):
    self_: Optional[str] = Field(default=None, alias="self")
    first: Optional[str] = None
    last: Optional[str] = None
    next: Optional[str] = None
    prev: Optional[str] = None
    related: Optional[str] = None


class Meta(_Base):
    count: Optional[int] = None
    server_time: Optional[str] = None
    relative_uri: Optional[str] = None
    language: Optional[str] = None
    params: Optional[dict[str, Any]] = None
    path: Optional[str] = None
    aggregations: Optional[dict[str, Any]] = None


class RelationshipRef(_Base):
    id: Optional[str] = None
    type: Optional[str] = None


class Relationship(_Base):
    links: Optional[Links] = None
    meta: Optional[dict[str, Any]] = None
    data: Optional[RelationshipRef | list[RelationshipRef]] = None


class ErrorSource(_Base):
    pointer: Optional[str] = None
    parameter: Optional[str] = None
    header: Optional[str] = None


class ErrorObject(_Base):
    id: Optional[str] = None
    status: Optional[str] = None
    code: Optional[str] = None
    title: Optional[str] = None
    detail: Optional[str] = None
    source: Optional[ErrorSource] = None


class Resource(_Base, Generic[T]):
    """A single JSON:API resource object with typed attributes."""

    id: str
    type: str
    attributes: Optional[T] = None
    relationships: Optional[dict[str, Relationship]] = None
    links: Optional[Links] = None
    meta: Optional[dict[str, Any]] = None


class Document(_Base, Generic[T]):
    """A JSON:API top-level document.

    `data` is generic over either a single `Resource[Attrs]` or a list.
    """

    jsonapi: Optional[dict[str, Any] | str] = None
    data: Optional[T] = None
    included: Optional[list[Resource[Any]]] = None
    errors: Optional[list[ErrorObject]] = None
    meta: Optional[Meta] = None
    links: Optional[Links] = None
