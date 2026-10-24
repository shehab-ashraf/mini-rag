from functools import lru_cache
from pathlib import Path
from typing import Literal, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class ParserSettings(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    max_upload_bytes: int = Field(default=5 * 1024 * 1024, ge=1024, le=25 * 1024 * 1024)
    max_pdf_pages: int = Field(default=30, ge=1, le=200)
    max_text_chars: int = Field(default=300_000, ge=1000, le=2_000_000)
    max_chunks: int = Field(default=200, ge=1, le=2000)
    max_archive_members: int = Field(default=1000, ge=1, le=10_000)
    max_archive_bytes: int = Field(default=25_000_000, ge=1024, le=100_000_000)
    max_artifact_bytes: int = Field(default=20_000_000, ge=1024, le=100_000_000)
    do_ocr: bool = False
    do_table_structure: bool = True
    cpu_threads: int = Field(default=2, ge=1, le=8)
    document_timeout_seconds: float = Field(default=120, gt=0, le=600)
    artifacts_path: Path | None = None
    artifact_manifest_sha256: str | None = Field(default=None, pattern=r"^[0-9a-f]{64}$")


class ChunkingSettings(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    strategy: Literal["hybrid", "hierarchical"] = "hybrid"
    proxy_tokenizer: Literal["cl100k_base"] = "cl100k_base"
    proxy_max_tokens: int = Field(default=384, ge=64, le=1024)
    merge_peers: bool = True
    max_context_bytes: int = Field(default=6000, ge=256, le=12_000)
    paragraph_words: int = Field(default=180, ge=20, le=500)
    paragraph_overlap_words: int = Field(default=30, ge=0)

    @model_validator(mode="after")
    def valid_overlap(self) -> Self:
        if self.paragraph_overlap_words >= self.paragraph_words:
            raise ValueError("paragraph_overlap_words must be smaller than paragraph_words")
        return self


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="forbid",
        frozen=True,
    )

    parser: ParserSettings = Field(default_factory=ParserSettings)
    chunking: ChunkingSettings = Field(default_factory=ChunkingSettings)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
