---
author: "Jim Bennett"
date: 2026-03-03
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

If you're following along on your own, complete [lesson 0](/blogs/star-wars-copilot-lesson-0-self-setup/) and [lesson 4](/blogs/star-wars-copilot-lesson-4-tool-calling/) first.

Lesson 5 does not require a new Azure resource, but it does require a reliable local multi-project setup.

## Self-setup: local MCP server/client wiring

1. Keep `StarWarsCopilot` and `StarWarsMCPServer` in stable local paths.
1. In your copilot app config (`MCPServerOptions`), use an absolute `--project` path to `StarWarsMCPServer.csproj`.
1. Verify the MCP server independently before launching your copilot:

```bash
npx @modelcontextprotocol/inspector dotnet run --project /absolute/path/to/StarWarsMCPServer.csproj
```

If the inspector can list tools and run `WookiepediaTool`, your MCP server wiring is ready.

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

> **Note:** Original workshop repository: [jimbobbennett/StarWarsCopilot](https://github.com/jimbobbennett/StarWarsCopilot).
