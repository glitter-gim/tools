# reqtrace

reqtrace is a small CLI utility that traces HTTP request flows from a start URL to the final destination.

It prints each hop with status code, latency, redirect target, and key response headers. It is designed to be run periodically via systemd oneshot/timer for operator-friendly monitoring.

## Install

```bash
python -m venv .venv
. .venv/bin/activate
pip install -U pip
pip install -e .
```
