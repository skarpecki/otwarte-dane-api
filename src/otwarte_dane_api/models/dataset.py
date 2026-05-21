"""Dataset models."""

from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict

from .common import Links, Meta, Relationship


class DatasetCategory(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | int | None = None
    title: str | None = None
    name: str | None = None
    description: str | None = None


class DatasetTag(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | int | None = None
    name: str | None = None
    title: str | None = None


class DatasetSource(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    title: str | None = None
    url: str | None = None
    type: str | None = None


class Dataset(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    title: Optional[str] = None
    slug: Optional[str] = None
    notes: Optional[str] = None
    category: Optional[DatasetCategory] = None
    categories: Optional[list[DatasetCategory]] = None
    formats: Optional[list[Any]] = None
    tags: Optional[list[DatasetTag]] = None
    license_code: Optional[str] = None
    license_name: Optional[str] = None
    source: Optional[DatasetSource] = None
    update_frequency: Optional[str] = None
    views_count: Optional[int] = None
    downloads_count: Optional[int] = None
    has_dynamic_data: Optional[bool] = None
    has_high_value_data: Optional[bool] = None
    has_research_data: Optional[bool] = None
    followed: Optional[bool] = None
    modified: Optional[str] = None
    created: Optional[str] = None
    verified: Optional[str] = None
    url: Optional[str] = None
    image_url: Optional[str] = None
    modified_by_resources_data: Optional[bool] = None
    modified_data: Optional[str] = None
    last_modified_resource: Optional[str] = None


DatasetAttributes = Dataset

__all__ = [
    "Dataset",
    "DatasetAttributes",
    "DatasetCategory",
    "DatasetSource",
    "DatasetTag",
    "Links",
    "Meta",
    "Relationship",
]
