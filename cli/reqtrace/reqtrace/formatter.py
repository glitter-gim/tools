"""
reqtrace.formatter Docstring
"""
from .types import Result

def format_text(r: Result) -> str:
    lines: list[str] = []
    lines.append(f"Start: {r.start_url}")
    lines.append(f"Final: {r.final_url}")
    lines.append(f"RedirectLimit: {r.redirect_limit}")
    lines.append(f"Total: {r.total_duration_ms}ms")
    for w in r.warnings:
        lines.append(f"Warning: {w}")
    lines.append("")

    for h in r.hops:
        lines.append(f"[{h.index}] {h.method} {h.url}")
        if h.error:
            lines.append(f"  Error: {h.error}")
            lines.append("")
            continue
        lines.append(f"  Status: {h.status}")
        lines.append(f"  Duration: {h.duration_ms}ms")
        if h.redirect_to:
            lines.append(f"  RedirectTo: {h.redirect_to}")
        if h.content_type:
            lines.append(f"  ContentType: {h.content_type}")
        if h.content_length is not None:
            lines.append(f"  ContentLength: {h.content_length}")
        if h.headers:
            lines.append("  Headers:")
            for k in sorted(h.headers.keys()):
                lines.append(f"    {k}: {h.headers[k]}")
        if h.set_cookies:
            lines.append("  Set-Cookie:")
            for c in h.set_cookies:
                lines.append(f"    {c}")
        lines.append("")
    lines.append(f"OK: {str(r.ok).lower()}")
    return "\n".join(lines)
