"""
reqtrace.cli Docstring
"""
import json
from typing import Optional

import typer

from .formatter import format_text
from .tracer import trace

app = typer.Typer(add_completion=False)

def _parse_headers(values: Optional[list[str]]) -> dict[str, str]:
    out: dict[str, str] = {}
    if not values:
        return out
    for raw in values:
        s = raw.strip()
        if not s:
            continue
        i = s.find(":")
        if i <= 0:
            raise typer.BadParameter("invalid header, expected 'Key: Value'")
        k = s[:i].strip()
        v = s[i+1:].strip()
        if not k:
            raise typer.BadParameter("invalid header, empty key")
        out[k] = v
    return out

@app.command()
def main(
    url: str,
    max_redirect: int = typer.Option(10, "--max-redirect"),
    timeout: float = typer.Option(20.0, "--timeout"),
    headers: bool = typer.Option(False, "--headers"),
    cookies: bool = typer.Option(False, "--cookies"),
    json_out: bool = typer.Option(False, "--json"),
    method: str = typer.Option("GET", "--method"),
    user_agent: str = typer.Option("reqtrace/0.1", "--user-agent"),
    accept: str = typer.Option("", "--accept"),
    referer: str = typer.Option("", "--referer"),
    H: Optional[list[str]] = typer.Option(None, "-H"),
):
    extra = _parse_headers(H)
    r = trace(
        url,
        max_redirect=max_redirect,
        timeout_sec=timeout,
        include_headers=headers,
        include_cookies=cookies,
        method=method,
        user_agent=user_agent,
        accept=accept,
        referer=referer,
        extra_headers=extra,
    )
    if json_out:
        print(json.dumps(r.to_dict(), ensure_ascii=False))
        return
    print(format_text(r))
