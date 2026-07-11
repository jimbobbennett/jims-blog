---
author: "Jim Bennett"
date: 2026-07-11
publishDate: 2026-07-11
description: "Everyone's talking about AI evals like they're a brand new discipline. They're not. They're testing - the same loop you've run for years. Define what good looks like, test against it, and fix your definition when it turns out to be wrong. What changed isn't the loop. It's the answer key."
draft: false
slug: "evals-are-just-testing"
title: "AI evals are just testing (with a much weirder answer key)"
tags: ["ai", "evals", "llm", "testing", "observability"]

images:
  - /blogs/evals-are-just-testing/banner.png
featured_image: banner.png
---

Years ago, before "AI" meant chatbots and before anyone said the word "eval" out loud, I spent a few months chasing a bug that didn't exist. Or rather, the bug was real - it just wasn't in my code.

I was working at a cheminformatics company - software for chemists, basically - and my job was to add chiral searching to our chemical structure search. If you've not had the pleasure: chirality is when a molecule and its mirror image aren't the same thing, like your left and right hands. Same fingers, same layout, but you can't rotate one onto the other. In chemistry that difference is a big deal - one version of a molecule can be a medicine and its mirror image can do nothing, or worse. So "does this structure match that one?" suddenly has to care about handedness.

My product manager did something genuinely brilliant. Instead of writing me a spec full of hand-wavy prose, they sent me hundreds of examples: this structure *should* match that one, this pair *shouldn't*. Real molecules, real expected answers. I didn't have the word for it at the time, but that was a golden dataset. And I did the obvious thing with it - I turned every example into a unit test and started making them pass.

![A chiral molecule pair - two mirror-image 3D chemical structures over a left and a right hand, one pairing marked with a green tick and the other with a red cross](/blogs/evals-are-just-testing/banner.png)

## The tests were failing because the answer was wrong

Here's the part I still think about. As I worked through the examples, some tests just wouldn't go green no matter what I did. My code said "no match," the golden dataset said "match," and I could not for the life of me reconcile them.

So I did what you do - I assumed I was the idiot. I stared at my matching logic for hours. I traced through the atoms by hand. And eventually, on a handful of cases, I realised my code was *right* and the dataset was *wrong*. Some of those hand-picked examples were mislabelled. The source of truth had bugs in it.

That changed the whole job. It wasn't "write code until the tests pass" any more. It was "write code and fix the tests, because some of the tests are lying to me." My PM and I ended up iterating on the golden dataset itself - correcting labels, arguing over edge cases, tightening what "match" even meant. The dataset got better *because* I was testing against it, and my code got better because the dataset got better.

That, it turns out, is an eval. I was doing evals in the early 2000s. I just called them tests.

## Testing was never really about "does it run"

Let's back up, because this matters for where evals fit.

If you're an engineer, you already know testing. But it's worth remembering that testing has never actually been about proving your code works. Edsger Dijkstra nailed this decades ago:

> Testing shows the presence, not the absence of bugs.

You can't test your way to "this is correct." You can only ever catch it being wrong. If you did any science at school, this is the null hypothesis wearing a different hat: you never prove your hypothesis true, you just keep failing to disprove it. A green test suite isn't proof your code works - it's a stack of experiments that tried to show it was broken and couldn't. Absence of evidence, not evidence of absence. And the field slowly came round to that idea. Testing started life as glorified debugging, then became "demonstrate it works," and then - around the time Glenford Myers wrote *The Art of Software Testing* in 1979 - flipped into something more useful: a good test is one that *finds* a bug. You're not trying to confirm your happy path. You're trying to break the thing.

