---
author: "Jim Bennett"
date: 2026-03-24
description: "Build AI agents with Microsoft Agent Framework and orchestrate a multi-agent Star Wars storytelling workflow."
draft: false
tags: ["ai", "copilot", "star wars", "dotnet", "c#", "agents", "microsoft agent framework", "orchestration"]
title: "Build a Star Wars Copilot in C# - Lesson 8: Agents and Orchestration"
images:
  - /blogs/star-wars-copilot-lesson-8-agents-and-orchestration/banner.png
featured_image: banner.png
image: banner.png
---

Final lesson, and probably my favorite.

We move from a copilot with tools to a system that also uses **agents** as composable specialists.

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

If you're following along on your own, complete [lesson 0](/blogs/star-wars-copilot-lesson-0-self-setup/) and [lesson 7](/blogs/star-wars-copilot-lesson-7-multimodal-image-generation/) first.

This lesson does not require a brand-new Azure resource, but it does add framework dependencies and orchestrates all prior components.

## Self-setup: agent dependencies and readiness checks

1. Install the Microsoft Agent Framework packages used by the workshop in your copilot project.
1. Keep package versions aligned with the workshop repo to avoid API mismatches.
1. Verify your existing resources still work before introducing agents:
   - chat model calls succeed
   - Tavily tool calls succeed
   - MCP server lists and runs tools
   - image generation tool returns URLs

Once these checks pass, add the agent orchestration code. Debugging is much easier when the underlying tools are already healthy.

## Copilot vs agent

The workshop frames agents as "LIT":

- **L**LM-powered
- **I**nstruction-driven
- **T**ool-using

Copilot is the user-facing conversational surface.

Agents are focused components that can be called by the copilot (or by other agents) to do bounded jobs.

## First agent: story creation

The initial `StoryAgent` is created with Microsoft Agent Framework and exposed as an AI tool.

This already gives a big capability jump: users can ask for tailored stories while the core copilot remains clean.

## Multi-agent workflow

Then the workshop introduces an "agents as tools" orchestration pattern:

1. `StoryAgent` creates story
1. `StorySummaryAgent` extracts scene prompts
1. `ImageGenerationAgent` uses image tool to generate visuals
1. `StoryGenerationAgent` supervises and returns story + image URLs

This is a practical orchestration pipeline, not just an abstract demo.

## Why this matters

This pattern scales well because each agent has:

- narrow responsibility
- its own instructions
- reusable interface

You can improve one agent without rewriting the whole system.

It's the same architectural principle as microservices, just in AI-native form.

## Suggested banner prompt

```text
A cinematic command-center scene with three specialized AI holograms (story writer, scene summarizer, image artist) collaborating under a supervising orchestration AI, producing a final illustrated story output. Epic space-opera style, high detail, no text, no logos.
```

## Follow along

Workshop source for this lesson: [Lesson 8 README](https://github.com/jimbobbennett/StarWarsCopilot/blob/main/8-agents/README.md).

And that's the full 8-part journey: chat, memory, model choice, tools, MCP, RAG, multimodal, and agents.

> **Note:** Original workshop repository: [jimbobbennett/StarWarsCopilot](https://github.com/jimbobbennett/StarWarsCopilot).
