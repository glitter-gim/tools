"""
reqtrace.types Docstring
"""
from dataclasses import dataclass
from typing import Any

@dataclass
class Hop:
    index: int
    url: str
    method: str
    status: int | None
    duration_ms: int
    redirect_to: str | None
    content_type: str | None
    content_length: int | None
    headers: dict[str, str]
    set_cookies: list[str]
    error: str | None

@dataclass
class Result:
    ok: bool
    start_url: str
    final_url: str
    redirect_limit: int
    total_duration_ms: int
    hops: list[Hop]
    warnings: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "start_url": self.start_url,
            "final_url": self.final_url,
            "redirect_limit": self.redirect_limit,
            "total_duration_ms": self.total_duration_ms,
            "warnings": self.warnings,
            "hops": [
                {
                    "index": h.index,
                    "url": h.url,
                    "method": h.method,
                    "status": h.status,
                    "duration_ms": h.duration_ms,
                    "redirect_to": h.redirect_to,
                    "content_type": h.content_type,
                    "content_length": h.content_length,
                    "headers": h.headers,
                    "set_cookies": h.set_cookies,
                    "error": h.error,
                }
                for h in self.hops
            ],
        }
