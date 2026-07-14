---
author: "Jim Bennett"
date: 2026-07-15
publishDate: 2026-07-15
description: "If evals are just testing, then they belong where your tests already live - in CI, blocking bad PRs. Here's how a golden dataset becomes parameterised tests, how arrange-act-assert grows an extra step, and why you should gate on a passing percentage instead of demanding a green board."
draft: false
slug: "evals-in-your-ci-cd-pipeline"
title: "Evals belong in your CI/CD pipeline"
tags: ["ai", "evals", "llm", "testing", "ci-cd", "observability"]

images:
  - /blogs/evals-in-your-ci-cd-pipeline/arrange-act-eval-assert.png
featured_image: arrange-act-eval-assert.png
---

The other day I wrote that [evals are just testing](/blogs/evals-are-just-testing) - the same old loop of "decide what good looks like, check reality against it, fix your definition when it turns out to be wrong," just with a much weirder answer key. A few people replied with the obvious follow-up question, and it's a good one: OK, if evals are just tests, why aren't they running where my tests run?

Because that's the bit we often skip. We'll happily wire up a golden dataset, write an evaluator, run it once from a notebook, nod at the score, and move on. Meanwhile every actual unit test we own runs automatically on every pull request, and a failed test blocks the merge. Evals get none of that. They sit in an observability platform like Arize AX while someone changes a system prompt in GitHub and ships it on vibes.

This post is about closing that gap. Evals are tests, so let's put them where your tests live - in continuous integration, gating your pull requests - and let's do it in a way that survives the fact that AI output is fuzzy and non-deterministic.

## Your golden dataset is already a parameterised test

Start with the thing you already have: a golden dataset. A curated set of trusted inputs with the outputs you'd want back, usually hand-labelled by someone who knows the domain. A dataset is "the foundation for reliably testing and evaluating your LLM application."

If you've written tests in the last decade, you've seen this shape before. It's a parameterised test. Here's the classic pytest version:

```python
import pytest

@pytest.mark.parametrize("expression,expected", [
    ("2 + 2", "4"),
    ("10 / 2", "5"),
    ("3 * 3", "9"),
])
def test_calculator(expression, expected):
    assert calculate(expression) == expected
```

One test body, three rows of parameters, three results. You don't write `test_calculator_1`, `test_calculator_2`, `test_calculator_3` - you write the body once and feed it a table of cases.

A golden dataset is that table. Each row is an input plus the expected output, and every row runs through the same task. When you run an experiment in AX, that's exactly what happens: your task function runs once per row, and every evaluator scores every row.

Same idea as `@pytest.mark.parametrize`, just that the parameters live in a versioned dataset instead of a decorator. Which is actually the upgrade you want, because a golden dataset grows: you pull interesting cases out of production, a teammate adds an edge case that broke last month, and the table gets richer over time without touching the test body.

![Your golden dataset is a parameterised test: a table of input/expected rows on the left feeds a single task-plus-evaluator body in the middle, which fans out to one pass/fail result per row on the right - the same shape as @pytest.mark.parametrize](/blogs/evals-in-your-ci-cd-pipeline/golden-dataset-parameterised.png)

## Arrange, act, eval, assert

Here's the mental model I keep coming back to. You already know arrange-act-assert - the three beats of pretty much every unit test ever written:

- **Arrange**: set up your inputs and world.
- **Act**: run the thing under test.
- **Assert**: check the output is what you expected.

The reason that works is that the output is deterministic. `calculate("2 + 2")` returns `"4"` every single time, so `assert result == "4"` is a fair check. But an AI app doesn't play that game. Ask a model the same question twice and you'll get two different sentences that mean the same thing. You can't `assert output == "the expected answer"` because there isn't *an* answer, there's a fuzzy cloud of acceptable ones.

So you add a step. Arrange, **act, eval,** assert.

![Arrange-act-eval-assert: a four-panel diagram showing the classic three-step unit test flow with a fourth "Eval" step inserted before the assertion, each step mapped to its Arize AX primitive underneath](/blogs/evals-in-your-ci-cd-pipeline/arrange-act-eval-assert.png)

The new **eval** step is where the fuzziness gets dealt with. Before you can assert anything, you run the output through an evaluator - which can be [any of four things, from a dead-simple code check to a full LLM-as-a-judge](/blogs/four-ways-to-run-evals) - that turns a squishy sentence into something you *can* assert on: a score, a label, a pass or fail. Only then do you assert.

