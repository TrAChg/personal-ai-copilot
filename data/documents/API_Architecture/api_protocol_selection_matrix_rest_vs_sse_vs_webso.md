# API Protocol Selection Matrix: REST vs. SSE vs. WebSockets vs. gRPC vs. MCP

**Category**: `api_architecture` | **Authority Rank**: 5/5 | **Date**: 2026-11-06

## Overview & Key Concepts

Protocol choice by communication pattern: (1) REST (HTTP/JSON): Stateless CRUD over resource nouns (GET/POST/PUT/PATCH/DELETE), pagination, rate-limiting (429), and status codes (200, 201, 400, 401, 403, 404, 422, 500). (2) Server-Sent Events (SSE): Unidirectional server-to-client HTTP stream; ideal for streaming LLM tokens to React. (3) WebSockets: Bidirectional full-duplex persistent TCP channel; ideal for live chat rooms and collaborative state. (4) gRPC (Protobuf/HTTP2): High-throughput binary microservice-to-microservice RPC. (5) MCP (JSON-RPC 2.0): Standardized AI Agent-to-Tool/DB protocol (@resource, @tool, @prompt).

## Connected GraphRAG Entities

- `REST_SSE_WebSockets_API`
- `FastAPI_Backend`
