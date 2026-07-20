---
author: "Jim Bennett"
date: 2026-07-20
publishDate: 2026-07-20
description: "Evals and observability get sold as a way to reduce risk. That's true, and it undersells them. The real return is speed: in a non-deterministic market, the team that can answer 'is this good enough to ship?' fastest is the team that gets to revenue first. Here's the case, the data, and where Arize AX fits."
draft: false
slug: "evals-are-a-speed-play"
title: "Evals Are a Revenue Strategy, Not a Safety Net"
tags: ["ai", "evals", "observability", "llm", "revenue", "arize-ax"]
featured_image: cover.png
---

Here's the moment every AI team knows. You have a demo that works. Not always, but most runs, and it's good enough that people in the room lean forward. Then someone tweaks the system prompt, or swaps the model, or adds a tool, and the question lands: did that make it better or did it quietly break something? Nobody in the room actually knows. You run it a few times by hand, it looks fine, and you ship on a shrug.

That shrug is expensive. Not because of the risk of shipping something bad, although that's real. It's expensive because the shrug is slow. Every time you can't answer "is this good enough?" quickly, you either stall while you check by hand, or you gamble. Both cost you time, and in AI right now time is the whole game.

Evals and observability usually get pitched as insurance. Put them in, sleep better, catch the embarrassing failure before your users do. That's true, and it badly undersells them. The bigger story is that the same machinery that reduces your risk is what lets you move fast, and moving fast is where the revenue is. Risk reduction is the floor. Speed is the return.

## Shipping late has a dollar price

![Paired bar chart: going 50% over budget costs 3.5% of after-tax profit, while shipping six months late costs 33% — being slow is roughly 10x more expensive than being over budget](/blogs/evals-are-a-speed-play/cost-of-late.png)

