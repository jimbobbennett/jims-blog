---
author: "Jim Bennett"
date: 2026-09-08
publishDate: 2026-09-08
description: "A finetuned 0.8B model beat a frontier LLM on one of Shopify's tasks. That's real, and it's not a one-off. But small only wins on narrow, high-volume tasks, you only know you won if your evals prove it on your data, and it only pays if the inference savings outrun the cost of retraining as the task drifts."
draft: true
slug: "slms-for-custom-tasks"
title: "SLMs for custom tasks: when small models beat frontier ones, and how to be sure"
tags: ["ai", "slm", "llm", "evals", "observability", "agents"]

image: /blogs/slms-for-custom-tasks/hero-3.png
featured_image: hero-3.png
---

On the first of September, Tobi Lütke, the CEO of Shopify, [posted something on X](https://x.com/tobi/status/2094808564355191249) that interested me:

{{< x user="tobi" id="2094808564355191249" >}}

The task he is referring to is called Buyer Profile. The finetuned 0.8 billion parameter model (a Qwen3.5-0.8B) scored 84.6 on their judge. The frontier model that trained it, GPT-5.6-sol at its highest setting, scored 83.0. The small model didn't just keep up, it passed its own teacher. On top of that they compressed the system prompt from 9.1K tokens down to 1.1K, an 8x cut.

This pushed throughput from 2 million profiles a day to 72 million, a 36x jump! A model roughly 0.1 percent the size of a frontier model wins on quality, and runs dramatically cheaper and faster on this one task.

![Line chart: the finetuned 0.8B student climbs from 75.3 to 84.6 across three checkpoints, crossing the prior production line at 77.2 and the teacher line at 83.0](/blogs/slms-for-custom-tasks/climb.png)

That last bit is the key here - "on this one task". The headline reads like "small models beat big models now," and that's not quite true. What's actually true is more useful and more demanding: for a narrow, high-volume task, a small finetuned model can beat a frontier model on quality, latency, and cost. But you only *know* you've won if your evals prove it on your data, and it's only *worth* it if the inference savings outrun the cost of retraining as the task drifts. Let's walk through why.

## It isn't a fluke

One vendor slide is one vendor slide. I'd not build a strategy on a single screenshot, and neither should you. The reason I take the Shopify result seriously is that it lines up with a pile of independent work that says the same thing.

Take [LoRA Land](https://oumi.ai/blog/small-fine-tuned-models-are-all-you) from Predibase. In 2024 they finetuned 310 models across 31 tasks, using base models all under 8 billion parameters. After finetuning, 6 of the 10 base models beat GPT-4 on average, and all 10 beat GPT-3.5-Turbo. The tasks were the sort of thing you actually ship: named entity recognition, SQL generation, natural language inference, that sort of stuff. And they got there with as few as around 1,000 training samples per task.

Then there's Google's [distilling step-by-step](https://research.google/blog/distilling-step-by-step-outperforming-larger-language-models-with-less-training-data-and-smaller-model-sizes/) work from back in 2023, which is basically the ancestor of what Shopify are doing. A 770 million parameter model beat a few-shot-prompted 540 billion parameter PaLM. That's a model over 700 times smaller coming out ahead. The trick was to train the small model on the reasoning the big model produced, not just the final labels. Teach it *why*, not just *what*.

The through-line across all three is the same. Take a big general model, use it to generate high quality training data for one specific task, and train a small model on that. The small model doesn't need to know everything. It needs to do one thing, and it can do that one thing brilliantly.

## Why this keeps happening to AI engineers

NVIDIA put out a paper last year with the very confident title ["Small Language Models are the Future of Agentic AI"](https://arxiv.org/abs/2506.02153). Their argument is simple once you've built an agent. Agents don't have sparkling open-ended conversations all day. They make the same narrow call, over and over: classify this, extract that, decide whether to call this tool, format this output. It's repetitive, low-variation work.

And that's exactly the shape where a small model is enough. You don't need a frontier model's general knowledge to decide whether a support ticket is about billing or shipping. You're paying for a whole library when you only ever check out one book. NVIDIA reckon swapping frontier models for small ones on these calls can cut costs anywhere from 5 to 150 times, and they point at real deployments doing it.

If you're building agents, most of what your agent does is probably a candidate for a smaller model.

## The other move: don't replace the model, route to it

There's a step before "finetune a model for this task," and it's lower risk. You don't have to bet a whole task on one finetune. You can just be smart about which model handles which call.

Think about how a multi-agent system actually works. You've got a supervisor deciding what happens next, and a bunch of sub-agents doing the actual work. There's no rule that says every one of those has to be the same model. Anthropic's Fable 5 farms tasks out to different models internally depending on the job. Models don't need to be from the same family or provider. As I write this I'm engaged in a discussion on models with an AI group, and someone has just said they like Google's Gemini as it's a cheap way to execute plans created by Fable.

You can do the same thing on purpose in your agents: put a small, fast model at the front as your router or supervisor, let it do intent detection, and only hand the genuinely hard calls to the expensive frontier model.

![Architecture diagram: all requests hit a small router doing intent detection, which sends the easy majority to a small model and the hard minority to a frontier model](/blogs/slms-for-custom-tasks/routing.png)

Most requests are easy. If a small model can catch the easy majority and pass the rest up the chain, you've cut your bill without touching quality on the hard stuff.

This is well documented with real numbers. [RouteLLM](https://www.lmsys.org/blog/2024-07-01-routellm/) from LMSYS is an open-source router that cut costs by up to 85 percent while keeping about 95 percent of GPT-4's quality on their benchmark. There's a lovely bonus for the cost argument I'll get to later: their routers generalise to new model pairs *without* retraining, so the routing layer itself stays cheap to run. NVIDIA's own [LLM Router Blueprint](https://arxiv.org/abs/2506.02153) uses a roughly 1.7 billion parameter Qwen model purely as the intent classifier sitting in front of bigger models. That's your supervisor, literally. And one documented case distilled a router down to a small model that cut routing latency from 5,000 milliseconds to 100 milliseconds while holding 92 to 96 percent precision.

The nice thing about routing is that it's an on-ramp. You get a chunk of the small-model win without committing to a full task finetune, and if you get the routing wrong you can adjust it far more cheaply than you can retrain a model. If you're going to try any of this, I'd start here.

## Catch number one: you only know you won on your data

A small model that's been finetuned or routed into a narrow lane fails in a nasty way when it goes outside of its capabilities. It fails *confidently*. When a frontier model hits something outside its comfort zone it often hedges or waffles, and you can see it. A small specialised model just gives you a crisp, wrong answer and moves on. Nothing in the output tells you it's wrong.

There's research that puts numbers on the risk. A [2025 paper](https://aclanthology.org/2025.findings-acl.1301.pdf) describes what the authors call a "small model learnability gap": below roughly 3 billion parameters, models struggle to absorb heavy chain-of-thought reasoning from a bigger teacher. Treat those thresholds as approximate, but the shape holds. It's worth noticing *why* Shopify's 0.8B model works despite being well under that line. Buyer Profile is an extraction and summarisation task, not multi-step reasoning. The task type decides whether the small model has a chance. There's also a robustness cost: narrow finetuned models can drop by something like 36 percent when the input drifts away from what they were trained on. Scale buys you generality, and when you shrink the model you're spending some of that generality.

So the only way to know a small model has actually won for you is to evaluate it on your own data, with your own judge, and to keep evaluating it as your traffic changes. This applies to routing too, and it bites harder there because a mis-route is silent. The router sends a hard query to the small model, the small model answers confidently and wrong, and unless you're scoring the router's *decisions* on real traffic, nothing ever flags it. Routing quality is itself a thing you have to measure.

This is the part people skip, and it's the part that turns a nice demo into something you can run in production. You need evals in place before you trust any of this, and monitoring in place to catch the day your task quietly drifts.

## Catch number two: the money maths

The other catch is the one that decides whether this is a good idea or a nice idea, and that's cold, hard, cash.

The savings from a small model are per call. Every time you run inference, you pay less. Lovely. But the training is not free, and here's the bit that trips people up: it's not a one-off. Tasks drift. Your product changes, your users change, the distribution of inputs moves, and the model that was brilliant in July is mediocre by November. So you retrain. And every retrain re-spends the training cost, both in model training and engineering time.

That gives you a rough break-even to reason about:

> savings per call × call volume, versus retrain cost × how often you retrain

When the left side wins, you're golden. High volume and a stable task is the dream: Shopify running 72 million profiles a day on a task that doesn't change much is exactly the case where the savings dwarf everything else. But flip it around. Low volume, or a task that drifts fast enough that you're retraining every few weeks, and the maths can easily tip the other way. At that point the frontier API you were trying to replace might genuinely be cheaper once you count the engineering and retraining, and it comes with generality thrown in for free.

![Line chart: cumulative cost against call volume. The frontier API rises steeply from zero; the finetuned SLM starts with an upfront training cost then rises slowly, with a step up each time the task drifts and forces a retrain. They cross at a break-even point](/blogs/slms-for-custom-tasks/breakeven.png)

This is also why routing is the safe first move. The router generalises without constant retraining, so you dodge most of the retraining tax while still banking the per-call savings on the easy majority of requests.

Run the numbers before you build anything. If you can't estimate your call volume and how often the task is likely to drift, you can't tell which side of the line you're on.

## So where does that leave us

The temptation with all of this is to read "0.8B beats a frontier model" and conclude that small is just better now. It isn't. Small isn't the goal. The goal is the cheapest thing that provably clears your eval bar and keeps clearing it.

Sometimes that's a finetuned 0.8B model doing 72 million calls a day. Sometimes it's a small router in front of a big model, sending the easy 90 percent to the cheap path and the hard 10 percent to the expensive one. Sometimes, if your volume is low or your task won't sit still, it's just the frontier API and you should stop trying to be clever. The model size is a consequence of the decision, not the decision itself.

What you don't get to do is guess. Every one of the wins above came with a judge score attached, and that's not a coincidence. Build the evals first. Then you'll actually know.
