---
author: "Jim Bennett"
date: 2026-03-17
description: "Add a multimodal image-generation tool to your copilot and handle content policy retries safely."
draft: false
tags: ["ai", "copilot", "star wars", "dotnet", "c#", "multimodal", "image generation", "gpt-image-1", "mcp"]
title: "Build a Star Wars Copilot in C# - Lesson 7: Multimodal Image Generation"
images:
  - /blogs/star-wars-copilot-lesson-7-multimodal-image-generation/banner.png
featured_image: banner.png
image: banner.png
---

Lesson 7 brings multimodal capabilities into the stack.

Instead of only generating text, the copilot can now generate images via an MCP tool.

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

If you're following along on your own, complete [lesson 0](/blogs/star-wars-copilot-lesson-0-self-setup/) and [lesson 6](/blogs/star-wars-copilot-lesson-6-rag-from-database/) first.

This lesson adds a dedicated Azure OpenAI image deployment.

## Self-setup: deploy a GPT image model

1. In Azure OpenAI, create a deployment for a GPT image model (for example `gpt-image-1` or `gpt-image-1.5`).
1. Copy the endpoint, API key, and deployment name.
1. Save them in the MCP server project:

```bash
dotnet user-secrets set "ImageGeneration:Endpoint" "https://<your-resource>.openai.azure.com/"
dotnet user-secrets set "ImageGeneration:APIKey" "<your-api-key>"
dotnet user-secrets set "ImageGeneration:ModelName" "<your-image-deployment-name>"
```

Tip: image generation can be expensive. Set a budget and test with a small number of prompts first.

Also worth noting: `dall-e-3` has been retired in Azure OpenAI. Use `gpt-image-1` or `gpt-image-1.5` for new deployments.

## The new tool

The workshop adds `GenerateStarWarsImageTool` to the MCP server.

It:

- accepts a text description
- calls Azure OpenAI image generation with a GPT image deployment (`gpt-image-1` series)
- returns an image URL as JSON

Simple contract, high utility.

## Prompt engineering for image safety

A really useful part of this lesson is how it handles content policy issues.

The first pass prompt nudges toward:

- cartoon/parody style
- no direct copyrighted character reproduction

Then, if policy violations happen, the tool returns **actionable retry guidance** rather than a dead-end error.

That guidance tells the model to:

- replace named characters with descriptive traits
- tone down disallowed content

This is a great pattern for resilient AI systems: tools can teach the orchestrating model how to recover.

## Tightening the copilot behavior

The system prompt is updated so if a tool asks for a retry, the assistant follows that instruction and retries.

This creates a self-healing loop:

1. user asks for image
1. tool call fails with policy violation
1. tool returns remediation guidance
1. assistant rewrites prompt and retries

That is much better UX than "sorry, failed".

## Suggested banner prompt

```text
A vibrant cinematic artwork of an AI assistant projecting generated concept art panels in a starship studio, with one panel being refined into a safer descriptive prompt workflow. Retro space-opera vibe, rich colors, high detail, no text, no logos.
```

## Follow along

Workshop source for this lesson: [Lesson 7 README](https://github.com/jimbobbennett/StarWarsCopilot/blob/main/7-multimodal/README.md).

Next up: building agents and a multi-agent story + image workflow.

> **Note:** Original workshop repository: [jimbobbennett/StarWarsCopilot](https://github.com/jimbobbennett/StarWarsCopilot).
