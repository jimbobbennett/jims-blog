---
author: "Jim Bennett"
date: 2026-10-08
publishDate: 2026-10-08
description: "Eight decision models, three challenges, one knockout bracket. We ran Jev, Kev, Liquid, Clef 27B and friends on hallucination, evaluator and routing tests in Arize AX to find the next top decision model."
draft: true
slug: "arizes-next-top-decision-model"
title: "Arize's next top decision model"
tags: ["ai", "llm", "evals", "llm-as-a-judge", "decision-models", "jev", "agents"]
canonical: "https://arize.com/blog/decision-model-benchmark/"

images:
  - /blogs/arizes-next-top-decision-model/banner.png
featured_image: banner.png
hero_alt: "A glamorous host presents eight robot contestants with sashes on the runway, under a pink \"top decision model\" title"
---

*Eight decision models. Three challenges. One bracket. Only one can be Arize's next top decision model.*

On 15 September, TypeSafe [released Jev](https://www.infoq.com/news/2026/10/typesafe-ai-jev-released/), and within a few weeks about 10 companies had shipped something that works the same way. OpenAI, Liquid, Cloudflare, AWS and PostHog all launched one, and an open clone called Kev showed up on Hugging Face in between. If you build agents or run evals, you now have a casting problem.

So we held auditions.

A decision model takes a question and a fixed set of options and returns a probability for each option. It doesn't write text, so there are no output tokens to pay for or wait on. That makes it cheap and fast at two jobs AI engineers care about: making a single decision inside an agent (which tool, which skill, stop or carry on), and acting as the judge that scores your traces in [Arize AX](https://arize.com/docs/ax/evaluate/jev-as-a-judge).

We've written about Jev as a judge before. Laurie Voss [benchmarked it against LLM judges](https://arize.com/blog/jev-as-a-judge/), and Elizabeth Hutton looked at [what its probabilities reveal](https://arize.com/blog/jev-llm-judge-consistency/). Both posts compared Jev with LLMs, but we hadn't lined the new decision models up against each other on the same data. A spreadsheet of eight models is no fun to read, though, so we turned it into a knockout.

The best decision models are now level on accuracy. They differ on where you can run them, and on whether they understand the question the way you asked it.

## Meet the contestants

Eight models made it through casting. Each one arrived with a different story, as all good contestants do.

| Model | Who | Their story | Size and licence | Where we ran it | List price |
| --- | --- | --- | --- | --- | --- |
| [Jev 1.13](https://www.infoq.com/news/2026/10/typesafe-ai-jev-released/) | TypeSafe | The one who started it all. Hosted API, 32k context | Closed | [TypeSafe API](https://docs.typesafe.ai/models) | $0.042 per million input tokens, output free |
| [Liquid d1](https://www.marktechpost.com/2026/09/29/liquid-ai-releases-d1-a-decision-model-that-returns-calibrated-probabilities-with-zero-output-tokens/) | Liquid AI | First to knock Jev off the top of [Hugging Face's Decision Index](https://huggingface.co/spaces/multimodalart/jev-decision-index), 58.9 to 57.9 | Closed | [Liquid API](https://docs.liquid.ai/lfm/models/decision-models) | $0.04 per million |
| [OpenAI Decisions](https://developers.openai.com/api/docs/guides/decisions) (gpt-6-luna) | OpenAI | The first frontier lab through the door. Still in public beta | Closed | [OpenAI API](https://developers.openai.com/api/docs/guides/decisions) | $0.10 per million |
| [Clef 27B](https://blog.cloudflare.com/clef-decision-models/) | Cloudflare | Open weights, Jev-compatible API, can read images | 27B, Apache 2.0 | [Workers AI](https://developers.cloudflare.com/changelog/post/2026-10-01-clef-workers-ai/) | $0.24 per million |
| [Kev 9B](https://huggingface.co/jaredpalmer/kev-9b) | Jared Palmer | The underdog. An open Jev clone whose first training run, across three model sizes, [cost about $95 of rented GPU time](https://runtimewire.com/article/jared-palmer-kev-qwen35-decision-models) | 9B, open | Local | Free to self-host |
| [Jeeves 9B](https://huggingface.co/PostHog/jeeves) | PostHog | The overthinker. Reasons before it decides | 9B, open | Local | Free to self-host |
| [Strands Decider 2B](https://huggingface.co/StrandsAgents/strands-decider-2B-hobson-v19) | AWS | The smallest in the house, with its [training recipe published](https://siliconangle.com/2026/10/01/aws-debuts-strands-decider-2b-a-first-lightweight-decision-model-for-accelerate-agentic-workflows/) | 2B, open | Local | Free to self-host |
| [Laya multilingual](https://huggingface.co/convaiinnovations/laya) | Convai Innovations | Not even an LLM. A BERT-style encoder with an 8,192-token context | 322M, Apache 2.0 | Local | Free to self-host |

Prices are list prices per million input tokens. In the results, we turn them into cost per 1,000 decisions, using the tokens each model consumed.

Seven of the eight accept Jev's `/v1/systemone` request format. Three weeks after launch, one API has become the default way to talk to a decision model, in the same way a lot of LLM vendors support the OpenAI API.

The odd one out is, fittingly, OpenAI. The other APIs take each case as named fields, such as the context and the response, but OpenAI's [Decisions API](https://developers.openai.com/api/docs/guides/decisions) takes one block of plain text plus a list of questions. So we wrote each case out as labelled text sections, one per field, in the same order the other models saw them. We chose that layout, and a different one could score differently. Treat OpenAI's numbers as a fair first look at a public beta, and a better prompt layout might lift them.

## The rules of the house

![The bracket: eight entrants in two conferences](/blogs/arizes-next-top-decision-model/bracket-0-seeding.png)

Comparing a hosted API with a model running on a laptop isn't a fair fight on speed, so the house is split into two conferences.

- The **cloud conference** is hosted APIs, called over the network.
- The **local conference** is open models running on a MacBook Pro (Apple M4 Max, 36 GB of memory).

Each conference crowns a champion, and the two meet in the grand final.

There are three challenges, one per round:

- The quarterfinals are the hallucination challenge: 2,675 rows from RAGTruth, built with [our own benchmark code](https://github.com/Arize-ai/arize/pull/88522).
- The conference finals are the evaluator challenge: all 13 [Phoenix evaluator suites](https://github.com/Arize-ai/phoenix/tree/main/js/benchmarks/evals-benchmarks), 655 labelled cases covering hallucination, toxicity, tool use and more.
- The grand final is the agent challenge: 52 routing decisions where the model picks which tool or skill an agent should use.

The judging panel scores three things: accuracy, latency and cost per 1,000 decisions. Win two of the three and you go through. Accuracy only counts as a win when the 95% confidence intervals don't overlap; otherwise that category is a draw. Ties go to accuracy, or to [calibration](#conference-finals-the-evaluator-challenge) in the conference finals. If that can't separate them either, the match is a draw. The grand final drops latency, because a laptop and an API still aren't comparable.

To keep it fair, every model gets its own yes/no cutoff, tuned on one half of the data and scored on the other half. It's the same procedure and random seed we've used in the past.

## Quarterfinals: the hallucination challenge

![The bracket after the quarterfinals](/blogs/arizes-next-top-decision-model/bracket-1-quarterfinals.png)

The first challenge is one of the more popular evals, hallucination detection. Given a context and a response, is every claim in the response supported by the context? RAGTruth mixes question answering, summaries and data-to-text, and about a third of its responses contain a hallucination.

**Jev vs OpenAI.** The first frontier lab in the house drew the house favourite in round one. OpenAI scored 81.5% balanced accuracy against Jev's 85.5%. That looks like a clear gap, but the confidence intervals touch by a tenth of a point, so under our rules accuracy is a draw. The other two categories weren't close. Jev answered in 0.08 seconds per decision against 0.16, and cost $0.045 per 1,000 decisions against $0.090. Jev goes through 2–0, and OpenAI packs its bags early. Don't forget about it, though. It comes back in the twist.

**Liquid d1 vs Clef 27B.** This is the match the panel will be talking about for weeks. On accuracy it was a dead heat: Clef 27B scored 85.2%, Liquid 84.8%, well inside each other's confidence intervals. So the decision came down to the other two categories, and Liquid won both. It was faster (0.20 seconds against 0.50) and much cheaper ($0.034 per 1,000 against $0.223). Clef 27B, I'm sorry, but you're going home.

**Kev vs Laya.** Laya was the fastest model in the competition at 0.04 seconds a decision, and it's under a gigabyte. But it scored 59.8% to Kev's 76.8%. On a laptop the cost is the same for both, so accuracy decides. Kev goes through.

**Jeeves vs Strands.** Jeeves reasons before it answers, and on hallucination that thinking paid off: 80.3% against 69.0% for Strands. Strands answered about 50 times faster at the median, but speed alone can't win a match where cost is tied. Jeeves goes through, slowly.

How do the survivors compare with an LLM judge? In our [earlier benchmarks](https://arize.com/blog/jev-as-a-judge/), Opus 5 scored 86.6% balanced accuracy at $14.30 per 1,000 judgments. Jev, Liquid and Clef 27B all land within the noise of that at a fraction of the price: Jev costs 0.3% of what Opus 5 does, Liquid 0.2% and Clef 27B 1.6%. OpenAI sits a few points further back, at 0.6%.

## Conference finals: the evaluator challenge

![The bracket after the conference finals](/blogs/arizes-next-top-decision-model/bracket-2-conference-finals.png)

This round is the audition for the job most of you are hiring for: could this model be the judge in your eval pipeline? The 13 Phoenix suites test the evaluators people run in production, from faithfulness and conciseness to whether an agent handled a tool response correctly.

It's also where the panel brings out its favourite tiebreaker: calibration. A calibrated model is right 99% of the time when it says it's 99% sure, and 70% of the time when it says it's 70% sure. For a judge it counts as much as raw accuracy, because it tells you which verdicts you can trust and which ones should go to a human or a bigger model.

We score it as calibration error: the average gap between how sure a model says it is and how often it's right, so lower is better. We use the [same calibration code](https://github.com/Arize-ai/arize/pull/88522) as our earlier Jev benchmark, with every model's confidence on the same scale.

**Cloud final: Jev vs Liquid.** Jev scored 91.1% and Liquid 87.6%, and those intervals overlap, so accuracy is a draw. Jev won on speed and Liquid on cost. That's one each, so the tie goes to [calibration](#conference-finals-the-evaluator-challenge). Jev's calibration error was 0.023 and Liquid's 0.051, so on average Jev's confidence sat within 2 points of how often it was right, and Liquid's within 5. Both are excellent, and with 655 cases their confidence intervals overlap. The panel can't split them. **The cloud final is a draw.**

If you made us pick, Jev edges it by a whisker. Its confidence was a slightly better guide to its own mistakes: take one case it got right and one it got wrong, and 85% of the time it was more confident about the right one, against 81% for Liquid. On the 14% of cases where Jev said it was at least 99% sure, it was right every time. Liquid was 99% sure on a third of the cases and right 99.1% of the time, which is also very good. Jev goes through to the grand final, by a nose.

That tells you something about the hosted APIs: at the top, they're close to interchangeable.

**Local final: Kev vs Jeeves.** Kev scored 88.7%, Jeeves 87.1%. Another draw on accuracy, and a draw on cost. But Kev answered in 0.19 seconds and Jeeves in 4.3, more than 20 times slower. On this challenge, all that thinking didn't buy Jeeves any accuracy. Kev didn't need the tiebreak, but for the record the two were level on [calibration](#conference-finals-the-evaluator-challenge), 0.055 against 0.043 for Jeeves, well inside the noise. Kev's confidence was the better guide to its own mistakes, 84% against 79% on the same test as the cloud final. The underdog is your local champion.

## Grand final: the agent challenge

![The final bracket: Jev and Kev draw](/blogs/arizes-next-top-decision-model/bracket-3-grand-final.png)

The last challenge leaves the judging booth and steps inside an agent. Each case is a user message and a list of tools or skills, and the model has to pick the right one, including "none of them". Twenty cases come from the travel assistant in our [tool-calling evaluation post](https://arize.com/blog/how-to-evaluate-tool-calling-agents/), and 32 from the labelled routing tests for [Phoenix's in-app assistant](https://github.com/Arize-ai/phoenix/tree/main/evals/pxi/datasets).

Jev got 49 of 52 right. Kev got 48. With only 52 cases, one question is worth about two percentage points, so a single answer is well inside the noise. Accuracy is a draw.

Cost can't separate them fairly either. Jev costs $0.022 per 1,000 routing decisions. Kev costs nothing extra if you already own the hardware, and rather more if you have to rent a GPU to run it.

I have two photos in my hand. And I'm handing out both of them.

**The grand final is a draw.** If you want an API you call and forget, Jev is Arize's next top decision model. If you want to self-host, Kev is. The scores can't split them, so your preference for where to run picks the winner.

## The twist: ask the question the wrong way and most models flip

Surprisingly, the biggest gap in the competition isn't in the bracket.

Before the runs, we tried a few ways of wording the hallucination question. Our original RAG test prompt asks whether the response *contains an unsupported claim*. Our final question asks whether *every claim is supported*. They mean the same thing with the polarity reversed, so a model that understands the question should score about the same on both.

So we ran every model a second time with the "unsupported claim" wording, on the same 1,338 test rows. Here's ROC AUC, where 0.5 is a coin flip and anything under 0.5 means the model is answering the opposite question:

| Model | "Is every claim supported?" | "Does it contain an unsupported claim?" |
| --- | --- | --- |
| Jev 1.13 | 0.93 | 0.93 |
| Clef 27B | 0.92 | 0.91 |
| OpenAI Decisions | 0.90 | 0.89 |
| Kev 9B | 0.85 | 0.54 |
| Laya multilingual | 0.64 | 0.36 |
| Strands Decider 2B | 0.75 | 0.26 |
| Jeeves 9B | 0.85 | 0.25 |
| Liquid d1 | 0.92 | 0.17 |

Only Jev, Clef 27B and OpenAI held their pose. OpenAI went home in round one, but it's one of only three models that understood the question both ways. Kev dropped to a coin flip. Liquid, Jeeves and Strands flipped, confidently answering "is this response grounded?" when we asked "does it contain an unsupported claim?" Liquid went from one of the best scores in the competition to 0.17.

Laya showed the same weakness on everyday phrasing. On the Phoenix suites worded as "Is the text free of toxic content?", it scored 0.11. Flip the wording to "Does the text contain toxic content?" and it jumps to 0.87. Its [model card](https://huggingface.co/convaiinnovations/laya) warns that its answers can follow the option labels rather than the question.

A decision model's score belongs to the model *and* the question. Swap a new model into your judge without changing a word, and you may have inverted your evals without noticing. The fix is cheap: run the new model on both phrasings of your question before you trust it.

## The one who should have made the final: Clef 27B

Every season has a contestant who goes home too early, and the internet doesn't let it go. This season, it's Clef 27B.

| Model | Hallucination (RAGTruth) | Evaluators (Phoenix suites) | Routing | [Calibration error](#conference-finals-the-evaluator-challenge) | Latency (p50, RAGTruth) | Cost per 1,000 (RAGTruth) |
| --- | --- | --- | --- | --- | --- | --- |
| Jev 1.13 | 85.5% | 91.1% | 49/52 | 0.023 | 0.08 s | $0.045 |
| Clef 27B | 85.2% | 91.5% | 50/52 | 0.062 | 0.50 s | $0.223 |
| Liquid d1 | 84.8% | 87.6% | 48/52 | 0.051 | 0.20 s | $0.034 |
| OpenAI Decisions | 81.5% | 90.0% | 48/52 | 0.042 | 0.16 s | $0.090 |
| Jeeves 9B | 80.3% | 87.1% | 48/52 | 0.043 | 16.8 s | $0 (local) |
| Kev 9B | 76.8% | 88.7% | 48/52 | 0.055 | 1.03 s | $0 (local) |
| Strands Decider 2B | 69.0% | 76.7% | 45/52 | 0.065 | 0.34 s | $0 (local) |
| Laya multilingual | 59.8% | 57.3% | 40/52 | 0.330 | 0.04 s | $0 (local) |

*Balanced accuracy on the held-out half at each model's tuned cutoff. Routing is all 52 cases. Calibration error is on all 655 Phoenix cases, with every model's confidence on the same scale (lower is better). Local latencies are from one laptop and aren't comparable with the cloud numbers.*

Clef 27B matched Jev on accuracy in every round, and along with Jev and OpenAI it was one of only three models to survive the wording twist. It went out in round one because Liquid was faster and cheaper on the day, and against Jev it would have lost on those same two categories.

That's the trouble with knockouts, and why we published the full results. If you want open weights you can also call as a hosted API, Clef 27B is the one to look at.

## The final walk

Three weeks after Jev, the top decision models are a commodity on accuracy. Jev, Clef 27B and Liquid sit within a point of each other on hallucination, and within the noise of an LLM judge that costs 60 to 400 times more. Even the cloud final couldn't separate Jev and Liquid. Kev, an open clone whose first training run cost about $95 in rented GPUs, ties Jev in the agent challenge.

Pick on where you want to run it, an API you call or weights you host. Then check the model reads your question the way you meant it, because wording can flip a judge from right to confidently wrong.

Test the question as hard as you test the model.

## Your turn on the runway

You don't need to rebuild our harness to run your own season. Arize AX has [Jev as a judge](https://arize.com/docs/ax/evaluate/jev-as-a-judge) built in: add your TypeSafe API key, write your question, and Jev scores your traces with a label and a confidence. If your contestant is one we didn't bring, like Kev on your own GPU, put it behind an HTTPS endpoint and connect it as a [remote evaluator](https://arize.com/docs/ax/evaluate/remote-evaluators). Your model does the scoring, and AX handles calling it, retries and writing the results back onto your traces. Either way, put both phrasings of your question to it before you trust the scores.
