from dataclasses import dataclass
from typing import Any
from uuid import UUID


@dataclass(frozen=True)
class Chunk:
    id: str
    document_id: UUID
    location: str
    ordinal: int
    text: str
    context: str
    metadata: dict[str, Any]


@dataclass(frozen=True)
class ParsedDocument:
    chunks: tuple[Chunk, ...]
    profile: dict[str, Any]
    profile_id: str
    canonical: dict[str, Any] | None
