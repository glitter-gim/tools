"""
reqtrace.tracer Docstring
"""
import time
from urllib.parse import urlparse, urljoin

import httpx

from .types import Hop, Result

_REDIRECTS = {301, 302, 303, 307, 308}

def _normalize_url(raw: str) -> str:
    s = raw.strip()
    if not s:
        raise ValueError("URL is empty")
    if "://" not in s:
        s = "https://" + s
    u = urlparse(s)
    if u.scheme not in ("http", "https"):
        raise ValueError("URL scheme must be http or https")
    if not u.netloc:
        raise ValueError("URL host is empty")
    return s

def _resolve_location(base: str, loc: str) -> str:
    loc = loc.strip()
    if not loc:
        raise ValueError("redirect status without Location header")
    return urljoin(base, loc)

def _summarize_headers(headers: httpx.Headers) -> dict[str, str]:
    keys = [
        "date",
        "server",
        "content-type",
        "content-length",
        "location",
        "cache-control",
        "etag",
        "last-modified",
        "vary",
    ]
    out: dict[str, str] = {}
    for k in keys:
        v = headers.get(k)
        if v:
            out[k] = v
    return out

def trace(
    start_url: str,
    *,
    max_redirect: int = 10,
    timeout_sec: float = 20.0,
    include_headers: bool = False,
    include_cookies: bool = False,
    method: str = "GET",
    user_agent: str = "reqtrace/0.1",
    accept: str = "",
    referer: str = "",
    extra_headers: dict[str, str] | None = None,
) -> Result:
    url0 = _normalize_url(start_url)
    m = method.strip().upper()
    if m not in ("GET", "HEAD"):
        raise ValueError("--method must be GET or HEAD")

    headers: dict[str, str] = {"User-Agent": user_agent}
    if accept:
        headers["Accept"] = accept
    if referer:
        headers["Referer"] = referer
    if extra_headers:
        headers.update(extra_headers)

    t_start = time.monotonic()
    hops: list[Hop] = []
    warnings: list[str] = []
    final_url = url0
    ok = False

    with httpx.Client(follow_redirects=False, timeout=timeout_sec, headers=headers) as client:
        current = url0
        for i in range(max_redirect + 1):
            if i > max_redirect:
                warnings.append("redirect limit reached")
                break

            t0 = time.monotonic()
            try:
                r = client.request(m, current)
                duration_ms = int((time.monotonic() - t0) * 1000)
            except httpx.TimeoutException:
                hops.append(Hop(i, current, m, None, int((time.monotonic() - t0) * 1000), None, None, None, {}, [], "timeout"))
                break
            except httpx.HTTPError:
                hops.append(Hop(i, current, m, None, int((time.monotonic() - t0) * 1000), None, None, None, {}, [], "request_error"))
                break

            content_type = r.headers.get("content-type")
            content_length = None
            cl = r.headers.get("content-length")
            if cl and cl.isdigit():
                content_length = int(cl)

            hop_headers = dict(r.headers) if include_headers else _summarize_headers(r.headers)
            cookies = r.headers.get_list("set-cookie") if include_cookies else []

            if r.status_code in _REDIRECTS:
                loc = r.headers.get("location", "").strip()
                try:
                    next_url = _resolve_location(current, loc)
                except ValueError as e:
                    hops.append(Hop(i, current, m, r.status_code, duration_ms, None, content_type, content_length, hop_headers, cookies, str(e)))
                    break

                hops.append(Hop(i, current, m, r.status_code, duration_ms, loc, content_type, content_length, hop_headers, cookies, None))
                current = next_url
                final_url = current
                continue

            hops.append(Hop(i, current, m, r.status_code, duration_ms, None, content_type, content_length, hop_headers, cookies, None))
            ok = True
            final_url = current
            break

    total_ms = int((time.monotonic() - t_start) * 1000)
    return Result(ok, url0, final_url, max_redirect, total_ms, hops, warnings)
