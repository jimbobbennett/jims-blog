---
author: "Jim Bennett"
date: 2026-09-23
publishDate: 2026-09-23
description: "Compare Jev and GPT-5.4 nano for real-time LLM guardrails, with demo results on latency, cost, and checks on agent inputs, replies, and tool calls."
draft: false
slug: "llm-guardrails-jev"
title: "Real-time LLM guardrails with Jev: comparing latency and cost"
canonical: "https://arize.com/blog/llm-guardrails-jev/"
tags: ["ai", "guardrails", "llm", "agents", "slm", "evals"]

images:
  - /blogs/llm-guardrails-jev/banner.png
featured_image: banner.png
---

{{< x user="ChrisJBakke" id="1736533308849443121" >}}

In December 2023, Chris Bakke talked a Chevrolet dealership's website assistant into agreeing in chat to sell him a 2024 Tahoe for $1.00, and got it to agree the deal was ["a legally binding offer - no takesies backsies."](https://x.com/ChrisJBakke/status/1736533308849443121) The screenshot went around the internet, the dealership pulled the bot, and the story became the canonical example of what happens when you put a language model in front of your business with nothing between it and the customer.

LLM guardrails check inputs, generated replies, or proposed tool calls against application rules, then allow, flag, or block the operation. They can combine model-based checks, such as detecting an unauthorized commitment, with deterministic rules, such as rejecting a quote below an approved price.

When these checks run before an operation proceeds, they add latency to the request. This underscores an engineering problem: how do you enforce the rules within your application's latency and cost budgets?

For model-based checks, options include a general-purpose LLM judge, a fine-tuned small model, or a purpose-built decision model such as TypeSafe's Jev. This post compares Jev with OpenAI's GPT-5.4 nano in a dealership chatbot demo, measuring guardrail latency and cost across two attack sequences. We also discuss the deployment tradeoffs of fine-tuning a small model, which we did not benchmark here.

