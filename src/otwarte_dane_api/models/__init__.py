"""Pydantic models for DANE.GOV.PL API responses."""

from .common import (
    Document,
    ErrorObject,
    ErrorSource,
    Links,
    Meta,
    Relationship,
    RelationshipRef,
    Resource,
)
from .dataset import Dataset, DatasetAttributes, DatasetCategory, DatasetSource, DatasetTag
from .dga import DgaAggregatedResponse
from .flatten import flatten_dict_resource, flatten_resource
from .history import HistoryAttributes, HistoryEntry
from .institution import Institution, InstitutionAttributes, InstitutionSource
from .report import (
    BrokenLinkEntry,
    BrokenLinkEntryAttributes,
    BrokenLinkRelatedObject,
    BrokenLinkReport,
    BrokenLinkReportAttributes,
    BrokenLinkReportFile,
)
from .resource import (
    DataResource,
    JsonApiResource,
    ResourceAttributes,
    ResourceRegion,
    ResourceSpecialSign,
    ResourceSupplement,
    ResourceTableMeta,
    TableRow,
    TableRowAttributes,
)
from .search import SearchResult, SearchResultAttributes
from .showcase import ExternalDataset, Showcase, ShowcaseAttributes

__all__ = [
    "BrokenLinkEntry",
    "BrokenLinkEntryAttributes",
    "BrokenLinkRelatedObject",
    "BrokenLinkReport",
    "BrokenLinkReportAttributes",
    "BrokenLinkReportFile",
    "DataResource",
    "Dataset",
    "DatasetAttributes",
    "DatasetCategory",
    "DatasetSource",
    "DatasetTag",
    "Document",
    "DgaAggregatedResponse",
    "ErrorObject",
    "ErrorSource",
    "ExternalDataset",
    "HistoryAttributes",
    "HistoryEntry",
    "Institution",
    "InstitutionAttributes",
    "InstitutionSource",
    "JsonApiResource",
    "Links",
    "Meta",
    "ResourceAttributes",
    "ResourceRegion",
    "ResourceSpecialSign",
    "ResourceSupplement",
    "ResourceTableMeta",
    "Relationship",
    "RelationshipRef",
    "Resource",
    "SearchResult",
    "SearchResultAttributes",
    "Showcase",
    "ShowcaseAttributes",
    "TableRow",
    "TableRowAttributes",
    "flatten_resource",
    "flatten_dict_resource",
]
