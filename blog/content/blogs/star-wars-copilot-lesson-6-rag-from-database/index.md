---
author: "Jim Bennett"
date: 2026-03-10
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

## Lessons in this series

| Lesson |
|---|
| [Lesson 0: Self-Setup](/blogs/star-wars-copilot-lesson-0-self-setup/) |
| [Lesson 1: Chat with an LLM](/blogs/star-wars-copilot-lesson-1-chat-with-an-llm/) |
| [Lesson 2: Chat History and System Prompts](/blogs/star-wars-copilot-lesson-2-chat-history-and-system-prompts/) |
| [Lesson 3: Model Choice and Local Models](/blogs/star-wars-copilot-lesson-3-model-choice-and-local-models/) |
| [Lesson 4: Tool Calling](/blogs/star-wars-copilot-lesson-4-tool-calling/) |
| [Lesson 5: MCP (Model Context Protocol)](/blogs/star-wars-copilot-lesson-5-mcp/) |
| [Lesson 6: RAG from a Database](/blogs/star-wars-copilot-lesson-6-rag-from-database/) |
| [Lesson 7: Multimodal Image Generation](/blogs/star-wars-copilot-lesson-7-multimodal-image-generation/) |
| [Lesson 8: Agents and Orchestration](/blogs/star-wars-copilot-lesson-8-agents-and-orchestration/) |

## Before you start (self-setup)

If you're following along on your own, complete [lesson 0](/blogs/star-wars-copilot-lesson-0-self-setup/) and [lesson 5](/blogs/star-wars-copilot-lesson-5-mcp/) first.

This lesson introduces a new Azure dependency: Storage Tables.

## Self-setup: Azure Table Storage + seed data

1. Create a Storage account in Azure.
1. In that account, create three tables:
   - `Figurines`
   - `Orders`
   - `OrderFigurines`
1. Get a connection string and save it:

```bash
dotnet user-secrets set "AzureStorage:ConnectionString" "<your-storage-connection-string>"
```

1. Seed the data.
   - The workshop repo includes a dataloader project in `6-rag/dataloader` you can run to populate sample data.
   - If you prefer, you can insert rows manually with Storage Explorer.

Quick verification: confirm order `66` exists before testing `StarWarsPurchaseTool`.

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

> **Note:** Original workshop repository: [jimbobbennett/StarWarsCopilot](https://github.com/jimbobbennett/StarWarsCopilot).
