---
author: "Jim Bennett"
date: 2026-03-23
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
