"""History models."""

from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class HistoryEntry(BaseModel):
    model_config = ConfigDict(extra="allow")

    action: Optional[str] = None
    table_name: Optional[str] = None
    message: Optional[str] = None
    change_user_id: Optional[str] = None
    row_id: Optional[int] = None
    change_timestamp: Optional[str] = None
    difference: Optional[dict[str, Any] | list[Any]] = None


HistoryAttributes = HistoryEntry

__all__ = ["HistoryAttributes", "HistoryEntry"]
