# Modern Python Toolchain: uv Package Manager, Ruff Linter/Formatter, Mypy and Pre-Commit

**Category**: `devops_mlops` | **Authority Rank**: 5/5 | **Date**: 2026-11-06

## Overview & Key Concepts

Production Python project setup (from uv-guide, ruff-guide, precommit-guide): (1) uv: Rust-powered package and virtualenv manager (10x-100x faster than pip/poetry); uses pyproject.toml + deterministic uv.lock, uv sync --frozen for reproducible builds, and uv run for zero-activation execution. (2) Ruff: Replaces Flake8, Black, and isort in one Rust binary (ruff check --fix for lint rules E/F/W/I/B/UP and ruff format). (3) Mypy: Static type checker (mypy --strict, explicit_package_bases = true) catching type/None bugs before runtime. (4) Pre-commit: Git hook manager (.pre-commit-config.yaml) running ruff, mypy, check-yaml, and trailing-whitespace before every git commit.

## Connected GraphRAG Entities

- `FastAPI_Backend`
- `UV_Ruff_PreCommit_Toolchain`
