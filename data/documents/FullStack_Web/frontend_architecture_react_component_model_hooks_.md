# Frontend Architecture: React Component Model, Hooks, Virtual DOM and Streaming UI

**Category**: `fullstack_web` | **Authority Rank**: 5/5 | **Date**: 2026-11-06

## Overview & Key Concepts

React builds declarative UIs where UI = f(state). Key rules: (1) Functional components with Hooks (useState for local state, useEffect for side-effects/API lifecycle with cleanup, useMemo/useCallback to prevent expensive re-renders, useRef for mutable DOM/stream references). (2) Virtual DOM reconciliation diffs component trees in O(N) using unique key props on lists. (3) For AI/LLM Full-Stack apps, connect React to backend streaming endpoints via Fetch ReadableStream or Server-Sent Events (SSE) for real-time token rendering.

## Connected GraphRAG Entities

- `React_Frontend`
- `REST_SSE_WebSockets_API`