- **Arrange** is fetching the dataset. Those are your rows.
- **Act** is the task function - run your app against a row and produce an output.
- **Eval** is the evaluator - grade that output into a score.
- **Assert** is the gate - pass or fail based on the scores.

Your evaluators are the new eval step. You run an eval against the output from your test first. This gives you the deterministic output that feeds the Assert.

## Gate on a percentage, not perfection

This is the part that trips up engineers coming from normal tests, so I want to sit on it for a second.

With a unit test suite, the rule is simple and brutal: one failed test fails the build. You want the board fully green, every time, no exceptions. It's tempting to carry that straight over - "all evals must pass or the PR is blocked" - and it's wrong.

AI output is non-deterministic. [Arize's own writing on testing agents](https://arize.com/blog/why-testing-ai-agents-is-non-negotiable/) says it well:

> We don't expect 100% pass rates (that would be suspicious). But we do expect consistency.

A 100% pass rate on a fuzzy system usually means your dataset is too easy or your judge is asleep, not that your app is perfect. So instead of demanding every row pass, you gate on an aggregate: what fraction passed, or what the mean score was, against a threshold you decide.

Your threshold is a real engineering decision, not a cop-out. Set it where a regression should genuinely block a merge, watch it over time, and raise it as your app gets better. If pass rates drop below our threshold, the PR is blocked.

![Gate on a percentage, not perfection: a bar chart of ten per-row evaluator scores against a dashed 0.7 threshold line. Two rows dip below the line but the mean of 0.82 clears it, so the gate stays green - whereas demanding all ten pass would turn a healthy run red on noise](/blogs/evals-in-your-ci-cd-pipeline/percentage-gate.png)

## Wiring it into a PR gate

Now the fun bit - making it run on every PR that touches your AI.

![Evals as a PR gate: a PR that touches prompts or agents triggers a GitHub Action, which runs the experiment against the golden dataset, scores it, and checks the mean against a 0.7 threshold. Pass and the PR goes green and can merge; fail and the PR is blocked before a human hits merge](/blogs/evals-in-your-ci-cd-pipeline/pr-gate-loop.png)

You don't run your evals on every commit - that'd be slow and expensive - you run them when someone changes the stuff that actually affects behaviour: the prompts, the tools, the agent logic. Change a system prompt, the experiment runs against your golden dataset, and if the pass rate falls below your threshold the PR goes red. Your API key lives in secrets and gets injected as an environment variable, same as any other credential.

That's it. That's evals as a PR gate. A change that quietly makes your assistant worse now gets caught by a robot before a human ever hits merge, exactly like a failing unit test.

## Who tests the tests? Unit-testing your eval prompts

There's a sharp edge here, and it's the one my old chiral-molecule bug beat into me: the thing you test against can itself be wrong. An LLM-as-a-judge is just a prompt, and prompts are fallible. A judge that's too generous passes garbage. A judge that's too harsh blocks good changes and trains your team to ignore the gate. Either way, a broken judge is worse than no judge, because you trust it.

So you test the judge, using the exact same machinery. You just point it at itself.

Build a small dataset of outputs you've already graded by hand - some you know are good, some you know are bad, with the correct verdict labelled on each row. Now run your judge against *that*. The judge is the thing under test, the task is "ask the judge to grade this output," and the human labels are the expected values. If the judge disagrees with the humans too often, the judge fails its own test, and you go fix the judge prompt before you trust it to gate anything.

It's parameterised testing all the way down. Same arrange-act-eval-assert, except the "app" being tested is your evaluator. One warning worth its own callout:

> Don't tune your judge on the same examples you use to prove it works. That's teaching to the test - the judge looks great on the cases it was built against and falls over on everything else. Hold some examples back. I wrote about the [train/dev/test split](/blogs/train-dev-test) separately, and it matters more here than almost anywhere.

Do this and you end up maintaining two products that both live in CI: the AI app, and the eval that guards it. Both have golden datasets. Both have gates. Both block a PR when they regress. That's eval-driven development - the same discipline you already trust for code, turned back on the tool doing the grading.

## So where does that leave you?

Nowhere new, really, and that's the point. You already know how to do all of this. Parameterised cases, a red-green gate in CI, a PR that can't merge when the checks fall over - that's Tuesday for most engineering teams. Evals just ask you to insert one extra step before the assertion and to gate on a percentage instead of a perfect board.

Put your evals in CI. Let a golden dataset drive them, let an evaluator handle the fuzzy part, and let a threshold block the bad PRs. The loop is old. You're just running it on the weird answer key now, right next to the tests you already have.
