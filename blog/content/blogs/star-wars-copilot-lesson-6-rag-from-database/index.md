---
author: "Jim Bennett"
date: 2026-03-23
description: "Use retrieval-augmented generation (RAG) with Azure Table Storage to answer Star Wars order questions."
draft: false
tags: ["ai", "copilot", "star wars", "dotnet", "c#", "rag", "azure table storage", "mcp"]
title: "Build a Star Wars Copilot in C# - Lesson 6: RAG from a Database"
images:
  - /blogs/star-wars-copilot-lesson-6-rag-from-database/banner.png
featured_image: banner.png
image: banner.png
---

By lesson 6, we already have an MCP server and client working.

Now we add a classic enterprise use case: retrieval from structured business data.

## What this lesson adds

A new MCP tool (`StarWarsPurchaseTool`) that queries Azure Table Storage to retrieve figurine order data.

The model can then answer questions like:

- what was in order 66?
- what did Ben Smith purchase?
- show orders for a specific character

## RAG is broader than document search

A lot of people hear "RAG" and think vector DB + embeddings.

This lesson is a good reminder that RAG simply means augmenting generation with retrieved data, and that retrieval source can be:

- relational/NoSQL tables
- APIs
- docs
- search systems

Here it's plain table queries plus deterministic filtering logic.

## Data shape and tool design

The workshop uses three tables:

- `Figurines`
- `Orders`
- `OrderFigurines`

The tool accepts optional filters:

- `orderNumber`
- `characterName`
- `customerName`

Then combines data into a JSON payload the model can reason over.

This is exactly the pattern I like for production tools: perform strict filtering in code, let the model focus on explanation and narrative.

## Practical implementation notes

The lesson adds:

- `Azure.Data.Tables` package
- helper functions for query composition
- explicit error responses for bad inputs / no matches

The case-sensitive lookup note in the workshop is also an important real-world reminder: retrieval quality starts with query normalization rules.

## Suggested banner prompt

```text
A high-detail sci-fi data-vault scene with holographic tables of orders and figurines floating above a console while an AI assistant correlates records into a clear response stream. Cool cyan and purple palette, cinematic lighting, no text, no logos.
```

## Follow along

Workshop source for this lesson: [Lesson 6 README](https://github.com/jimbobbennett/StarWarsCopilot/blob/main/6-rag/README.md).

Next up: multi-modal AI with image generation tools.
