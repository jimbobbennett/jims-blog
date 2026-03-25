---
author: "Jim Bennett"
date: 2026-03-23
description: "Turn Star Wars tools into an MCP server and connect your copilot as an MCP client."
draft: false
tags: ["ai", "copilot", "star wars", "dotnet", "c#", "mcp", "model context protocol", "tooling"]
title: "Build a Star Wars Copilot in C# - Lesson 5: MCP (Model Context Protocol)"
images:
  - /blogs/star-wars-copilot-lesson-5-mcp/banner.png
featured_image: banner.png
image: banner.png
---

Lesson 4 gave us tool calling inside the app.

Lesson 5 takes the next architectural step: move tools into an MCP server so they are reusable by any MCP-capable client.

## Why MCP

Without MCP, tools are often tightly embedded in one app.

With MCP:

- tools live in a separate server
- clients discover and call tools dynamically
- the same tooling can be reused across copilots, IDEs, and agents

This decoupling is huge once your tool surface grows.

## Building the MCP server

The workshop creates a separate `StarWarsMCPServer` .NET console app and wires:

- `AddMcpServer()`
- stdio transport
- tool discovery from assembly

Important implementation detail: stdio transport means logging should go to **stderr**, not stdout.

## Porting the tool

The previous `WookiepediaTool` logic becomes an MCP tool via `[McpServerTool]` in a `StarWarsTools` class.

You still keep strong natural-language descriptions because the model depends on those descriptions to choose tools correctly.

## Testing with MCP Inspector

Before integrating the copilot client, the workshop validates server behavior using the MCP Inspector:

- connect
- list tools
- run tool
- inspect responses

That "test tools independently first" pattern saves a lot of debugging pain later.

## MCP client in the copilot

Then the app switches from local in-process tools to:

- `StdioClientTransport`
- `McpClient.CreateAsync(...)`
- `ListToolsAsync()` feeding `ChatOptions.Tools`

At that point your copilot is now an MCP host/client combo and can scale by adding more servers, not more hardcoded tool wrappers.

## Suggested banner prompt

```text
A futuristic illustration of a central AI copilot console connected by glowing protocol lines to multiple external tool servers in separate modules, with a clean developer workspace aesthetic, cinematic contrast, high detail, no text, no logos.
```

## Follow along

Workshop source for this lesson: [Lesson 5 README](https://github.com/jimbobbennett/StarWarsCopilot/blob/main/5-mcp/README.md).

Next up: RAG from a structured database using an MCP tool.
