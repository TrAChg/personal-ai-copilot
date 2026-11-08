# Containerization and CI/CD: Docker Multi-Stage Builds, Docker Compose and GitLab CI / GitHub Actions

**Category**: `devops_mlops` | **Authority Rank**: 5/5 | **Date**: 2026-11-06

## Overview & Key Concepts

Deployment and CI/CD Architecture (from gitlab-ci-guide and Project/shortest-link): (1) Docker: Multi-stage Dockerfiles (Stage 1 builder runs uv sync --frozen --no-dev or npm ci and npm run build; Stage 2 runtime copies built artifacts into python:3.11-slim or node:20-alpine as non-root user) with .dockerignore excluding .venv, node_modules, and .git. (2) Docker Compose (docker-compose.yml): Orchestrates multi-container stacks (React + Express/FastAPI + Postgres/ChromaDB/Redis) with healthchecks, volumes, and .env config. (3) GitLab CI/CD (.gitlab-ci.yml) and GitHub Actions: Automated 4-stage pipeline (lint -> test -> build -> deploy) with dependency caching so broken code never merges to main.

## Connected GraphRAG Entities

- `UV_Ruff_PreCommit_Toolchain`
- `Docker_GitLab_CICD`
