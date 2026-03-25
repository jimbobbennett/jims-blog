---
author: "Jim Bennett"
date: 2026-02-03
description: "Start a Star Wars Copilot in C# by connecting a console app to an LLM with Microsoft.Extensions.AI."
draft: false
tags: ["ai", "copilot", "star wars", "dotnet", "c#", "microsoft.extensions.ai", "azure openai"]
title: "Build a Star Wars Copilot in C# - Lesson 1: Chat with an LLM"
images:
  - /blogs/star-wars-copilot-lesson-1-chat-with-an-llm/banner.png
featured_image: banner.png
image: banner.png
---

I recently put together a workshop called [StarWarsCopilot](https://github.com/jimbobbennett/StarWarsCopilot), and I wanted to turn it into a proper blog series so you can follow along at your own pace.

This is lesson 1 of 8.

In this first step we build the foundation: a .NET console app that can send prompts to an LLM and print responses back to the terminal.

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

If you're following the series on your own, start with [lesson 0](/blogs/star-wars-copilot-lesson-0-self-setup/).

For this lesson specifically, you need:

- an Azure subscription with permission to create AI resources
- Azure OpenAI access in a supported region
- a deployed chat model (for example `gpt-5-mini`)
- .NET 10 SDK installed locally

## Setup notes for this lesson

1. In the Azure portal, create an **Azure OpenAI** resource.
1. Open the resource and launch **Azure AI Foundry** for that resource.
1. Deploy a chat model (for example `gpt-5-mini`).
1. Copy:
   - your Azure OpenAI endpoint (for example `https://<your-resource>.openai.azure.com`)
   - an API key
   - your deployment name (used as model name in this lesson)

Then configure your app secrets:

```bash
dotnet user-secrets init
dotnet user-secrets set "OpenAI:Endpoint" "https://<your-resource>.openai.azure.com"
dotnet user-secrets set "OpenAI:APIKey" "<your-api-key>"
dotnet user-secrets set "OpenAI:ModelName" "<your-chat-deployment-name>"
```

Quick verification:

```bash
dotnet user-secrets list
```

You should see the three `OpenAI:*` keys before moving on.

## What we're building

The app is intentionally simple:

- Read user input from the console
- Send it to a model via `IChatClient`
- Print the assistant response
- Repeat until the user exits

Under the hood this uses `Microsoft.Extensions.AI`, which gives us a clean abstraction over different model providers.

## Project setup

The workshop starts by scaffolding a console app and installing packages for:

- LLM access (`Microsoft.Extensions.AI`, `Microsoft.Extensions.AI.OpenAI`)
- Azure OpenAI connectivity (`Azure.AI.OpenAI`)
- Config and secrets (`Microsoft.Extensions.Configuration.UserSecrets`)
- Logging (`Microsoft.Extensions.Logging.Console`)

Then we store model details in user secrets:

```bash
dotnet user-secrets set "OpenAI:Endpoint" "..."
dotnet user-secrets set "OpenAI:APIKey" "..."
dotnet user-secrets set "OpenAI:ModelName" "gpt-5-mini"
```

I like this pattern because it keeps credentials out of source and makes swapping models easy later.

## Connecting to the model

The key flow is:

1. Load endpoint/key/model from configuration
1. Create `AzureOpenAIClient`
1. Convert it to `IChatClient`
1. Wrap with logging middleware
1. Call `GetResponseAsync`

That "convert to `IChatClient`" part is the important design choice. It means we can switch providers later without rewriting the entire app loop.

## First interactive loop

Once wired up, the app is basically:

```cs
while (true)
{
    Console.Write("User > ");
    var userInput = Console.ReadLine();
    if (string.IsNullOrWhiteSpace(userInput))
        break;

    var result = await chatClient.GetResponseAsync(userInput);
    Console.WriteLine("Assistant > " + result.Messages.Last()?.Text);
}
```

This gets us a working copilot quickly, with great trace visibility from logging.

## What you should notice

If you ask:

1. "What is the best Star Wars movie?"
1. "What is the worst?"

...the second answer won't understand context from the first question.

That's expected. LLMs are stateless unless **you** provide prior messages.

And that's exactly where lesson 2 goes next.

## Suggested banner prompt

```text
A cinematic, retro-futuristic illustration of a developer at a terminal in a starship cockpit, chatting with a glowing AI hologram. Neon blues and warm amber instrument lights, dramatic depth, hopeful mood, high detail, wide composition, no text, no logos.
```

## Follow along

Workshop source for this lesson: [Lesson 1 README](https://github.com/jimbobbennett/StarWarsCopilot/blob/main/1-chat-with-copilot/README.md).

Next up: chat history, message roles, and turning this into a true conversation.

> **Note:** Original workshop repository: [jimbobbennett/StarWarsCopilot](https://github.com/jimbobbennett/StarWarsCopilot).
