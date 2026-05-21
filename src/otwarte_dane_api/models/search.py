"""Search endpoint models."""

from __future__ import annotations

from typing import Any

from pydantic import ConfigDict

from .common import _Base
from .dataset import Dataset
from .institution import Institution
from .resource import DataResource
from .showcase import Showcase


class SearchResultAttributes(_Base):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    title: str | None = None
    notes: str | None = None
    description: str | None = None
    slug: str | None = None
    url: str | None = None


class SearchResult(SearchResultAttributes):
    """Flattened search hit with attribute and mapping-style access."""

    id: str
    type: str

    def as_dict(self) -> dict[str, Any]:
        return self.model_dump(by_alias=False, exclude_unset=True)

    def __getitem__(self, key: str) -> Any:
        if key in self:
            return self.as_dict()[key]
        raise KeyError(key)

    def __contains__(self, key: object) -> bool:
        return isinstance(key, str) and key in self.as_dict()

    def get(self, key: str, default: Any = None) -> Any:
        return self[key] if key in self else default

    def keys(self):
        return self.as_dict().keys()

    def items(self):
        return self.as_dict().items()

    def values(self):
        return self.as_dict().values()

    def as_dataset(self) -> Dataset:
        self._ensure_type("dataset")
        return Dataset.model_validate(self.as_dict())

    def as_resource(self) -> DataResource:
        self._ensure_type("resource")
        return DataResource.model_validate(self.as_dict())

    def as_institution(self) -> Institution:
        self._ensure_type("institution")
        return Institution.model_validate(self.as_dict())

    def as_showcase(self) -> Showcase:
        self._ensure_type("showcase")
        return Showcase.model_validate(self.as_dict())

    def _ensure_type(self, expected: str) -> None:
        if self.type != expected:
            raise ValueError(f"Search result is {self.type!r}, not {expected!r}")
