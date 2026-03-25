---
author: "Jim Bennett"
date: 2026-03-23
description: "Add a web-search tool to your Star Wars copilot so it can fetch current knowledge instead of hallucinating."
draft: false
tags: ["ai", "copilot", "star wars", "dotnet", "c#", "tool calling", "function calling", "tavily"]
title: "Build a Star Wars Copilot in C# - Lesson 4: Tool Calling"
images:
  - /blogs/star-wars-copilot-lesson-4-tool-calling/banner.png
featured_image: banner.png
image: banner.png
---

LLMs are smart, but they're also confidently wrong sometimes.

Lesson 4 fixes that by giving the copilot a tool to query Wookieepedia via Tavily, so answers can be grounded in external data.

## Why tools

Without tools, your copilot only knows what the model was trained on.

That leads to classic hallucinations for newer entities and events. In the workshop, asking about Kay Vess is a good example.

With tool calling, the model can:

1. request a tool call
1. receive tool results
1. produce a grounded final answer

## Building the tool

The workshop creates a `WookiepediaTool` derived from `AIFunction` and defines:

- name and natural-language description
- input JSON schema (`query`)
- return JSON schema (selected Tavily fields)
- `InvokeCoreAsync` to call Tavily search API

Then it enables function invocation middleware:

```cs
.UseFunctionInvocation()
```

and passes the tool through `ChatOptions`.

## Important mental model

The LLM does **not** execute your code directly.

It emits a function-call request message. The SDK executes the tool, appends tool output, and calls the LLM again.

So one apparent "answer" can include multiple internal messages:

- assistant function call
- tool result
- final assistant response

Understanding this makes debugging much easier.

## Prompting still matters

Even with tools registered, models can ignore them. The lesson improves reliability by nudging the system prompt:

> If you're not sure, use `WookiepediaTool`.

Small instruction, big behavior shift.

## Suggested banner prompt

```text
A cinematic digital artwork of an AI assistant in a starship briefing room reaching into a holographic web of knowledge nodes labeled by icons, retrieving verified data into a chat window. Blue and gold lighting, high detail, dynamic composition, no text, no logos.
```

## Follow along

Workshop source for this lesson: [Lesson 4 README](https://github.com/jimbobbennett/StarWarsCopilot/blob/main/4-call-tools/README.md).

Next up: moving tools into an MCP server so they become reusable across clients.
