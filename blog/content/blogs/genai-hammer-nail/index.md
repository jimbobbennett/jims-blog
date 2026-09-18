---
author: "Jim Bennett"
date: 2026-09-21
publishDate: 2026-09-21
description: "jev looks like a shiny new decision model, but strip away the calibration and it's intent classification, a problem we solved cheaply a decade ago. Meanwhile the big vendors are retiring fast, deterministic tools like Microsoft LUIS for general LLMs and paying a token tax on every request. Match the tool to the job."
draft: false
slug: "genai-hammer-nail"
title: "When everything looks like a nail: jev, intent detection, and everything old is new again"
tags: ["ai", "llm", "intent-detection", "evals", "cost", "agents"]

image: /blogs/genai-hammer-nail/cover.png
featured_image: cover.png
---

I've been watching a small model launch bounce around my feed this week, and it sent me down a rabbit hole thinking about how we build things now, and how we did in the past. The model is called [jev](https://www.theneuron.ai/explainer-articles/typesafe-jev-system-one-models-explained/), from a company called TypeSafe, and my first reaction was "wait, didn't we already know how to do this?"

Turns out we did. We just forgot, because we've all been holding the same shiny hammer for three years.

## The model that doesn't talk

jev shipped on 15 September 2026, and TypeSafe put it in a category they're calling "System One." The pitch is simple: it doesn't generate text. You hand it a situation and a list of questions with a fixed set of allowed answers, and it hands back a typed answer for each one, with a probability attached, all in a single pass. Fraud or not fraud. Route to billing or route to support. Escalate or don't.

