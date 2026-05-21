"""Pagination helpers and Paginator wrappers (SDK-style ergonomics)."""

from __future__ import annotations

from urllib.parse import parse_qsl, urlparse

from typing import (
    Any,
    AsyncIterator,
    Callable,
    Generic,
    Iterator,
    Mapping,
    Optional,
    TypeVar,
)

T = TypeVar("T")


def build_page_params(
    *,
    page: Optional[int] = None,
    per_page: Optional[int] = None,
    sort: Optional[str] = None,
    extra: Optional[Mapping[str, Any]] = None,
) -> dict[str, Any]:
    """Build a standard query-param dict honoring page/per_page/sort."""
    params: dict[str, Any] = {}
    if page is not None:
        params["page"] = page
    if per_page is not None:
        params["per_page"] = per_page
    if sort is not None:
        params["sort"] = sort
    if extra:
        for k, v in extra.items():
            if v is not None:
                params[k] = v
    return params


# ---------------------------------------------------------------------------
# Paginator — the primary list-endpoint return type
# ---------------------------------------------------------------------------


class _PaginatorBase(Generic[T]):
    """Common state for sync/async Paginators."""

    def __init__(
        self,
        *,
        path: str,
        params: Mapping[str, Any],
        document_cls: Any,
        transform: Optional[Callable[[Any], T]] = None,
    ) -> None:
        self._path = path
        self._params: dict[str, Any] = dict(params)
        self._document_cls = document_cls
        self._transform = transform
        self._current: Any = None  # validated Document instance
        self._items: list[T] = []

    # ----- accessors mirroring the underlying Document -----
    @property
    def items(self) -> list[T]:
        """Typed entities on the current page."""
        return self._items

    @property
    def data(self) -> list[T]:
        """Backward-compatible alias for :attr:`items`."""
        return self.items

    def _build_items(self) -> list[T]:
        if self._current is None or self._current.data is None:
            return []
        raw_items = list(self._current.data)
        if self._transform is None:
            return raw_items
        return [self._transform(item) for item in raw_items]

    @property
    def meta(self) -> Any:
        return None if self._current is None else self._current.meta

    @property
    def links(self) -> Any:
        return None if self._current is None else self._current.links

    @property
    def total(self) -> Optional[int]:
        m = self.meta
        return getattr(m, "count", None) if m is not None else None

    @property
    def raw(self) -> Any:
        """The full underlying ``Document`` for the current page."""
        return self._current

    @property
    def page_number(self) -> int:
        return int(self._params.get("page", 1) or 1)

    def has_next(self) -> bool:
        if self._current is None or self._current.links is None:
            return False
        return bool(self._current.links.next)

    @property
    def next_page_url(self) -> Optional[str]:
        """URL advertised by the API for the next page, if one exists."""
        if self._current is None or self._current.links is None:
            return None
        return self._current.links.next

    def _next_page_request(self) -> tuple[str, dict[str, Any]] | None:
        if not self.has_next():
            return None
        next_url = self._current.links.next
        parsed = urlparse(next_url)
        path = parsed.path or self._path
        params = dict(parse_qsl(parsed.query, keep_blank_values=True))
        if not params:
            params = dict(self._params)
            params["page"] = self.page_number + 1
        return path, params

    # ----- container protocol on the CURRENT page -----
    def __len__(self) -> int:
        return len(self.items)

    def __getitem__(self, index: int) -> T:
        return self.items[index]

    def __iter__(self) -> Iterator[T]:
        return iter(self.items)

    def __repr__(self) -> str:  # pragma: no cover - cosmetic
        return (
            f"<Paginator path={self._path!r} page={self.page_number} "
            f"items={len(self.items)} total={self.total}>"
        )


class Paginator(_PaginatorBase[T]):
    """Synchronous paginator. Iterating it yields entities on the current page."""

    def __init__(
        self,
        *,
        http: Any,
        path: str,
        params: Mapping[str, Any],
        document_cls: Any,
        transform: Optional[Callable[[Any], T]] = None,
    ) -> None:
        super().__init__(
            path=path, params=params, document_cls=document_cls, transform=transform
        )
        self._http = http
        self._load(self._params)

    def _load(self, params: Mapping[str, Any]) -> None:
        raw = self._http.get(self._path, params=params)
        self._current = self._document_cls.model_validate(raw)
        self._items = self._build_items()

    def next_page(self) -> bool:
        """Advance to the next page in place. Returns False at the last page."""
        request = self._next_page_request()
        if request is None:
            return False
        self._path, self._params = request
        self._load(self._params)
        return True

class AsyncPaginator(_PaginatorBase[T]):
    """Asynchronous paginator.

    Construct via :meth:`create` (the first page fetch must be awaited).
    Use ``async for entity in paginator`` for the current page.
    """

    def __init__(
        self,
        *,
        http: Any,
        path: str,
        params: Mapping[str, Any],
        document_cls: Any,
        transform: Optional[Callable[[Any], T]] = None,
    ) -> None:
        super().__init__(
            path=path, params=params, document_cls=document_cls, transform=transform
        )
        self._http = http

    @classmethod
    async def create(
        cls,
        *,
        http: Any,
        path: str,
        params: Mapping[str, Any],
        document_cls: Any,
        transform: Optional[Callable[[Any], T]] = None,
    ) -> "AsyncPaginator[T]":
        self = cls(
            http=http,
            path=path,
            params=params,
            document_cls=document_cls,
            transform=transform,
        )
        await self._load(self._params)
        return self

    async def _load(self, params: Mapping[str, Any]) -> None:
        raw = await self._http.get(self._path, params=params)
        self._current = self._document_cls.model_validate(raw)
        self._items = self._build_items()

    async def next_page(self) -> bool:
        request = self._next_page_request()
        if request is None:
            return False
        self._path, self._params = request
        await self._load(self._params)
        return True

    def __aiter__(self) -> AsyncIterator[T]:
        async def _gen() -> AsyncIterator[T]:
            for item in self.items:
                yield item

        return _gen()