By the time we got to test-driven development, the loop was fully formed. [TDD](https://martinfowler.com/bliki/TestDrivenDevelopment.html) is red-green-refactor: you write a failing test that describes the behaviour you want *before* you write the code, then you make it pass. You're writing down "what good looks like" first, then building towards it. Unit tests, integration tests, [UI tests](/blogs/ui-testing-your-xamarin-apps) - each one is just a wider net, checking a bigger slice of the system against a definition of correct that *you* wrote down.

That's the whole game, and it always has been:

1. Decide what "good" looks like.
1. Check reality against it.
1. When the check and reality disagree, figure out which one is wrong - and sometimes it's your definition.

Hold onto that last point. It's the one everyone forgets, and it's the one my chiral bug beat into me.

## So what's an eval, then?

Right. AI apps. You've built something on top of a large language model (LLM) - a chatbot, a summariser, an agent that books meetings, whatever. How do you test it?

You can't write `assert output == "the expected answer"`, because there isn't one expected answer. Ask the same model the same question twice and you'll get two different sentences that both mean the same thing. The output is non-deterministic, and often it's judged on fuzzy things like "is this helpful?" or "is the tone right?" - questions with no single correct string.

An **eval** is how you test that anyway. And if you squint, every piece of it maps onto something you already know:

- A **golden dataset** - a set of trusted inputs with ideal outputs, usually hand-labelled by people who know the domain - is your test fixtures and expected values. It's exactly what my PM sent me: examples of right and wrong.
- An **[LLM-as-a-judge](/blogs/anatomy-of-an-eval-prompt)** - a second model you prompt to grade the first one's output - is your assertion. It's the `assert` you *can't* write as a simple equality check, so you hand it to something that can read a sentence and say "yeah, that's helpful" or "no, that dodged the question." (For the prompt-based kind, a judge is just a new prompt, not a new model - which is a very freeing thing to realise.)
- The **score** it hands back - "8 out of 10," "pass," "hallucinated" - is your pass/fail, just fuzzier.

Same loop. Define good, check reality against it. If you want the full spread of how you actually run these - from a dead-simple code check all the way up to a full agent doing the grading - I wrote about the [four ways to run an eval](/blogs/four-ways-to-run-evals) separately.

![A two-column mapping diagram - classic testing terms on the left (fixture, assertion, pass/fail) with arrows to their eval equivalents on the right (golden dataset, LLM judge, score)](/blogs/evals-are-just-testing/testing-to-evals-mapping.png)

## Where the analogy gets uncomfortable

I want to be honest here, because "evals are just testing" is a great line and also slightly too smug.

The loop is old. The answer key got weird.

With a classic unit test, your oracle - the thing that decides pass or fail - is crisp. `2 + 2` should be `4`, and it either is or it isn't. With an eval, the oracle is often another model, or a human, or a statistical threshold. It's subjective. It drifts. Two reasonable people disagree on whether an answer was "helpful." Your judge model has its own biases. And the moment you start optimising your app to score well on a judge, you risk gaming the judge instead of actually getting better - the AI equivalent of teaching to the test.

None of that makes it *not* testing. My chiral matching wasn't a clean `==` either - it was rules and tolerances and edge cases, fuzzy long before LLMs showed up. This is a difference of degree, not kind. But the degree is big enough that you have to take one part of testing that engineers usually get away with ignoring, and put it front and centre.

## Your eval is a product, and it needs testing too

Here's the bit my chiral bug was really teaching me.

When some of those golden examples turned out to be wrong, the lesson wasn't "datasets sometimes have typos." It was: **the thing you test against is itself a fallible product, and it needs testing.** My tests were only as trustworthy as the golden data behind them, and that data was wrong often enough to matter.

With classic testing you can usually skate past this. Your expected values are simple enough that nobody seriously worries the test itself is broken. With evals you cannot skate past it at all. Your LLM judge can be confidently, consistently wrong. So you have to validate the judge against human-labelled golden data - and then you have to make sure you're not tuning your judge on the very same examples you use to prove it works, which is its own trap. (That's a real enough problem that I gave it [its own post on the train/dev/test split](/blogs/train-dev-test).)

So now you're maintaining two products, not one. There's the AI app, and there's the eval that tests it - and the eval needs its own golden data, its own iteration, its own "wait, is the judge wrong or is the app wrong?" moments. Which is exactly the argument I was having with my PM, just with a model in the mix instead of a mislabelled molecule.

## "If it's just testing, why all the new tooling?"

Fair question. If evals are just tests, why is there a whole industry of eval platforms, dataset versioning, judge calibration and dashboards? Why can't I just chuck it all in my existing test runner?

Because the weird answer key drags a lot of baggage in with it. You need to *version* golden datasets, because they change as you learn - mine certainly did. You need to run the same input multiple times and look at the distribution, because one pass tells you nothing about a non-deterministic system. You need to collect real traffic and pull the interesting cases back into your dataset. You need humans in the loop to keep the judges honest. And you need [evals doing different jobs at different stages](/blogs/evals-across-the-lifecycle) - some gating your releases like a CI check, some [watching live traffic in production, some sitting in the request path as guardrails](/blogs/three-jobs-evals-do).

That's not a different discipline. It's testing with the volume turned up on the one part - the oracle - that classic testing let you take for granted.

## The flywheel

Put it all together and you get a loop that looks like an infinity symbol.

Your app runs in production and throws off traces - real inputs, real outputs. Humans review the interesting ones and curate them into versioned golden data. That golden data validates and sharpens your evals. Those evals gate changes to your app. The improved app goes back to production and surfaces new cases you hadn't thought of. Round and round.

![An infinity-loop flywheel - on one side the AI app in production surfacing traces, feeding into human review and labelling, then a held-out golden dataset, then evals, which gate the app and loop back round](/blogs/evals-are-just-testing/evals-flywheel.png)

The important node in that diagram is the human one. Without people curating the data, the loop collapses into an app grading its own homework, and you learn nothing. The whole thing only works because a person keeps deciding what "good" actually means - the same job my PM was doing when they sent me those hundreds of examples.

So no, evals aren't magic, and they aren't a new thing you have to learn from scratch. If you can test software, you already know how to do this. Define what good looks like, test against it, and stay humble about the fact that your definition of good might be the thing that's broken.

The loop is old. It's just the answer key that got weird.
