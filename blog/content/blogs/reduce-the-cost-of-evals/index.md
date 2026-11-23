---
author: "Jim Bennett"
date: 2026-11-23T07:00:00-08:00
publishDate: 2026-11-23T07:00:00-08:00
description: "Engineers told me they'd stopped running evals because of the cost. I spent about $84 testing 8 ways to cut eval cost, from code checks and sampling to trimming traces, decision models and cheaper judges. Some came out 600x cheaper for similar accuracy."
draft: false
slug: "reduce-the-cost-of-evals"
title: "8 ways to reduce the cost of evals"
tags: ["ai", "llm", "evals", "llm-as-a-judge", "cost", "agents", "arize"]

images:
  - /blogs/reduce-the-cost-of-evals/cover.png
featured_image: cover.png
---

I was at an event last week, and spent a lot of time discussing the same objection to evals from different AI engineers. They all said evals cost too much to run, especially in these times where engineering management are becoming very cost conscious.

Some had stopped running evals against development builds, others were holding back on scoring production traffic. We all agreed that evals are important to not ship on vibes, but to ship tested, measurable changes, so I wanted to put together a guide with some ways to reduce your eval costs.

Most of what an eval costs comes from defaults: the largest judge, the whole trace as input, reasoning switched on, every trace scored. These defaults often have cheaper alternatives that hold their accuracy. Eval cost is mostly a design choice, not a fixed tax.

In this post I cover 8 ways you can reduce your eval costs. Every eval and agent is different, so review these suggestions, and see which ones will work for your use cases.

## 1. Use code where code fits

Defaulting to an LLM judge can be a quick way to rack up unnecessary costs. Some evals simply don't need a model, and every one of those that goes to a judge is paying for a judgement no one needs.

Code costs nothing to run, so the question is which evals can it handle. A good litmus test is whether two people looking at the same span with the same rubric could ever disagree on the answer. If they couldn't, [use a code evaluator](https://arize.com/docs/ax/concepts/evaluators/online-code-evaluators). Schema checks, format checks and comparisons against a known answer fall on the code side. Questions about meaning, such as whether a reply is a refusal or is concise, stay with an LLM judge. Arize AX ships [pre-built code evals](https://arize.com/docs/ax/evaluate/evaluators/code-evaluations) for the common cases, including JSON Parsable, Matches Regex and Exact Match, and you can write your own in Python.

Code also doesn't have to replace the judge. The Arize AX docs recommend [stacking the two](https://arize.com/docs/ax/concepts/evaluators/online-code-evaluators): a code check validates the shape of the output or settles the clear-cut cases, and an LLM judge scores only what's left. Two things to plan for: how you write the check matters as much as whether you use code, and code is only as good as the reference answers it compares against, so audit those first.

**From my testing.** I tried code two ways: on its own, and as a first check in front of an LLM judge.

![Cost per 1,000 evals: Math-Verify is free at 99.8% against a $3.46 judge, and a schema check in front of the judge cuts tool-call cost by 38%](/blogs/reduce-the-cost-of-evals/s1-code.png)