Start with the oldest finding in the book, because it still holds. Back in 1991, [Harvard Business Review laid out the math](https://hbr.org/1991/01/the-return-map-tracking-product-teams) from a McKinsey study:

> A McKinsey study reports that, on average, companies lose 33% of after-tax profit when they ship products six months late, as compared with losses of 3.5% when they overspend 50% on product development.

Going 50% over budget costs you about 3.5% of profit. Shipping six months late costs you a third of it. The market does not care what your product cost to build. It cares when it showed up. Being slow is roughly 10 times more expensive than being over budget, and that's from an era when a product cycle was measured in years.

This isn't only about launch timing. It's about the whole rhythm of shipping. The [DORA research program](https://dora.dev/research/2019/dora-report/) has spent years measuring how software teams deliver, and the teams that ship fast and often aren't just tidier engineering shops. They win on business outcomes. Elite delivery performers, DORA found, are *"twice as likely to meet or exceed their organizational performance goals"*: profitability, market share, the things a CFO actually tracks. Speed of delivery and business success turn out to be the same muscle.

## The finish line moved from "first" to "first to something that works"

It's tempting to read all that as "be first, win everything." That's not quite right, and the honest version is more useful. Being first is genuinely risky. The classic Golder and Tellis study of market pioneers put the failure rate of those pioneers at 47%. Nearly half of the companies that got somewhere first died there. First out the door is not the prize.

The prize is being first to something that actually works, and then staying ahead by improving faster than everyone else. That distinction matters more in AI than it ever did in software, because the ceiling on speed just moved. [Stripe's data on the top AI companies](https://stripe.com/blog/inside-the-growth-of-the-top-ai-companies-on-stripe) shows this cohort hit $1 million in annualized revenue in *"a median period of just 11.5 months… about 4 months ahead of the fastest-growing SaaS companies."* The fastest-growing software category in history just got beaten by four months, and the teams doing the beating are the ones iterating toward a working product fastest.

So the game isn't a one-time land grab. It's a race of iteration. Whoever can go from "idea" to "working and trustworthy" and back again, over and over, on the shortest loop, captures the revenue. Which raises the obvious question: what's actually slowing that loop down?

## Why AI teams stall between the demo and production

![Two-panel diagram: on the left, 46% of AI proof-of-concepts are scrapped before reaching production; on the right, the share of companies abandoning most AI initiatives jumps from 17% to 42% year over year](/blogs/evals-are-a-speed-play/demo-to-prod-gap.png)

The thing that kills the loop is the gap between a demo that impresses and a product you can put in front of paying users. That gap is where AI projects go to die, and the numbers are brutal. [S&P Global Market Intelligence found](https://www.ciodive.com/news/AI-project-fail-data-SPGlobal/742590/) that *"the share of companies abandoning most of their AI initiatives jumped to 42%, up from 17% last year,"* and that the average organization *"scrapped 46% of AI proof-of-concepts before they reached production."* Almost half of everything that gets built never ships.

The root cause is the thing that makes AI feel like magic in the first place: it's non-deterministic. Ask a model the same question twice and you get two different answers. That's fine for a demo and poison for a release process, because your normal safety net stops working. As [Red Hat's engineers put it](https://developers.redhat.com/articles/2026/03/23/eval-driven-development-build-evaluate-ai-agents), existing test frameworks *"don't work well for agentic systems because of inherent variability."* You can't `assert output == expected` when there's no single expected output. So the demo-to-production gap isn't a discipline problem or a talent problem. It's a measurement problem. You cannot ship what you cannot measure, and most teams have no fast way to measure a fuzzy system.

That's the real speed killer. Not that the model isn't good enough, but that you can't tell, quickly and repeatably, whether it is.

## Evals turn "is it good enough?" into a loop you can run

![Side-by-side comparison of two loops answering "is this good enough to ship?": the manual loop (change, poke by hand, afternoon gone, ship on a shrug) versus the eval loop (change, run the evals, know in minutes, ship with confidence), with the same regression check dropping from 6 hours to 20 minutes](/blogs/evals-are-a-speed-play/two-loops.png)

An eval is just a repeatable way to score your AI's output against what "good" means for your use case. A code check, or another model acting as a judge, that turns a squishy answer into something you can compare: a score, a label, a pass or a fail. Observability is the other half: tracing what your system actually did on every run, so when a score drops you can see why. Put them together and the unanswerable question from the top of this post becomes a number you can watch move.

That's the whole point, and it's worth being precise about why it's a speed win and not just a safety one. When "is this better?" is a manual check, every change costs you an afternoon of poking. When it's an eval, every change costs you a test run. You stop gambling and you stop stalling, at the same time. Anthropic's engineering team [said it plainly](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents):

> Teams without evals get bogged down in reactive loops… Teams that invest early find the opposite: development accelerates.

Development accelerates. Not "risk decreases," although it does. The team with evals ships faster because they can trust their own changes. And this shows up in real numbers, not just principle. When DoorDash built automated evals for their in-app assistant, [they cut regression testing](https://www.infoq.com/news/2026/07/doordash-ai-ask-assistant/) *"from six hours to twenty minutes."* That's the same six-hour manual check, run as an eval instead, roughly 18 times faster. Multiply that across every change a team makes in a quarter and you can see where the four-month head start comes from. The eval is the thing that lets you ask "is this good enough?" as often as you need to, instead of once, nervously, before a launch.

## Where AX fits

This is the loop [Arize AX](https://arize.com/ax/) is built for. AX is the AI engineering platform for the whole eval-driven cycle: tracing what your system actually did on every run, evaluating quality against the standards you set, running controlled experiments, and monitoring what happens once real users are hitting it. It frames the exact gap this whole post is about. As their product page puts it, *"You can build and ship at agent speed… You still can't improve at agent speed."* Building fast was never the bottleneck. Improving fast, with confidence, is.

That's the whole job of an eval tool. You turn the runs that mattered into a dataset, you score every change against it instead of poking by hand, and you run an experiment to prove a change is better *before* you ship it. Then, once you're live and the stakes are real, the same evaluators keep watching in production, so a regression sets off an alert instead of a support ticket. It's one continuous loop that shortens the distance between "I changed something" and "I know whether it worked" — first while you're building, then while you're running.

## The floor and the return

Reducing risk is the floor. Evals will absolutely catch the regression before your users do, and that's worth the price on its own. But the floor was never the interesting part. The return is that the exact same discipline, the same golden datasets, the same evaluators, the same traces, is what lets you move fast enough to win. In a market where the product is non-deterministic and the fastest iterator takes the revenue, the ability to answer "is this good enough to ship?" in minutes instead of afternoons isn't a safety feature. It's the moat.

You don't put evals in because you're worried. You put them in because you're in a hurry.