We created a demo to show guardrails with Jev, compared against LLMs. The code, attack transcripts, and measurement harness are all in the [typesafe-guardrails repo](https://github.com/jimbobbennett/typesafe-guardrails).

## How we tested Jev and GPT-5.4 nano as the LLM judge

The demo we created rebuilds the dealership: a chatbot that can quote prices and call a tool to record an offer. Except this time, we added guardrails. There are several, each screening a different boundary:

- the inbound customer message, before the agent sees it
- the draft reply, before it is sent back
- the tool arguments the agent wants to record
- a deterministic below-floor price check that needs no model at all

We run that whole set in one of three configurations:

- **No guardrail**: nothing sits between the model and the customer, so you can reproduce the original $1 Tahoe incident, albeit as a demo, not by buying an SUV for $1.
- **Jev**: a purpose-built decision model, reached through TypeSafe System One.
- **LLM-as-a-Judge**: a general model, GPT-5.4-nano, called through structured outputs. This is the baseline.

With the guardrail running, a normal purchase goes straight through, while the $1 Tahoe attack is stopped before the offer is ever recorded.

![The demo chatbot handling a normal request, where a reasonable offer is allowed through to the agent](/blogs/llm-guardrails-jev/allowed-request.png)

![The demo chatbot blocking the $1 Tahoe attack, refusing to record the below-floor offer](/blogs/llm-guardrails-jev/blocked-request.png)

Under the hood, Jev is TypeSafe AI's first "System One" model. The name is a nod to [Kahneman's "System 1" thinking](https://en.wikipedia.org/wiki/Thinking,_Fast_and_Slow): the fast, intuitive judgment you make in a single pass, as opposed to the slow, deliberate, step-by-step reasoning of System 2.

A generative LLM writing out its reasoning token by token is doing System 2 work for a job that only needs System 1. Jev is built for exactly that kind of structured, snap decision rather than open-ended generation. Instead of writing an answer token by token, it returns a typed answer with a probability distribution in a single parallel pass, which is where most of the speed comes from.

It is trained with Reinforcement Learning for Calibrated Decisions, which TypeSafe describes as training for calibrated probabilities. For more background, see [our comparison of TypeSafe Jev and LLM-as-a-Judge evaluation](https://arize.com/blog/typesafe-jev-llm-judge/).

We ran the same three-turn Tahoe attack through the Jev guardrail and the LLM-as-a-Judge guardrail, and measured two things:

- **Latency**: how long a single guardrail call takes, and how long the whole conversation takes to screen end to end.
- **Cost**: what each guardrail costs per conversation, worked out from the measured token counts against published prices.

Both engines use the same question definitions, thresholds, and decision functions. The agent's generated replies can vary between runs, however, so the engines don't necessarily evaluate identical text. These results compare the two engines in a live demo. A controlled accuracy comparison would require replaying the same labeled inputs, replies, and tool arguments through both.

![Arize AX trace of the guardrail firing on the attack, with the boundary check that blocks the $1 offer surfaced in the span tree](/blogs/llm-guardrails-jev/guardrail-ax.png)

The three-turn attack fires five separate guardrail checks: the inbound message, the draft reply, and the tool arguments across the turns.

Here is how the two engines compare across all five:

| Measure | Jev | GPT-5.4-nano |
|---|---|---|
| Median per call | 104ms | 1,915ms |
| Full attack, 5 checks | 0.7s | 9.2s |
| Token price | $0.042/M in, output free | $0.20/M in, $1.25/M out |
| Decisions | 3 allow, 1 review, 1 block | 3 allow, 1 review, 1 block |

Same questions, same thresholds, same decisions, and the same answers in 0.7 seconds instead of 9.2 seconds. On the longer slow-burn attack the per-call gap holds, 117ms against 1,811ms, and both engines reach identical verdicts on both attacks: all five boundary checks in the first, all seven in the second.

## Jev vs. GPT-5.4 nano: guardrail latency and cost

Across these two demo runs, Jev was 15-to-18x faster and 12-to-14x cheaper per call. Jev clears all five checks in 0.7 seconds where GPT-5.4-nano takes 9.2, and does it at list prices ([OpenRouter](https://openrouter.ai/) for Jev, [OpenAI](https://openai.com/api/pricing/) for GPT-5.4-nano), not negotiated rates, with identical verdicts. That reduction makes Jev worth testing against your application's latency budget and accuracy requirements.

The cost gap is structural, not a pricing quirk. Jev returns a typed distribution, so it emits far fewer output tokens, and the ones it does emit are free, while the LLM writes about three times as many output tokens at the highest per-token rate on its bill.

## Why we chose GPT-5.4 nano as the LLM judge

The easiest way to win a benchmark is to pick a weak opponent. We went the other way and picked the baseline that flatters Jev least.

We used GPT-5.4 nano as a small-model baseline with structured outputs for the guardrail decisions.

The obvious cheaper candidate, GPT-4.1-nano, disqualified itself on accuracy: asked whether a reply containing the verbatim words "and that's a legally binding offer" implied a binding commitment, it scored the claim at 0.1, near-certain that nothing binding had happened. That is the exact failure the guardrail exists to catch. The model we chose is the one that made Jev's win the narrowest.

## How the guardrail checks agent inputs, replies, and tool calls

Speed from a smaller model would be a hollow result if it came from a dumber guardrail. It does not, because the design difference is structural rather than a matter of scale.

The first difference is that Jev returns typed answers. Ask it a yes-or-no question and you get back a probability, not a sentence you have to interpret. Ask it to pick a level of risk and you get an ordered choice. The answer says what the model concluded, and the shape of the distribution says how sure it is.

Here is what Jev returns for the draft-reply boundary on the binding-offer reply, one typed answer per question:

```json
{
  "claims_binding": { "probability": 0.97 },
  "commitment": {
    "score": 2.0,
    "confidence": 0.94,
    "probabilities": {
      "no commitment, informational or a question": 0.01,
      "informal encouragement, no price agreed": 0.05,
      "states a firm price or makes a commitment": 0.94
    }
  }
}
```

`claims_binding` is a yes-or-no proposition, so the answer is simply the probability it is true. `commitment` is a graded score from 0 to 2, so it comes back with the level, a confidence read off the shape of the distribution, and the full distribution behind it. That gives the guardrail a second axis to act on.

Instead of a binary tripwire, it can allow a confident-safe turn, block a confident-unsafe one, and route the genuinely ambiguous middle to a human for review.

A high-stakes moment like a binding quote gets gated harder than an ordinary chat reply, and the confidence threshold to act on the money-moving tool is deliberately looser than the one for text because that is the call you least want to wave through.

![The three trust boundaries the guardrail screens: the inbound customer message, the agent's draft reply, and the tool arguments, each returning allow, review, or block](/blogs/llm-guardrails-jev/three-boundaries.png)

The second difference is where the guardrail sits. It checks three boundaries, not one: the inbound customer message, the draft reply before it is sent, and the arguments the agent wants to pass to a tool.

That last boundary is the one an input-only guardrail can never cover. The second attack in the repo never jailbreaks the conversation at all. Every message looks fine. The block lands only at the tool boundary, on the arguments the agent assembled to record a $1 offer. If you are only screening inbound text, you never see it.

And because each check runs in around 100ms, stacking all three boundaries on the hot path still costs the customer a fraction of a second, so you can run every guardrail on every turn without a noticeable lag. That latency headroom is what makes multiple guardrails practical rather than a luxury you ration.

The third difference is that the policy is not in the prompt. The floor price for the Tahoe LT, $54,500 against an MSRP (manufacturer's suggested retail price) of $58,195, lives in guardrail configuration and is kept out of the customer-facing agent's context. The guardrail model receives the floor price when checking a quote, while deterministic code enforces the minimum.

A deterministic below-floor check sits right alongside the model's judgment. The model handles the fuzzy question of whether a reply sounds like a binding commitment; plain arithmetic handles whether a number is below the floor. You do not need a language model to compare two numbers, and you do not want one to.

None of this is exotic. It is the difference between a model that returns structured decisions and a model that returns prose you hope to parse correctly. That difference is what lets the guardrail be small, fast, and cheap without being naive.

## Jev vs. fine-tuned small models: deployment tradeoffs

There is a legitimate middle path between a general LLM-as-judge and an off-the-shelf decision model: fine-tune your own small language model (SLM) on your own guardrail decisions.

On the one axis this post has hammered, latency, it genuinely works. A well fine-tuned small model [can run in less than 200ms on the right hardware](https://www.distillabs.ai/learn/self-hosted-vs-managed-inference/), right in Jev's range. So the SLM route is not slow. If speed were the only question, it would be a fine answer.

The catch is that speed is the cheap part, and everything around it is not. The bill for a fine-tuned SLM lands in three places, none of them the inference call:

- **The first is data, and it is the largest.** The [training compute is genuinely cheap](https://www.spheron.network/blog/how-to-fine-tune-llm-2026/), often tens or hundreds of dollars of GPU time for a small model. The expensive part is the labelled corpus you feed it: a set of allow, review, and block decisions across your whole policy, labelled well enough to trust. Data work routinely runs [40 to 60 percent of a fine-tuning project's cost](https://pricepertoken.com/fine-tuning) and into the tens of thousands of dollars on real projects.
- **The second is serving.** A fine-tune is not done when training finishes; it has to run somewhere, in production, at your latency. [Self-hosting only starts to pay off above a few billion tokens a month](https://bentoml.com/llm/getting-started/serverless-vs-self-hosted-llm-inference); below that the idle GPU time, the DevOps, and the systems engineering make it more expensive than an API, not less. Managed endpoints for a custom fine-tune bill you for uptime whether traffic shows up or not. Either way, it is a standing cost that never stops.
- **The third, and the sharpest in practice, is time to ship.** Jev works today. It is a configuration change. A fine-tuned SLM screens nothing until you have gathered the data, labelled it, run the fine-tune, and stood up serving, and only then does the guardrail go live. That delay between "we need this guardrail" and "the guardrail is running" is dead time your agent spends unprotected. And it recurs. Every new policy and every new class of attack restarts the same gather-label-train-serve cycle before the new rule can catch anything. Jev is a config change; a fine-tuned SLM is a project, and a new project every time the threat model moves.

So the argument for a purpose-built decision model over a fine-tuned SLM is not that SLMs are slow. It is that you get the same real-time latency off the shelf, per call, without the upfront data bill, the standing serving cost, or the wait.

## What to evaluate using Jev for production guardrails

Two engines, two attack sequences, identical decisions, and roughly an order of magnitude on both latency and cost.

This is not a controlled benchmark. The next step is a calibration study: a corpus of clearly-safe and genuinely-ambiguous inputs run through both engines, to test whether Jev's confidence axis stays trustworthy at the edges the way it does in these two attacks. That study is worth running, and it is not this post.

But the result does not need it. The guardrail that catches the $1 Tahoe is the one that runs on every message, every reply, and every tool call, and it can only do that if it is fast enough and cheap enough that nobody is ever tempted to turn it off. A guardrail you can afford to leave on is the only kind that protects you.

Jev is not the only purpose-built decision model you will hear about. This is a fast-growing space, and more of these small, fast classifiers are shipping all the time, each with its own claims about speed, cost, and calibration.

That is good news, but it also means the model you pick today is a decision you should keep revisiting. This is where evals earn their keep: with a labelled set of your own guardrail decisions, you can measure each new model on your traffic instead of taking the benchmark on faith, and swap in a better one the moment the numbers say so.

The guardrail stays on the whole time, and the choice of what powers it becomes something you test rather than something you guess.