**Code on its own.** I graded 1,500 answers to [MATH-500](https://huggingface.co/datasets/HuggingFaceH4/MATH-500) problems against the known correct answer. [Math-Verify](https://github.com/huggingface/Math-Verify), a library that checks whether two answers are mathematically equal, was 99.8% accurate and cost nothing. Sonnet 5.5 as the judge was 99.9% accurate and cost $3.46 per 1,000.

**Code plus a judge.** I checked 890 tool calls from the [Berkeley Function Calling Leaderboard (BFCL)](https://huggingface.co/datasets/gorilla-llm/Berkeley-Function-Calling-Leaderboard), half correct and half with one thing broken. A schema check ran first and failed every call with a structural error, such as a missing argument or a wrong type. That settled 38% of calls for free. It can't tell that the user asked for Paris and the call says Lyon, so the calls that passed it went to a Sonnet 5.5 judge. Judge cost fell from $2.17 to $1.34 per 1,000, and accuracy stayed about the same, going from 96.4% to 96.5%.

How much you save depends on how much code can settle. On PII leaks, simple pattern rules settled only 18% of documents, because spotting a name or an address is mostly a judgement call. Check your scenarios and see where code fits in.

## 2. Reduce your eval runs by sampling production and keeping datasets small

Scoring every production trace feels thorough, but past a certain point each extra trace adds cost without adding information. The same goes for development datasets that grow without limit: a large, stale dataset costs more per experiment run and tells you less about today's traffic.

You don't need every trace to know your pass rate, only enough of them. Arize AX sets this with a [sampling rate](https://arize.com/docs/ax/concepts/evaluators/filters-scope-and-cadence) on each online eval task. There is an exception: for guardrail-style evals that hunt rare failures, sampling defeats the purpose. You can combine sampling with code, with a code eval on every span for the objective checks, and an LLM judge on a smaller sample of the same traffic.

In development, a few hundred examples that reflect real traffic give more signal per dollar. The Arize AX [Dataset Coverage agent](https://arize.com/docs/ax/agents/dataset-coverage-agent) compares recent production spans with a dataset and adds real spans that fill gaps, up to a size cap you set. That cap is what keeps each experiment run bounded, which matters most when experiments run as [CI/CD regression gates](https://arize.com/docs/ax/improve/ci-cd-for-automated-experiments) on every pull request.

**From my testing.** In the [RAGTruth](https://arxiv.org/abs/2401.00396) test set, 35% of responses contain a hallucination.

![Daily cost of scoring 10,000 traces with Opus 5 against a random sample of 500 with Opus 5 or Haiku 5.5](/blogs/reduce-the-cost-of-evals/s2-sampling.png)

Treat a measure like this as the true rate in your production traffic, and score a random sample of traces:

| Traces scored | Measured rate, 95% of the time | Cost with Opus 5 | Cost with Haiku 5.5 |
|---|---|---|---|
| 100 | 35% ± 9 points | $1.45 | $0.02 |
| 500 | 35% ± 4 points | $7.27 | $0.09 |
| 1,000 | 35% ± 3 points | $14.53 | $0.17 |
| 10,000 | 35% ± 1 point | $145.30 | $1.70 |

*Costs use my measured cost per 1,000 hallucination evals: $14.53 for Claude Opus 5 at high effort and $0.17 for Claude Haiku 5.5.*

The range narrows with the square root of the sample size, so every extra trace buys less. Going from 1,000 traces to 10,000 costs 10x as much and only narrows the range from ±3 points to ±1.

For a service producing 10,000 traces a day, scoring all of them with Opus costs about $145 a day. Scoring a random 500 costs about $7.27, a 20th of that, and still gives the rate to within ±4 points. Sampling and a cheaper judge multiply: 500 traces scored by Haiku cost 9 cents.

Comparing two versions needs more traces than tracking one. To catch a rise from 35% to 40% hallucinations between versions, with 95% confidence and an 80% chance of spotting it, you need about 1,500 traces per version. A 10-point rise needs about 380 per version, and a 2-point rise about 9,000. Size the sample to the smallest change you need to catch, not to your total traffic.

## 3. Evaluate at the right session, trace, or span level

An eval scoped wider than its question pays for context it never uses. Asking whether an agent picked the right tool doesn't need the whole trace, but if the eval runs at trace level, the judge reads it anyway.

The fix is to [pick the narrowest evaluation level](https://arize.com/docs/ax/concepts/evaluators/evaluation-levels) that can answer the question. A span evaluator typically sees a few hundred tokens of context, while a session evaluator can see tens of thousands.

"Did the agent pick the right tool?" is a span question. "Did the agent loop?" needs the trace. "Did the user's problem get solved?" needs the session. In Arize AX, scope is a setting on each evaluator, span, trace or session, used by [online evals on traces](https://arize.com/docs/ax/evaluate/run-evals-on-traces). [Trace and session evals](https://arize.com/docs/ax/evaluate/trace-and-session-evals) are there for the failures that only show up across a whole request or conversation. Scope decides which spans the judge sees, and the next section, trimming, decides which fields it gets.

**From my testing.** In 199 expert-labelled web-agent traces from [AgentRewardBench](https://arxiv.org/abs/2504.08942), a typical trace had 18 LLM spans.

![A span question answered from one span reads 7,700 tokens instead of 120,000 for the whole trace](/blogs/reduce-the-cost-of-evals/s3-levels.png)

One span's input was about 7,700 tokens, and all 18 were about 120,000. A span question answered from one span costs about 1/16th of the same question answered from the whole trace. A trace question answered from a code-trimmed trace needed about 5,600 tokens, 21x fewer than every raw span.

## 4. Send the judge only what it needs

A common setup maps a whole trace into the judge's prompt. In agent traces that input can be mostly noise: system prompts, tool schemas, repeated chat history and full page dumps at every step. You pay for every token of it, and the noise can make the judge worse.

The fix is to extract the fields the question needs before the judge sees anything. In Arize AX, two task settings do much of this without custom code. [Variable mapping](https://arize.com/docs/ax/concepts/evaluators/filters-scope-and-cadence) fills each template placeholder from one span attribute, so the judge gets the fields you name rather than the whole span. For trace and session evals, the [evaluator data filter](https://arize.com/docs/ax/concepts/evaluators/filters-scope-and-cadence) chooses which spans reach the prompt. Without it, every span in every qualifying session goes to the judge, including internal LLM calls, tool spans and retrieval spans, and you pay for all of them. For extraction that needs real logic, such as keeping only the final page, run your trimming code in a [remote evaluator](https://arize.com/docs/ax/evaluate/remote-evaluators) before it calls the judge. If you can't write extraction code, a cheap model can summarise the input first.

There's one rule to hold to: trim boilerplate, history and page dumps, never the evidence. A judge that can't see the evidence can't verify the claims it's checking.

**From my testing.** On AgentRewardBench, a whole trace averaged about 155,000 tokens.

![Code-trimmed agent traces cost 20x to 24x less to judge than full traces, for four judges, with the same or better accuracy](/blogs/reduce-the-cost-of-evals/s4-trimming.png)

Code that kept only the user's goal, the agent's reasoning, action and any error at each step, and the final page brought that to about 6,500.

| Judge (agent success task) | Full trace | Code-trimmed trace |
|---|---|---|
| Sonnet 5.5 | 56.0%, $154.84 | 70.0%, $6.58 |
| Haiku 5.5 | 58.5%, $15.52 | 65.5%, $0.71 |
| Kimi K3, reasoning off | 77.0%, $20.80 | 78.5%, $1.04 |
| DeepSeek V4.1 Flash, reasoning off | 69.5%, $2.44 | 75.4%, $0.11 |

Accuracy is balanced accuracy against the expert labels.

Trimming cut cost by 20x to 24x, and every judge was as accurate or more accurate at its default cutoff. The page dumps made judges reluctant to call a run a success, matching the AgentRewardBench authors' finding that more page data lowered judge performance.

## 5. Use a decision model

A generative judge writes its verdict out as text, and you pay for every output token, at the highest rate on the bill with output tokens typically 5x the cost of input tokens. For an eval with a fixed set of answers, such as pass or fail, that text adds cost and latency without adding anything.

A decision model returns a probability for each of a fixed set of options instead of generating text, so it produces no output tokens, with no output charge. Arize AX runs decision models directly as a [Decision Judge](https://arize.com/docs/ax/evaluate/decision-judge). The [JEV-as-a-Judge paper](https://arxiv.org/abs/2609.26550) found decision models strong where the verdict can be read from the text, and weaker on maths, code and multi-step logic. They suit classification-style evals such as hallucination, relevance or tone.

**From my testing.** On the hallucination task, 1,338 labelled responses from the test half of RAGTruth (the split used in [Arize's Jev-as-a-Judge benchmark](https://arize.com/blog/jev-as-a-judge/)), Jev scored 85.4% at $0.046 per 1,000.

![Jev decision model at $0.046 per 1,000 hallucination evals and 85.4% accuracy, against Opus 5 at $14.53 and 84.9%](/blogs/reduce-the-cost-of-evals/s5-decision.png)

My large-judge baseline, Claude Opus 5 at high effort, scored 84.9% at $14.53. Jev's median latency was 82 milliseconds, against 3.2 seconds for Opus. Orders of magnitude cheaper and faster, with similar accuracy.

## 6. Use a cheaper judge

Where an eval does need a generative judge, many teams default to the largest model they have, on the assumption that a larger model is a better judge. For many evals a much smaller model is close enough, at a fraction of the price.

The most direct saving is to keep the eval prompt and change the model. Switching doesn't always mean rewriting the evaluator, switch your model and test, then tune the eval prompt if needed.

Some of the gap between a small and a large judge is calibration rather than capability. A small judge can rank cases well but set its pass/fail line in the wrong place, so tune the cutoff against human labels before you write it off. And test each eval separately: a cheap judge that works on one eval tells you nothing about the next.

**From my testing.** On the hallucination task:

![Cost per 1,000 hallucination evals and accuracy for Opus 5 and four cheaper judges](/blogs/reduce-the-cost-of-evals/s6-cheaper-judge.png)

| Judge (hallucination task) | Accuracy | Cost per 1,000 evals |
|---|---|---|
| Claude Opus 5, high effort | 84.9% | $14.53 |
| Kimi K3, reasoning off | 85.4% | $0.44 |
| Claude Haiku 5.5 | 82.3% | $0.17 |
| DeepSeek V4.1 Flash, reasoning off | 83.1% | $0.024 |
| GPT-6 Luna | 74.6% | $0.14 |

DeepSeek V4.1 Flash, an open-weight model, came within 2 points of Opus for about 1/600th of the cost. It held up elsewhere too: 95.6% on tool calls for $0.018 per 1,000, against Claude Sonnet 5.5's 96.4% for $2.17.

Haiku 5.5 ranked cases almost as well as Opus but flagged too many responses at its default cutoff. Tuning that cutoff against human labels, with two-fold cross-validation, lifted Haiku to 86.3%, level with Opus at about 1% of the cost.

GPT-6 Luna shows why each eval needs its own test: it was among the best on tool calls (96.5%) and maths (99.9%), and 10 points behind Opus on hallucination.

## 7. Change how you call the judge

Even with the right judge, the way you call it can multiply the bill. Reasoning tokens are billed as output, and output costs far more than input. A judge that thinks at length before a one-word verdict pays for an essay nobody reads. Standard real-time API pricing and repeated, uncached context add more.

Run judges with reasoning off by default, and turn it on only where a test shows it pays. If you need to keep a large judge, lower its effort setting, use the [Anthropic Message Batches API](https://docs.claude.com/en/docs/build-with-claude/batch-processing) or your provider's equivalent (half the standard rate), and turn on [prompt caching](https://docs.claude.com/en/docs/build-with-claude/prompt-caching) for the shared part of the prompt. If you run several evals over the same span, put the shared context first so it can be cached. Batch billing doesn't suit online evals, but it fits development builds, nightly suites and CI experiments: the runs the engineers at the event had stopped doing.

In Arize AX, most of these levers sit on the evaluator itself. You choose the [judge model and AI provider](https://arize.com/docs/ax/evaluate/evaluators/llm-as-a-judge) when you create the evaluator, and an [LLM override](https://arize.com/docs/ax/concepts/evaluators/filters-scope-and-cadence) on the task lets you swap in a cheaper model for one task without touching the template. The evaluator also stores [invocation parameters and whether to include explanations](https://arize.com/docs/ax/graphql-reference/guides/evaluators-and-tasks). Invocation parameters are where you set reasoning effort and output limits, for providers that expose them. Explanations are output tokens, so they're worth having while you check a new judge and worth turning off once you trust it. Batch pricing and prompt caching are different: AX calls the provider for you, so those depend on the provider. If you need batch pricing for a large offline suite, run the judge in your own code as an [experiment from the SDK](https://arize.com/docs/ax/develop/datasets-and-experiments) and log the results to AX.

Whichever settings you change, check the effect: Arize AX [shows evaluation cost](https://arize.com/docs/ax/evaluate/results-and-costs) inline for Playground runs, and through cost tracking for production tasks.

**From my testing.** DeepSeek at its lowest reasoning setting still produced about 2,000 reasoning tokens per hallucination eval, which made it dearer than Haiku.

![Lower effort, batch and caching cut Opus 5 cost 5x; turning reasoning off cuts Kimi K3 11x and DeepSeek 7x](/blogs/reduce-the-cost-of-evals/s7-calling.png)

Reasoning didn't reliably buy accuracy:

- **Hallucination:** DeepSeek fell from 83.1% to 75.5% with reasoning on, at 7x the cost. Kimi K3 went from $0.44 to $4.82 per 1,000 and lost 1.4 points.
- **Tool calls:** DeepSeek rose about a point, from 95.6% to 96.7%, and cost 3x more.
- **PII:** DeepSeek rose from 95.0% to 98.6%, catching 99.6% of leaks for $0.05 per 1,000. That matches Sonnet 5.5's 98.8% at about 1/40th of the price.

I also reran Opus 5 on the hallucination task at low effort, through the Batch API, with caching on. Cost fell from $14.53 to $3.09 per 1,000, and accuracy went from 84.9% to 86.0%. Low effort cut Opus's average output from 213 tokens to 46, because a verdict doesn't need an essay.

## 8. Escalate only when the cheap judge is unsure

Running every case through an expensive judge pays the top price for cases a cheap judge would have got right. Most cases are clear-cut. The expensive judge earns its cost only on the hard ones.

A cascade runs a cheap judge first and sends a case to an expensive judge only when the cheap judge is unsure. Code checks from section 1 can sit in front of both. This matches published work: [Trust or Escalate](https://arxiv.org/abs/2407.18370) (ICLR 2025) uses cheaper models as the first judges and escalates to stronger ones only when needed, and Arize's guide to [LLM evaluation costs](https://arize.com/resources/llm-evaluation-costs/) recommends keeping expensive judges and human review for uncertain or high-stakes cases.

The uncertainty band has to be set on data you hold out from your test set. To run escalation logic like this in Arize AX, host it as a [remote evaluator](https://arize.com/docs/ax/evaluate/remote-evaluators): you keep the scoring logic, and Arize handles orchestration, retries and writing results back to traces.

**From my testing.** On the hallucination task I ran Jev first and escalated to Opus 5 when Jev's probability fell inside a band chosen on the tuning half.

![Jev first, escalating 8% of cases, costs 10x less than Opus 5 alone with Opus and 69x less with Sonnet 5.5](/blogs/reduce-the-cost-of-evals/s8-cascade.png)

That sent 8% of cases to Opus. The cascade scored 86.8% at $1.40 per 1,000: more accurate than Opus alone, at about 1/10th of the cost. Escalating to Sonnet 5.5 instead scored 86.6% at $0.21.

## Let Arize AX find the spend

Two Arize AX agents target eval cost:

- **The** [Eval Health agent](https://arize.com/docs/ax/agents/eval-health-agent) reviews a project's evaluators every six hours. Its "Optimize eval" recommendation moves an evaluator to a cheaper judge or replaces it with a code eval: techniques 6 and 1 above. It never creates or edits an eval on its own, so each change is yours to review and apply.
- **The** [Cost Agent](https://arize.com/docs/ax/agents/cost-agent) looks for expensive models doing low-complexity work and recommends cheaper routing, with savings calculated from your span data rather than estimated. Its docs focus on application spend, but traced judge calls appear in the same data. Because the agent works from span data, set up [cost tracking](https://arize.com/docs/ax/security-and-settings/cost-tracking) early: [eval costs](https://arize.com/docs/ax/evaluate/results-and-costs) are only recorded from the point tracking is switched on, not backfilled.

## Test on your own data before you switch

The spread in results is the reason you need to test on your own data. For example, GPT-6 Luna scored 74.6% on hallucination and 99.9% on maths. Reasoning helped on PII and hurt on hallucination. Trimming improved one eval and damaged another. A result on my data is a hypothesis about yours.

The check itself is cheap. Take a few hundred examples from one eval with known answers. Run your current judge and two or three candidates: a smaller model with reasoning off, the same judge on a trimmed input, and a code check if the eval has a structural part. Compare accuracy and cost per 1,000. In my experiments that cost between a few cents and a few dollars per eval, and an [Arize AX experiment](https://arize.com/docs/ax/develop/datasets-and-experiments) keeps the results side by side.

For development and CI, the best combination in my tests was a cheap judge with reasoning off, batch billing and a small dataset that tracks production. For production, it was code checks in front of a cheap judge, a cascade for uncertain cases, trimmed inputs at the narrowest level that answers the question, and a sample of traffic rather than all of it.

The cost of an eval comes from the choices made when it was set up. Each of those choices can be measured and changed, and once the cost is known, there's no longer a reason not to run the eval.
