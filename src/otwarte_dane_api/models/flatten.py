"""Helpers for converting JSON:API resources to flat entity objects."""

from __future__ import annotations

from typing import Any, Mapping, Type, TypeVar

from pydantic import BaseModel

from .common import Resource

T = TypeVar("T", bound=BaseModel)


def flatten_resource(resource: Resource[Any], attr_cls: Type[T]) -> T:
    """Merge a JSON:API ``Resource`` envelope's id/type into its attributes
    model and return a single flat pydantic instance.

    Relies on ``extra="allow"`` on the attribute model (already set on all
    `*Attributes` models in this package) so ``id`` and ``type`` become
    accessible as fields on the returned object.
    """
    if resource.attributes is None:
        data: dict[str, Any] = {}
    elif isinstance(resource.attributes, BaseModel):
        data = resource.attributes.model_dump(by_alias=False, exclude_none=False)
    elif isinstance(resource.attributes, Mapping):
        data = dict(resource.attributes)
    else:
        raise TypeError(
            f"Cannot flatten resource attributes of type {type(resource.attributes)!r}"
        )

    attribute_type = data.get("type")
    if attribute_type is not None and attribute_type != resource.type:
        if data.get("attribute_type") is None:
            data["attribute_type"] = attribute_type
    data["id"] = resource.id
    data["type"] = resource.type
    return attr_cls.model_validate(data)


def flatten_dict_resource(resource: Resource[Any]) -> dict[str, Any]:
    """Flatten a ``Resource[dict]`` (untyped attributes) to a plain dict
    with ``id`` and ``type`` merged in.
    """
    if resource.attributes is None:
        data: dict[str, Any] = {}
    elif isinstance(resource.attributes, Mapping):
        data = dict(resource.attributes)
    elif isinstance(resource.attributes, BaseModel):
        data = resource.attributes.model_dump(by_alias=False, exclude_none=False)
    else:
        raise TypeError(
            f"Cannot flatten resource attributes of type {type(resource.attributes)!r}"
        )

    attribute_type = data.get("type")
    if attribute_type is not None and attribute_type != resource.type:
        if data.get("attribute_type") is None:
            data["attribute_type"] = attribute_type
    data["id"] = resource.id
    data["type"] = resource.type
    return data
