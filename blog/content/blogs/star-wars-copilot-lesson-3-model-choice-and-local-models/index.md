---
author: "Jim Bennett"
date: 2026-03-23
description: "Swap LLM providers in C# using Microsoft.Extensions.AI, including Azure AI Inference and Foundry Local."
draft: false
tags: ["ai", "copilot", "star wars", "dotnet", "c#", "microsoft.extensions.ai", "foundry local", "azure ai inference"]
title: "Build a Star Wars Copilot in C# - Lesson 3: Model Choice and Local Models"
images:
  - /blogs/star-wars-copilot-lesson-3-model-choice-and-local-models/banner.png
featured_image: banner.png
image: banner.png
---

One of the biggest advantages of the architecture so far is that we're coding against `IChatClient`, not one provider-specific API.

That pays off in lesson 3: we switch models and runtimes with minimal app changes.

## Why model choice matters

Different models have different:

- latency
- capability
- cost
- output style
- tool-calling behavior

If your app is tightly coupled to one SDK, experimentation gets expensive (in both money and effort).

Using `Microsoft.Extensions.AI` gives a single abstraction so you can plug in different model backends.

## Azure AI Inference SDK

First swap: Azure OpenAI -> Azure AI Inference.

The workshop adds:

- `Azure.AI.Inference`
- `Microsoft.Extensions.AI.AzureAIInference`
- extra secrets for inference endpoint/model

Then creates an inference-backed `IChatClient` with `ChatCompletionsClient(...).AsIChatClient(...)`.

Everything else stays mostly the same because the app talks to `IChatClient`.

## Foundry Local

Second swap: cloud model -> local model (Phi-4-mini via Foundry Local).

This path uses:

- `Microsoft.AI.Foundry.Local`
- `OpenAI` SDK
- local model startup via `FoundryLocalManager.StartModelAsync(...)`

The practical outcome is great for demos and offline workflows: you can run the same copilot app without internet once the model is available locally.

## The architecture takeaway

This lesson is less about syntax and more about design:

- keep app logic model-agnostic
- isolate config and model wiring
- make provider swaps a startup concern, not a full rewrite

That design makes future lessons (tools, MCP, agents) much easier.

## Suggested banner prompt

```text
A split-scene sci-fi illustration: left side cloud datacenter with holographic LLM nodes, right side a local workstation running an AI model, both feeding the same glowing chat interface in the center. Cinematic lighting, clean composition, high detail, no text, no logos.
```

## Follow along

Workshop source for this lesson: [Lesson 3 README](https://github.com/jimbobbennett/StarWarsCopilot/blob/main/3-llm-choice/README.md).

Next up: tool calling so the model can go beyond its training data.
