---
author: "Jim Bennett"
date: 2026-03-23
description: "Add chat history and a system prompt to give your C# copilot memory, tone, and behavior."
draft: false
tags: ["ai", "copilot", "star wars", "dotnet", "c#", "prompt engineering", "chat history"]
title: "Build a Star Wars Copilot in C# - Lesson 2: Chat History and System Prompts"
images:
  - /blogs/star-wars-copilot-lesson-2-chat-history-and-system-prompts/banner.png
featured_image: banner.png
image: banner.png
---

In [lesson 1](/blogs/star-wars-copilot-lesson-1-chat-with-an-llm/), we got basic prompt/response working.

Now we make it feel like an actual copilot by adding:

- chat history
- message roles
- a system prompt

This is where things get fun.

## Why follow-up questions failed

LLMs don't "remember" by default. Every call is stateless unless you pass prior messages.

So in lesson 2 we move from:

```cs
await chatClient.GetResponseAsync(userInput);
```

to:

```cs
await chatClient.GetResponseAsync(history);
```

where `history` includes both user and assistant messages.

## Build chat memory

We start with:

```cs
var history = new List<ChatMessage>();
```

Then for each turn:

1. add user message to history
1. get model response using full history
1. add assistant response back to history

That loop gives continuity so "What is the worst?" can refer to the previous question.

## Message roles matter

By this point we have two roles:

- `User`
- `Assistant`

Then we add a third:

- `System`

System messages are the highest-priority behavior instructions. This is where tone, format rules, and constraints live.

## System prompt: from generic bot to Star Wars copilot

The workshop evolves the prompt to:

- keep responses concise (optional)
- answer in Yoda style
- warn about the dark side
- respond to "hello there" with only "General Kenobi!"

It sounds playful (because it is), but this is a great pattern for real apps: keep core behavior in one explicit, testable prompt.

## Tradeoff: memory vs tokens

Sending history improves quality, but increases token usage and cost.

That tradeoff is unavoidable in chat apps. The practical takeaway: keep enough context for quality, but not so much that costs or latency spike unnecessarily.

## Suggested banner prompt

```text
A stylized sci-fi scene showing layered chat bubbles orbiting around a glowing holographic AI mentor in a spaceship command room, one bubble labeled by icon only for system rules, one for user, one for assistant. Warm cinematic lighting, high detail, no text, no logos.
```

## Follow along

Workshop source for this lesson: [Lesson 2 README](https://github.com/jimbobbennett/StarWarsCopilot/blob/main/2-chat-history-and-message-roles/README.md).

Next up: swapping model providers, including local models with Foundry Local.
