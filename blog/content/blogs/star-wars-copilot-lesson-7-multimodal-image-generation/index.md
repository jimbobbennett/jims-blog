---
author: "Jim Bennett"
date: 2026-03-23
description: "Add a multimodal image-generation tool to your copilot and handle content policy retries safely."
draft: false
tags: ["ai", "copilot", "star wars", "dotnet", "c#", "multimodal", "image generation", "dall-e", "mcp"]
title: "Build a Star Wars Copilot in C# - Lesson 7: Multimodal Image Generation"
images:
  - /blogs/star-wars-copilot-lesson-7-multimodal-image-generation/banner.png
featured_image: banner.png
image: banner.png
---

Lesson 7 brings multimodal capabilities into the stack.

Instead of only generating text, the copilot can now generate images via an MCP tool.

## The new tool

The workshop adds `GenerateStarWarsImageTool` to the MCP server.

It:

- accepts a text description
- calls Azure OpenAI image generation (DALL-E 3)
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
