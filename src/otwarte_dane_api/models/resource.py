"""Models for the resources namespace."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict

from .common import Resource as JsonApiResource


class ResourceRegion(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | int | None = None
    name: str | None = None
    title: str | None = None


class ResourceSupplement(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | int | None = None
    title: str | None = None
    description: str | None = None
    url: str | None = None
    file_url: str | None = None
    format: str | None = None


class ResourceSpecialSign(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    name: str | None = None
    title: str | None = None
    description: str | None = None


class DataResource(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    title: str | None = None
    description: str | None = None
    format: str | None = None
    file_url: str | None = None
    download_url: str | None = None
    link: str | None = None
    csv_file_url: str | None = None
    jsonld_file_url: str | None = None
    openness_score: int | None = None
    views_count: int | None = None
    downloads_count: int | None = None
    data_date: str | None = None
    file_size: int | None = None
    has_chart: bool | None = None
    has_map: bool | None = None
    has_table: bool | None = None
    has_dynamic_data: bool | None = None
    has_high_value_data: bool | None = None
    has_research_data: bool | None = None
    is_chart_creation_blocked: bool | None = None
    license_code: str | None = None
    license_name: str | None = None
    modified: str | None = None
    created: str | None = None
    verified: str | None = None
    attribute_type: str | None = None
    type: str | None = None
    language: str | None = None
    geo_data: Any = None
    regions: list[ResourceRegion] | None = None
    media_type: str | None = None
    category: str | None = None
    csv_download_url: str | None = None
    jsonld_download_url: str | None = None
    csv_file_size: int | None = None
    jsonld_file_size: int | None = None
    visualization_types: list[str] | None = None
    has_high_value_data_from_ec_list: bool | None = None
    contains_protected_data: bool | None = None
    supplements: list[ResourceSupplement] | None = None
    special_signs: list[ResourceSpecialSign] | None = None


class TableRow(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)


class ResourceTableMeta(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    headers_map: dict[str, Any] | None = None
    data_schema: dict[str, Any] | None = None
    count: int | None = None


ResourceAttributes = DataResource
TableRowAttributes = TableRow

__all__ = [
    "DataResource",
    "JsonApiResource",
    "ResourceAttributes",
    "ResourceRegion",
    "ResourceSpecialSign",
    "ResourceSupplement",
    "ResourceTableMeta",
    "TableRow",
    "TableRowAttributes",
]
