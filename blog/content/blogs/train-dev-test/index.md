---
author: "Jim Bennett"
date: 2026-07-08
publishDate: 2026-07-08
description: "If you tune an LLM judge on the same examples you use to prove it works, you've proved nothing. The fix is a trick borrowed straight from machine learning: split your labelled traces into train, dev and test, and never let them mix."
draft: true
slug: "train-dev-test"
title: "Train, dev, test: the split that makes an LLM judge trustworthy"
tags: ["ai", "evals", "llm", "observability"]

images:
  - /blogs/train-dev-test/banner.png
featured_image: banner.png
---

Say you've built an LLM judge and you want to know if it's any good. The obvious move is to feed it some labelled examples, tweak the prompt until its scores match your labels, and then point to those matching scores as proof it works.

Except you've proved nothing. You tuned the judge on those exact examples, so of course it agrees with them - you bent it until it did. It's the oldest mistake in machine learning: marking your own homework with the answer sheet open. The fix is just as old, and it carries straight over to building evals. Split your labelled traces into three piles, and never let them touch.

![Infographic: train, dev, test - splitting your labelled traces to build an evaluator you can trust, with roughly 10-20%, 20-30% and 50-70% of your data](/blogs/train-dev-test/banner.png)

*Want it to hand? [Download the infographic as a PDF](/blogs/train-dev-test/infographic.pdf).*

The three piles run left to right from *teach* to *validate*. The rough proportions are on the cards - a small training slice, a medium dev slice, and the bulk held back for the test - and those proportions matter, so I'll come back to why. First, what each pile is actually for.

## Train, 10 to 20%

The smallest pile. This is the handful of hand-labelled traces you use to *teach* the judge what good and bad look like - ideally a few clear examples of a passing case and a few of a failing one.

These are the cases you drop straight into the prompt as few-shot examples. They're the judge's reference points, the "here's what I mean" samples it pattern-matches against when it sees something new. (This is the examples slot from the [anatomy of an eval prompt](/blogs/anatomy-of-an-eval-prompt) post - now you know where those examples are supposed to come from.) You don't need many. Three to five passes and three to five fails is plenty, which is why this slice is small. Their job is to demonstrate, not to cover every case.

## Dev, 20 to 30%

The middle pile is your workbench. This is the held-out set you iterate the prompt against, run after run, as you tune it.

You score the dev set, see where the judge disagrees with your labels, adjust the wording of the criteria or the rubric, and run it again. Tighten, re-score, repeat, until the judge's scores line up with yours across the set. This is the loop where the actual work happens, and it's deliberately *not* the train set - if you only ever checked against the few examples baked into the prompt, you'd just be confirming the judge can parrot back what you showed it. The dev set tells you whether it generalises a little beyond the exact cases it was taught.

## Test, 50 to 70%

The biggest pile, and the one with the strictest rule: you don't look at it. Not while you're tuning, not to peek, not even once. It sits untouched the entire time you're working on the dev set.

These are unseen labelled traces the judge has never encountered, and you score them exactly once, at the end, when you think you're done. That single run is your real evidence. Because the judge was never tuned against these, its agreement with your labels here is an honest estimate of how it'll do on live traffic it's never seen. You measure the true-positive and true-negative rates - how often it correctly catches the bad cases and correctly passes the good ones - and *that's* the number you actually trust. If you'd glanced at the test set while tuning, even a little, it'd be contaminated, and you'd be back to marking your own homework.

## Why the proportions are upside down

Here's the bit that catches people out. The split is backwards from what your instincts say. You teach with the *smallest* slice and validate with the *largest*, when intuition screams it should be the other way round.

But think about what each pile is for. Teaching needs only a few clear examples - a handful of passes and fails is enough to anchor the judge. Proving it works needs as much unseen data as you can spare, because the more cases you test on, the more you can trust the result. So the bulk of your data goes into the test pile, where it does the most good. A few examples teach; lots of examples prove.

That's the whole trick, and it's why an eval built this way is one you can actually defend. You taught the judge on one slice, tuned it on another, and proved it on a third it never saw coming. The score it gets on that final untouched pile is the one you can take to live traffic with a straight face - which, when the whole point of an eval is [knowing it agrees with a human](/blogs/how-to-build-an-eval), is exactly the number you were after all along.
