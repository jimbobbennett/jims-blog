---
author: "Jim Bennett"
date: 2026-01-27
description: "Set up Azure, Foundry, and local prerequisites so you can complete the Star Wars Copilot lesson series end-to-end."
draft: false
tags: ["ai", "copilot", "star wars", "dotnet", "azure", "azure openai", "foundry"]
title: "Build a Star Wars Copilot in C# - Lesson 0: Self-Setup"
images:
  - /blogs/star-wars-copilot-lesson-0-self-setup/banner.png
featured_image: banner.png
image: banner.png
---

This series came from a taught workshop, so some original steps assumed resources were already provisioned by an instructor.

If you're following along on your own, this lesson gets you set up so lessons 1-8 work end-to-end.

Consider this your opening crawl: over this series, you'll learn to build your own Star Wars-inspired copilot, one lesson at a time.

The workshop itself is a hands-on build where you create a Star Wars-themed copilot in C#, step by step, using modern Azure AI tooling.

**Aim:** build a production-style AI app architecture, not just a one-off chatbot demo.

**Goals:**

- start with a basic chat loop using `Microsoft.Extensions.AI`
- add memory, prompts, and model flexibility (cloud + local)
- expand with tools, MCP servers, and retrieval from data
- add multimodal image generation and agent orchestration
- finish with a reusable, composable architecture you can adapt to real workloads

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

## What you'll set up

- local dev tooling (`git`, .NET 10 SDK, optional Node.js for MCP Inspector)
- Azure OpenAI chat deployment
- optional Azure AI Inference endpoint
- Tavily API key (lesson 4)
- Azure Storage Tables + sample data (lesson 6)
- Azure OpenAI image deployment (lesson 7)

## Local tooling

Install and verify:

```bash
git --version
dotnet --version
```

For MCP Inspector in lesson 5, also install Node.js and verify:

```bash
node --version
npx --version
```

## Clone the workshop source

```bash
git clone https://github.com/jimbobbennett/StarWarsCopilot.git
cd StarWarsCopilot
```

## Azure account and cost guardrails

You'll need:

- an active Azure subscription
- permission to create Azure OpenAI and Storage resources
- a spending plan (this series uses billable services)

My recommendation:

- use a dedicated resource group for this series
- set a budget/alert on that resource group
- only deploy the models you need for the current lesson

## Azure OpenAI baseline (lesson 1)

1. Create an Azure OpenAI resource in a supported region.
1. Deploy a chat model (for example `gpt-5-mini`).
1. Copy endpoint, API key, and deployment name.

In your copilot project:

```bash
dotnet user-secrets init
dotnet user-secrets set "OpenAI:Endpoint" "https://<your-resource>.openai.azure.com"
dotnet user-secrets set "OpenAI:APIKey" "<your-api-key>"
dotnet user-secrets set "OpenAI:ModelName" "<your-chat-deployment-name>"
```

## Optional: Azure AI Inference + Foundry Local (lesson 3)

If you want to test alternative models via Azure AI Inference:

```bash
dotnet user-secrets set "AIInference:Endpoint" "https://<your-foundry-project>.services.ai.azure.com/models"
dotnet user-secrets set "AIInference:ModelName" "<your-inference-model-name>"
```

If you want local/offline execution, install Foundry Local and test:

```bash
foundry model download phi-4-mini
foundry model run phi-4-mini
```

## Tavily key (lesson 4)

Create a Tavily account and set:

```bash
dotnet user-secrets set "Tavily:ApiKey" "<your-tavily-api-key>"
```

## Azure Storage Tables (lesson 6)

Create a Storage account and set:

```bash
dotnet user-secrets set "AzureStorage:ConnectionString" "<your-storage-connection-string>"
```

Create these tables:

- `Figurines`
- `Orders`
- `OrderFigurines`

Then seed sample rows using the workshop dataloader (`6-rag/dataloader`) or Storage Explorer.

## Image deployment (lesson 7)

Deploy a GPT image model (for example `gpt-image-1` or `gpt-image-1.5`) in Azure OpenAI and set:

```bash
dotnet user-secrets set "ImageGeneration:Endpoint" "https://<your-resource>.openai.azure.com/"
dotnet user-secrets set "ImageGeneration:APIKey" "<your-api-key>"
dotnet user-secrets set "ImageGeneration:ModelName" "<your-image-deployment-name>"
```

Also worth noting: `dall-e-3` has been retired in Azure OpenAI, so use the `gpt-image-1` model family for new deployments.

## Quick readiness check

Before starting lesson 1, run:

```bash
dotnet user-secrets list
```

You should see at least:

- `OpenAI:Endpoint`
- `OpenAI:APIKey`
- `OpenAI:ModelName`

Add and verify the other secrets as you reach each lesson.

## Cleanup when you're done

To avoid surprise costs:

- delete model deployments you no longer need
- delete the workshop Storage account
- delete the workshop resource group
- rotate/revoke any API keys created for exercises

You're ready for [lesson 1](/blogs/star-wars-copilot-lesson-1-chat-with-an-llm/).

> **Note:** Original workshop repository: [jimbobbennett/StarWarsCopilot](https://github.com/jimbobbennett/StarWarsCopilot).
