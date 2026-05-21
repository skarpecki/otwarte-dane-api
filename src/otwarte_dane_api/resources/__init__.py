"""Resource namespaces."""

from .datasets import AsyncDatasetsResource, DatasetsResource
from .dga import AsyncDgaResource, DgaResource
from .histories import AsyncHistoriesResource, HistoriesResource
from .institutions import AsyncInstitutionsResource, InstitutionsResource
from .reports import AsyncReportsResource, ReportsResource
from .resources import AsyncResourcesResource, ResourcesResource
from .search import AsyncSearchResource, SearchResource
from .showcases import AsyncShowcasesResource, ShowcasesResource

__all__ = [
    "InstitutionsResource",
    "AsyncInstitutionsResource",
    "DatasetsResource",
    "AsyncDatasetsResource",
    "ResourcesResource",
    "AsyncResourcesResource",
    "ShowcasesResource",
    "AsyncShowcasesResource",
    "HistoriesResource",
    "AsyncHistoriesResource",
    "SearchResource",
    "AsyncSearchResource",
    "DgaResource",
    "AsyncDgaResource",
    "ReportsResource",
    "AsyncReportsResource",
]
