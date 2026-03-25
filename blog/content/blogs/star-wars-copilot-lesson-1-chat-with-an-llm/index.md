---
author: "Jim Bennett"
date: 2026-03-23
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
