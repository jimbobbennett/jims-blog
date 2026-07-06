---
author: "Jim Bennett"
date: 2026-07-06
publishDate: 2026-07-06
description: "Ask most people what an eval is for and they'll say testing - checking the app works before you ship it. That's one job out of three. Evals also monitor live traffic and act as guardrails in the request path, and they're not interchangeable."
draft: false
slug: "three-jobs-evals-do"
title: "Evals do three jobs, not one"
tags: ["ai", "evals", "llm", "observability"]

images:
  - /blogs/three-jobs-evals-do/banner.png
featured_image: banner.png
---

Ask most people what an eval is for and you'll get some version of "testing". You run it before you ship to check the app works, like a unit test. That's true, and it's also about a third of the story.

Evals do three different jobs, and the testing one is just the first. The same basic machinery - judge an output, score it - gets pointed at three completely different problems depending on *when* it runs and *what happens next* with the result. Treat all three as "testing" and you'll under-use the other two, which is where a lot of the value actually is.

![Infographic: the three jobs evals do - pre-release testing, production monitoring, and inline guardrails](/blogs/three-jobs-evals-do/banner.png)

*Want it to hand? [Download the infographic as a PDF](/blogs/three-jobs-evals-do/infographic.pdf).*

The three run left to right from *before release* to *in production*. The eval itself can be near enough identical across all three - same prompt, same judge. What changes is where it sits in the lifecycle and what you do with the score. That's the bit worth getting straight.

## Pre-release testing

This is the one everyone already knows. Before you ship, you run your evals over a golden dataset and check the scores clear the bar. It's eval-driven development, and it works exactly like the unit tests you already write, just with a fuzzier kind of assertion at the end.

The value here is the same value tests have always had: you catch the regression while it's cheap. A prompt change that quietly broke the tone of every reply, a model upgrade that made answers less grounded - you find it on your own dataset, before a single user is exposed to it. It's the cheapest possible place to catch a problem, because the only thing that's been harmed is a test run.

## Production monitoring

Here's where it gets interesting, and where most teams stop too early. Once the app is live, the evals don't retire. They keep running, scoring real traffic as it flows through.

This matters because real users don't behave like your test set. They ask things you never thought of, in combinations you never tried, and the world drifts out from under your carefully tuned golden dataset the moment you ship. Pre-release testing tells you the app worked on the inputs *you* imagined. Monitoring tells you whether it's working on the inputs *users actually bring*, right now. You score live traffic continuously and you alert when quality drops, so you find out a model's having a bad day from a dashboard rather than from an angry post going round. Same eval as the testing step, pointed at production instead of a fixed dataset.

## Inline guardrails

The third job is the most aggressive. Here the eval runs *inside* the request path, checking a response in real time before it's allowed out the door. And critically, the score doesn't just get logged - it gets acted on, immediately.

If the check fails, you can block the response, regenerate it, or fall back to something safe, all before the user sees a thing. This is the eval as a bouncer rather than an auditor. The trade-off is that it has to be fast and it has to be cheap, because now it's sitting in the critical path of every single request, adding latency to real user traffic. So you reserve guardrails for the things that genuinely can't be allowed through - leaking personal data, going wildly off-topic, saying something unsafe - rather than every quality nicety you'd happily check after the fact.

## Same tool, three jobs

The thing to take away is that "eval" isn't one activity. It's one tool doing three jobs, and the difference between them is timing and consequence. Pre-release, you test against a fixed set and block the release if it fails. In production, you monitor live traffic and alert if it dips. In the request path, you guard each response and act on it in real time.

Most teams build the first, occasionally build the second, and forget the third exists. But an app you can actually trust in front of real users usually needs all three - the test to ship with confidence, the monitor to know it's still working, and the guardrail to catch the things that must never get out. It's the same reason evals belong [at every stage of the lifecycle](/blogs/evals-across-the-lifecycle) and not just before launch: the work isn't done when you ship, it just changes job.