The numbers TypeSafe quote are eye-watering: 70 to 500ms, somewhere between 40 and 200 times faster than a general LLM doing the same job, and 40 to 400 times cheaper. Those are vendor numbers with no independent benchmarks yet, so pinch of salt. But the interesting bit isn't the speed. It's the calibration. The model is trained so that a 90% really means 90% and a 55% really means 55%, which means you can actually threshold on it. As [Laurie Voss put it](https://www.linkedin.com/pulse/typesafes-jev-change-how-we-build-ai-applications-laurie-voss-tkp7c/), *"A model that's right 95% of the time but can't tell you when it's in the other 5% can't automate anything."*

Strip away the calibration and the zero-shot flexibility, and jev is doing intent classification. Take some input, sort it into one of a fixed set of buckets, tell me how confident you are. That's a problem we solved cheaply and well over a decade ago.

## The tax nobody mentions

![Side-by-side comparison of one discrete decision answered two ways: a classifier or code is cheap, fast, deterministic and calibrated, while an LLM costs 40 to 400 times more, is slow, non-deterministic and gives no testable score.](/blogs/genai-hammer-nail/generation-tax.png)

Somewhere around 2023 we all learned that a large language model could do genuinely open-ended generation, which is the hardest trick in the box. And then, because it was right there and it was easy to call, we started pointing it at everything. Including a pile of problems that were never open-ended to begin with.

Picking which agent handles a request. That's a decision. Checking whether a response is valid JSON. That's a decision. Deciding if a support ticket is angry enough to escalate. Decision. None of these need a paragraph of generated prose. They need an answer from a small set of options, ideally with a confidence score.

When you use a text generator to make a decision, you pay for it, and right now the bill everyone is staring at is the token bill. You pay in money, because you're charged per token to produce an answer that could have been a single label, and those tokens compound fast across millions of requests. You pay in latency, because generation is slow. You pay in non-determinism, because the same input can give you a different answer tomorrow. And you get no calibration you can test, just a vibe. That's the generation tax, and we've been quietly paying it on work that never needed generation.

The odd part is how much effort the industry now pours into clawing that money back. There are whole guides on [cutting LLM costs](https://arize.com/blog/how-to-reduce-llm-costs-without-sacrificing-quality/), token-optimisation playbooks, caching layers, and at the company I work for, [Arize](https://arize.com/docs/ax/instrument/track-costs), there's now a managed [Cost Agent](https://arize.com/blog/using-managed-agents-to-optimize-llm-costs/) that reads your traces, works out which node is burning the budget, and opens a pull request to fix it. In one writeup it traced a financial assistant's spend, found the research agent was eating 72% of it, and proposed changes worth 35 to 40% of the monthly bill. That tooling is genuinely useful, and I'm glad it exists. But notice what it's telling us. We have built an industry around trimming the cost of a tool we reached for too fast, and a good slice of that spend went on decisions that never needed a generative model to begin with. The cheapest token is the one you never generate.

## The whole industry is walking the wrong way

![Two opposing currents drawn as lanes on a cost axis. The drift lane, higher runtime cost, shows Microsoft LUIS, Google Dialogflow, IBM and AWS all flowing into one big LLM. The counter-current lane, lower runtime cost, shows jev, Rasa CALM, spaCy, code evals and cheap-model routing.](/blogs/genai-hammer-nail/two-currents.png)

It's not just that individual teams reach for the LLM by reflex. The big vendors are actively retiring the right tool for the job because the hammer is more fashionable.

Microsoft has shipped managed intent detection since 2015. It was called [LUIS](https://azure.microsoft.com/en-us/blog/luis-ai-automated-machine-learning-for-custom-language-understanding/), and its whole model was intents plus entities plus a few example utterances. That is intent-detection-for-routing, sold as a service, a full decade before anyone asked GPT-4 to pick a branch. Its successor, [Conversational Language Understanding](https://learn.microsoft.com/en-us/azure/ai-services/language-service/conversational-language-understanding/overview), does the same job and Microsoft's own docs sell it as *"high-quality, deterministic intent classification."* The docs even name the exact use case, routing commands like *"stop, play, forward"* or turning lights on and off. And yet LUIS retired in October 2025, CLU is scheduled to retire in March 2029, and all new work is being pushed toward general LLM models.

It's not just Microsoft. [Google](https://docs.cloud.google.com/dialogflow/cx/docs/generative-deterministic) folded Dialogflow's classic intent engine into an LLM-driven console and sells the switch on developer velocity, less design time, while staying quiet about runtime cost and latency. IBM killed its [Natural Language Classifier](https://www.ibm.com/products/natural-language-understanding) in 2022 and pointed everyone at foundation models. AWS bolted an LLM on top of [Lex](https://docs.aws.amazon.com/lexv2/latest/dg/assisted-nlu.html), with a Bedrock model as the fallback when the classifier gets unsure.

Notice the pattern in how it's justified. The reason is almost always setup effort: less labeling, less design time, fewer training phrases to write. That's a real win. But it's a build-time win, and it gets paid for with a run-time tax, most of it in tokens, every single request, forever. The vendors are optimising the bit you do once and taxing the bit you do a million times.

## And a few people rowing the other way

So jev is interesting not because it's novel, but because of when it launched. It arrived pointing straight into that current, saying purpose-built decision models still have a place. And it's not alone.

[Rasa](https://rasa.com/nlu) built DIET, one of the canonical open-source intent classifiers, and their newer approach leans on language models for dialogue. But their actual advice is the sane one: *"Keep NLU where it is working well, and opt for language models when you need more powerful dialogue understanding."* Classify with the cheap deterministic thing, fall back to the LLM only when confidence is low. That's basically the whole argument of this post, coming from a vendor who sells both.

A developer working with [spaCy](https://biggo.com/news/202508270713_SpaCy_vs_LLMs_Debate) spent, in their words, "thousands of dollars" testing LLMs for a text classification task. Then they tried logistic regression with TF-IDF, a technique older than most of the people reading this, and it beat the LLMs for the job. Thousands of dollars to rediscover that sometimes the boring tool wins.

The same split shows up in evaluations. If you're testing your AI app, the current advice from folks like [Arize](https://arize.com/resources/llm-as-a-judge-when-should-you-use-it/) is refreshingly blunt: if you can write the pass or fail check without understanding the actual content of the response, use code. Valid JSON, right tool called, correct number of rows, under the length limit. Save the LLM-as-judge for the genuinely subjective stuff like tone and grounding. And yet the default reflex is to spin up a judge model for things a three-line assertion would nail, faster and for free.

This is the small end of the same habit, and it's where I'll admit I'm as guilty as anyone. I have, more than once, asked an agent to run `git commit` for me. A command I have typed ten thousand times. I could type it in my sleep, and instead I burned a few seconds and some tokens asking a language model to do it. It's harmless on its own, but it's the same instinct: reaching for the clever tool to do a thing my own two hands already knew how to do.

## The cheapest call is the one you route away

You don't have to choose between a language model and a classic classifier to play this game. You can play it between models.

Think about a supervisor agent. Its job is mostly routing: read the request, work out what kind of thing it is, hand it off to the right sub-agent. That is intent detection wearing a different hat. And there's no rule that says the supervisor has to be your most expensive frontier model. It can be a small, cheap model doing the discrete routing decision, and then you spend the expensive tokens only on the sub-tasks that genuinely need reasoning. Match the model to the job, the same way you'd match the tool to the job.

This is exactly how people are cutting real bills. One [writeup from Arize](https://arize.com/blog/how-i-cut-coding-agent-costs-with-model-harness-routing/) routes a coding agent so a cheaper model drives the loop and a frontier model only reviews the plan at checkpoints, taking a run from about $100 down to $15 or $20. A security scan went from an estimated $1,000 to $2,000 on a frontier model to around $100 once the work was routed by task. The line they land on is a tidy summary of this whole post: spend frontier tokens on judgment, then check the workflow still holds up. The routing decision itself, the bit that decides where each request goes, is a cheap classification. It never needed the big model.

## It's not all unicorns and rainbows with the old tools

Now, the vendors aren't stupid, and I don't want to leave you thinking classic tools always win. They don't.

The genuine advantage of a language model here is that it handles the long tail and the cold start. A classic intent classifier needs training data, and it falls over on phrasings it's never seen. An LLM will take a swing at a request nobody anticipated, with zero labeled examples, and often get it right. AWS make [exactly this point](https://docs.aws.amazon.com/lexv2/latest/dg/assisted-nlu.html): traditional NLU often lacks the data to handle out-of-band responses, and the LLM generalises. If your input is genuinely open-ended, or you have no data yet, or the job really is subjective judgement, then the LLM is the right tool and you should use it.

The failure isn't using the hammer. The hammer is brilliant. The failure is picking it up before you've looked at whether you're holding a nail.

## Pick the tool, not the trend

That's the whole thing, really. There are two currents running in opposite directions right now. One is the whole industry quietly retiring cheap, fast, deterministic tools because the general model is what everyone's excited about. The other is a handful of people, and now a model called jev, pointing out that a lot of what we do is discrete decisions that never needed a text generator.

Every LLM call you don't make is money you don't spend, latency you don't wait for, and a non-deterministic answer you don't have to debug at 2am. And when you do need a model, you can still reach for a cheaper one. So next time you reach for the model, have a look at the problem first. If it's a nail, there are cheaper, faster, more reliable ways to hit it. Some of them have been sitting in the toolbox for over a decade.
