"""DGA endpoint models."""

from __future__ import annotations

from pydantic import ConfigDict

from .common import _Base


class DgaAggregatedResponse(_Base):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    resource_slug: str | None = None
    dataset_id: int | None = None
    resource_id: int | None = None
    dataset_slug: str | None = None
