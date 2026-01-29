# tools

This repository contains small, operator-focused CLI tools designed for diagnostics, inspection, and operational observability in self-hosted environments.

Each tool is intended to be simple, explicit, and usable directly on production or staging systems without additional infrastructure dependencies.

## Scope

- Lightweight command-line utilities
- Diagnostics and inspection tools for operators
- One-off or narrowly scoped operational helpers
- Minimal dependencies and predictable behavior

This repository does not aim to provide full frameworks or long-running services.

## Repository Structure

Each top-level directory represents an independent tool.

Tools are not required to share:
- Language
- Runtime
- Release cycle

They are grouped here solely for operational convenience.

## Design Principles

- Explicit over clever
- Inspectable over abstract
- Operator ergonomics over developer convenience
- Safe defaults for production environments

## Usage

Each tool directory should document:
- Purpose
- Supported environments
- Invocation examples
- Limitations or safety notes

Refer to individual tool directories for details.

## Notes

This repository is maintained for direct infrastructure operation and troubleshooting.
Stability and clarity are preferred over feature completeness.
