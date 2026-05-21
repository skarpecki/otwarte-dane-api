"""Institution models."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class InstitutionSource(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    title: str | None = None
    url: str | None = None
    type: str | None = None


class Institution(BaseModel):
    model_config = ConfigDict(extra="allow")

    title: str | None = None
    slug: str | None = None
    abbreviation: str | None = None
    regon: str | None = None
    institution_type: str | None = None
    city: str | None = None
    street: str | None = None
    street_number: str | None = None
    street_type: str | None = None
    flat_number: str | None = None
    postal_code: str | None = None
    email: str | None = None
    tel: str | None = None
    fax: str | None = None
    website: str | None = None
    epuap: str | None = None
    electronic_delivery_address: str | None = None
    image_url: str | None = None
    description: str | None = None
    notes: str | None = None
    followed: bool | None = None
    sources: list[InstitutionSource] | None = None
    created: str | None = None
    modified: str | None = None


InstitutionAttributes = Institution

__all__ = ["Institution", "InstitutionAttributes", "InstitutionSource"]
