"""Report models."""

from __future__ import annotations

from typing import Optional

from pydantic import ConfigDict

from .common import _Base


class BrokenLinkReportFile(_Base):
    download_url: Optional[str] = None
    file_size: Optional[int] = None
    format: Optional[str] = None


class BrokenLinkReport(_Base):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    title: Optional[str] = None
    description: Optional[str] = None
    file_url: Optional[str] = None
    created: Optional[str] = None
    modified: Optional[str] = None
    status: Optional[str] = None
    rows_count: Optional[int] = None
    update_date: Optional[str] = None
    files: Optional[list[BrokenLinkReportFile]] = None


class BrokenLinkRelatedObject(_Base):
    id: Optional[str] = None
    type: Optional[str] = None
    title: Optional[str] = None
    name: Optional[str] = None
    url: Optional[str] = None


class BrokenLinkEntry(_Base):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    link: Optional[str | BrokenLinkRelatedObject] = None
    status_code: Optional[int] = None
    resource_id: Optional[str] = None
    dataset_id: Optional[str] = None
    last_checked: Optional[str] = None
    error_message: Optional[str] = None
    institution: Optional[str | BrokenLinkRelatedObject] = None
    dataset: Optional[str | BrokenLinkRelatedObject] = None
    portal_data_link: Optional[str | BrokenLinkRelatedObject] = None
    modified: Optional[str] = None
    created: Optional[str] = None
    file_url: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None


BrokenLinkReportAttributes = BrokenLinkReport
BrokenLinkEntryAttributes = BrokenLinkEntry

__all__ = [
    "BrokenLinkEntry",
    "BrokenLinkEntryAttributes",
    "BrokenLinkRelatedObject",
    "BrokenLinkReport",
    "BrokenLinkReportAttributes",
    "BrokenLinkReportFile",
]
