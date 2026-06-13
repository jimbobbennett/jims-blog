---
author: "Jim Bennett"
date: 2026-06-13
publishDate: 2026-06-13
description: "There isn't one way to run an eval on your AI app - there's a spectrum, from a dead-simple code check all the way to handing the whole job to an agent. Here's how the four methods stack up, and when to reach for each."
draft: false
slug: "four-ways-to-run-evals"
title: "Four ways to run an eval, from a cheap unit test to a full-blown agent"
tags: ["ai", "evals", "llm", "observability"]

images:
  - /blogs/four-ways-to-run-evals/banner.png
featured_image: banner.png
---

Someone asked me last week how you actually run an eval on an AI app. I gave the honest answer, which is "it depends", and then watched their face do the thing faces do when you give them the honest answer. So let me give the longer version, because "it depends" is true but useless on its own.

There isn't one way to run an eval. There's a spectrum. At one end you've got a check so simple it's basically a unit test. At the other end you've got an agent crawling through your traces like a detective. And the interesting bit is the middle, which most people skip straight past.

![Infographic: four ways to run evals on a deterministic-to-agentic spectrum - Code, LLM as a judge, Code + LLM, and Harness as a judge](/blogs/four-ways-to-run-evals/banner.png)

The whole thing runs left to right from *deterministic, fast and cheap* to *agentic, flexible and powerful*. As you move right you gain intelligence and nuance, and you pay for it in speed, money, and the loss of a thing that turns out to matter a lot: determinism. Run the same check twice on the left, you get the same answer twice. Do it on the right and you're at the mercy of a model having a good day.

Here's the rule I keep coming back to, and I'll spoil the ending now: start as far left as you possibly can, and only move right when the question genuinely needs it.

## Code

The cheapest eval is just code. A function that takes the output and returns pass or fail. Did the model return valid JSON? Does the response match the schema? Is there a phone number in there shaped like a phone number? Did it come back under two seconds?

It's a unit test for your model. That's not me being reductive - that's genuinely what it is. Same tooling, same mindset, same satisfying green tick.

Code evals are fast, they're basically free, they're completely objective, and they give you the same answer every single time. The catch is they're blind to anything fuzzy. A code check can tell you the response is valid JSON. It cannot tell you the response is *rude*, or unhelpful, or confidently made up. For that you need something that can read.

But here's the thing - a huge amount of what you want to check is not fuzzy at all. Format, structure, presence of a required field, staying under a length limit. Use a code eval for every one of those, every time. Don't pay a language model to count characters.

## LLM as a judge

When the thing you're checking is genuinely subjective, you reach for an LLM as a judge. You hand a model the output and ask it to score something a human would otherwise have to score - tone, helpfulness, factual accuracy, whether the answer is actually grounded in the source you gave it.

This sounds dodgy the first time you hear it. *You're using an AI to mark an AI's homework?* Yeah, and it works better than you'd expect. A well-prompted judge lands around 85% agreement with human reviewers, which is about as often as two humans agree with *each other*. Turns out we're a noisy bunch.

The cost is real, though. Every eval is now an API call, so it's slower and you're paying per check. And a judge needs calibrating - you have to actually check it agrees with you before you trust it, which is a whole topic of its own ([I wrote about that here](/blogs/how-to-build-an-eval)).

So reserve the judge for the fuzzy stuff. The subjective questions code can't touch. Don't point it at things a regex would've nailed for free.

## Code + LLM

This is the one people skip, and it's the one I'd most like to talk you into.

Real traces are messy. A judge pointed at a raw trace has to wade through tool calls, retries, system prompts and metadata just to find the bit it's supposed to be grading. That's slow, it's expensive, and it's where judges get confused and start scoring the wrong thing.

So you do the boring part in code first. Code deterministically pulls out exactly the span you care about, parses the field you need, cleans up the input - and *then* hands that tidy little nugget to the LLM to judge. Code does the extraction, the model does the reasoning.

You get cheaper, more reliable evals out of it, because the model is only ever looking at the signal and never the noise. Think of code as the cheap pre-filter that does the donkey work before you pay for the clever bit. It's a bit more plumbing up front, but on real production traces it's the difference between a judge that works and one that quietly grades the wrong thing for a month.

## Harness as a judge

The far right of the spectrum is the new and genuinely exciting one. Instead of a single judge call, you give an agent harness - something like Claude Code - the keys to your trace data.

It pulls traces through an API or a CLI, inspects spans, follows a thread when something looks off, and uses tools to go and check. It's not answering one fixed question. It's investigating. And because it can reason across a whole trace rather than one extracted field, it can spot things you didn't think to write a check for. Point it at a pile of traces and it can even come back and *suggest* the evals you should be running.

The one hard requirement: your trace data has to be reachable. If it's all locked inside a dashboard you can only look at, the agent can't touch it and the loop stays manual. If it's available through APIs, CLIs and standard formats, the agent can just get on with it.

This is the most flexible and most powerful option by a mile. It is also the slowest, the priciest, and the least deterministic - you're handing the wheel to an agent and trusting where it drives. So it's the thing you reach for when you want to *understand* what's going wrong across your whole system, not the thing you run on every single response in production.

## So which one?

All four. That's the actual answer.

Start as far left as you can. Push everything that's deterministic into code evals, because they're free and they never lie to you. Bring in an LLM judge only for the genuinely subjective stuff code can't see. When your traces are messy - and they will be - put code in front of the judge to do the extraction. And keep a harness in your back pocket for the bigger questions, the "what's actually going wrong here" investigations that don't fit in a single check.

The mistake I see most often is reaching straight for the expensive end. Someone writes a clever LLM judge for something a three-line code check would've handled, then wonders why their eval bill looks like that. Match the method to the question. Most of your questions are cheaper than you think.

One more thing before you run off and build any of this: an eval is only worth running if you know it agrees with a human. That part deserves its own post, so [here's that post](/blogs/how-to-build-an-eval).
