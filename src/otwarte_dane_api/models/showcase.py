"""Showcase models."""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict


class ExternalDataset(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    url: Optional[str] = None
    title: Optional[str] = None


class Showcase(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    title: Optional[str] = None
    notes: Optional[str] = None
    slug: Optional[str] = None
    url: Optional[str] = None
    image_url: Optional[str] = None
    image_thumb_url: Optional[str] = None
    license_type: Optional[str] = None
    license_logo_url: Optional[str] = None
    main_page_position: Optional[int] = None
    modified: Optional[str] = None
    created: Optional[str] = None
    views_count: Optional[int] = None
    illustrative_graphics_url: Optional[str] = None
    illustrative_graphics_alt: Optional[str] = None
    has_chart: Optional[bool] = None
    has_map: Optional[bool] = None
    has_table: Optional[bool] = None
    has_image: Optional[bool] = None
    author: Optional[str] = None
    category: Optional[str] = None
    image_alt: Optional[str] = None
    tags: Optional[list[str]] = None
    keywords: Optional[list[str]] = None
    external_datasets: Optional[list[ExternalDataset]] = None
    followed: Optional[bool] = None
    has_image_thumb: Optional[bool] = None
    is_mobile_app: Optional[bool] = None
    is_desktop_app: Optional[bool] = None
    mobile_apple_url: Optional[str] = None
    mobile_google_url: Optional[str] = None
    desktop_linux_url: Optional[str] = None
    desktop_macos_url: Optional[str] = None
    desktop_windows_url: Optional[str] = None


ShowcaseAttributes = Showcase

__all__ = ["ExternalDataset", "Showcase", "ShowcaseAttributes"]
