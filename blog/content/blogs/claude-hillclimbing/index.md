---
author: "Jim Bennett"
date: 2026-09-29
publishDate: 2026-09-29
description: "Anthropic's new build-eval and hillclimb commands get the method right. Here's what it takes to run that loop on a production agent: start from your traces, mix your graders, aim for the cheapest setup that clears the bar, and keep results where the team can see them."
draft: false
slug: "claude-hillclimbing"
title: "Claude's hillclimb loop, with your traces underneath"
tags: ["ai", "evals", "claude", "agents", "observability"]

images:
  - /blogs/claude-hillclimbing/cover.png
featured_image: cover.png
hero_alt: "Two engineers with coffee at a standing desk look out of a window at a glowing wireframe data mountain, with a neon stepped graph climbing to a beacon at the summit"
---

On September 28, Anthropic's Lance Martin published [Automating eval design and hillclimbing with Claude](https://claude.dev/blog/automating-eval-design-and-hillclimbing/). It adds two commands to the claude-api skill. `/claude-api build-eval` interviews you and builds an evaluation inside your codebase. `/claude-api hillclimb` then improves your application against that eval, *"one change at a time, with a held-out set of examples to catch overfitting."*

> **Hillclimbing** is the name for that second loop: make one change, score it, keep it if the score goes up, revert it if it doesn't, repeat.

We read it and nodded along most of the way. It's very close in principle to how we run evals at Arize, on our own agents and with the teams we work with, but with a few big gaps. We have a "yes, and": the method is right. The question is what happens when the loop leaves one engineer's laptop and has to run against an agent in production, reliably, repeatably, and with a team around it.

## What Anthropic gets right

Start with the eval itself. The post lists four elements of a good one: *"Eval tasks mirror production."* It's easy to build a test set out of whatever is simple to generate or grade. It's much harder, and much more useful, to build one out of what your users actually do.

The advice on hard cases is just as clear. *"Pick hard cases because a human judged them hard."* It's the line we'd underline. A model can generate a thousand test cases, but it can't tell you which ones matter to your users. Deciding what "hard" means, and what "good" looks like, is a human call, and everything downstream inherits it: the eval set, the rubric and the judge.

If you only collect the cases today's model fails, you end up measuring that model's weak spots rather than what's hard about your problem. Anyone who has watched an eval set go stale after a model upgrade will recognize this one.

On grading, `build-eval` *"proposes the cheapest grader that fits."* That means code checks when the output is constrained, and a large language model (LLM) as a judge when the output is open-ended. The rubric is written as checkable claims rather than a 1-to-5 scale, and the post is explicit that *"You pick the judge model, and it should not be the model you are testing."*

The hillclimb side has the guardrails you'd want. The cases are split at random into train and test, and the noise is checked before the first round. Each round makes one change. If the training set goes up while the testing set stays flat, Claude treats that as overfitting and reverts.

When you run `hillclimb`, you choose what it's allowed to change:

- Your system prompt
- Skills or instruction files
- Tool descriptions
- Model choice, effort level, and other API parameters
- Your harness code

That list is a good working definition of "the agent". It's not just the model. It's the model plus everything wrapped around it, and every item on the list is something you can change and score.

The post's second example proves the point. Anthropic hillclimbed their own claude-api skill against an eval built from their documentation, and took it from 66% to about 88%. A skill is on that list, so a skill can be climbed.

## Our running example: the arize-instrumentation skill

![The hillclimb loop: traces feed a dataset, evaluators score an experiment against the baseline, and one change is kept or reverted before the loop runs again](/blogs/claude-hillclimbing/hillclimb-loop.png)

We've been hill-climbing a skill too. Our [arize-instrumentation skill](https://arize.com/docs/ax/skills/catalog) adds Arize tracing to an app that has none. You point Claude Code, Cursor or Codex at it, and the coding agent follows the recipe instead of guessing. We wanted it to work as often as possible, as fast as possible, with as few tokens as possible. The full write-up is in [Quantifying skill changes in Arize AX](https://arize.com/blog/quantifying-skill-changes-arize-ax/).

The loop itself is the one Anthropic describes. Run the current skill across a dataset and save that experiment as the baseline. Make one edit, rerun the identical experiment, and compare. Where our version differs is in four places, and each one is a "yes, and."

## Yes, and: start from your traces

Look at the order `build-eval` uses to gather inputs:

1. Production transcripts, after asking about retention and sensitive data.
2. Bug reports and support tickets.
3. A small set of cases you write by hand.
4. Cases synthesized from your codebase.

Production transcripts are first, and the getting-started section suggests steering the command with *"access to examples (e.g., traces)."* We agree completely. If your agent is traced, you already have those transcripts, complete with the tool calls, retrieved context and model responses that led to each output.

Traces come from your agent sending data to an observability tool like [Arize AX](https://arize.com/ax/).

In the skill example, the traces come from the coding agent itself. Every run is traced with [coding-harness-tracing](https://github.com/Arize-ai/coding-harness-tracing), so each model response, tool call and subagent lands as a span attached to the experiment, along with its token count. The input side is a dataset where each row names the coding agent, the model, the source of the skill (the main branch of the [arize-skills repo](https://github.com/Arize-ai/arize-skills), or a PR branch), the prompt, and the app to instrument.

Those apps are chosen to mirror what users actually bring. They come from [project-rosetta-stone](https://github.com/Arize-ai/project-rosetta-stone), our sample app built in every framework OpenInference supports, plus a few small apps like an OpenAI SDK "hello world" with manual tool calling. That makes the dataset a grid of real apps, coding agents, models and skill versions. Changing one of those at a time is what makes a result attributable.

The bigger difference is what happens next. A folder of exported transcripts is a snapshot. A dataset built from traces can keep growing. When a new failure shows up in production, you add that trace to the dataset, and the next experiment covers it. Over a few months, the eval set follows your users instead of your first guess at them.

Someone still has to decide which traces are worth adding. That's the job of human annotation. An LLM can help here too, by scanning many traces for error patterns and pointing reviewers at the clusters worth their time. That gives you the same "a human judged them hard" rule, applied to production traffic.

## Yes, and: mix your graders

"The cheapest grader that fits" is the right rule. In practice, you often need more than one grader per row, and they work best together.

The skill example asks "how good was the tracing it produced?", not "did it pass?", and three evaluators share the work:

- An LLM judge reads the traces the instrumented app generated and grades them for correctness.
- A code evaluator checks the verifiable things: it used the auto-instrumentors, it created sessions where it should, it set span status, and the app still runs.
- The app is run, and a second code evaluator checks that traces land in AX with the right shape.

Each check that passes is worth a point, so the grade is a percentage of checks passed. The code evals catch the cheap, verifiable things, and they can clean up the input before the judge sees it. Strip out noise, validate the structure, and hand the judge only what it needs. The judge gets cheaper and more consistent.

None of that means anything if the agent can reach the answer. Coding agents cheat. The first time we ran this, the agent noticed that the Rosetta Stone repo already contained a version of the app with AX tracing, and copied it. It would also pick up other installed skills, or spot Phoenix running locally and trace to that instead. As the original write-up puts it, *"it's the agent being good at its job."* Laurie Voss makes the wider point in [agents are too smart for our benchmarks](https://arize.com/blog/agents-too-smart-for-benchmarks/).

Anthropic's advice lines up: *"Keep the answers structurally out of the model's reach."* For us, that meant a fresh container for each row, with only the bare app and the credentials it genuinely needs.

Past code and LLM judges, there are more options. For multi-step work, where the right answer depends on what the agent did along the way, an [agent-as-a-judge evaluator](https://arize.com/docs/ax/release-notes/history/2026/09-2026) can investigate the trace before reaching a verdict. And for bounded questions like "did it choose the right tool?", a decision model can beat a general-purpose LLM. In an Arize benchmark on hallucination detection, [a threshold-tuned Jev matched Claude Opus 5 at 87% accuracy](https://arize.com/blog/arize-ax-jev-as-a-judge/), *"while running at roughly 1/300 of the cost and 23x the speed in that test."*

Two further points. First, Anthropic already says the judge shouldn't be the model you're testing. We'd go a step further and use a judge from a different model family where you can, so you aren't grading Claude only with Claude's blind spots. Second, calibrate every judge against human labels. The same Jev test found the default threshold *"performed materially worse"* until it was tuned against labeled data. Anthropic makes the same point: read a sample of scored transcripts before you believe your evaluator.

## Yes, and: aim for the cheapest setup that clears the bar

One of Anthropic's four elements of a good eval is *"Performance improves with stronger models and more thinking."* As a sanity check on the eval, that's useful. If a stronger model does worse, the task or the grader is probably broken.

As a target, it points the wrong way. The goal for most production agents isn't the most capable model at the highest effort. It's the cheapest configuration that clears the quality bar you care about. Better prompts, better tools and better graders often do more than a bigger model.

Anthropic's own cost example makes this case well. It started on Opus 4.8 at high effort, with 74.4% accuracy at 4.6 cents per ticket. The hillclimb cleaned up the prompt, moved to Opus 5.5 at low effort, then stepped down to Sonnet 5 at low effort, which scored 88.9% at 1 cent per ticket. On the 14 held-out tickets, the final setup scored 90.5% against the original's 78.6%, *"at about one fifth of the cost."* The winning move was a smaller model with a better prompt.

To be fair to the post, `hillclimb` already supports this. You can ask it to optimize for *"cost while performance holds"*, and if the baseline already scores about 95% or higher, it warns you to explore cost or latency instead of quality. The practical step is to make it the default.

That's what the skill example does. Total tokens and latency for the coding agent are captured as scores on every row, alongside the grade. The grade should go up, and tokens and latency should go down, so every change shows its cost next to its quality.

![PR #101 against the current skill: trace correctness 74% to 83%, overall tracing grade 13% to 50%, correct session use 83% to 100%, tokens down 9% and latency down 22%](/blogs/claude-hillclimbing/pr101-before-after.png)

[PR #101 against arize-skills](https://github.com/Arize-ai/arize-skills/pull/101) shows why that matters. It cut duplicated guidance and filled gaps in the skill, and the experiments showed better tracing for fewer tokens and less time, with no model change at all.

## Yes, and: keep results near the data

By default, `build-eval` gives you the cases, the grader, the runner, a JSON line and transcript per case, and *"a plain page that lists each case's score with a link to its transcript."* Any extra pages are *"static files that open locally and load nothing from the network."*

For one engineer on one laptop, that's a sensible default. It's private, fast and simple. For a team running an agent in production, it runs out quickly.

A team needs the raw rows, not just the page. They need to filter by model, slice by input type, and sort by the worst scores. They need to compare this week's experiment with last week's side by side, and keep that history around after the branch is merged.

In the skill example, AX puts the baseline and the new experiment next to each other, so "is it better?" becomes a set of numbers that moved. [Experiment charts](https://arize.com/docs/ax/develop/datasets-and-experiments) show how each evaluator's score changes from run to run, or you can put them on a [dashboard](https://arize.com/docs/ax/observe/dashboards) so the whole team can watch the climb. When a row scores badly, you open its trace. Because the coding agent was traced, you can follow what it did step by step, and usually find the sentence in the skill that sent it the wrong way. Fix the sentence, and run the loop again. It's why the write-up can say of the PR #101 results that *"every one of those numbers came from an experiment run rather than someone's read of the diff."*

## Run the loop yourself

You don't have to build this by hand. The [Arize skills](https://arize.com/docs/ax/skills/catalog) give a coding agent the AX workflow as a set of recipes. Install them then let Claude Code drive:

1. Use arize-trace to pull the production traces that matter.
2. Use arize-dataset to turn them into a dataset, split into train and test.
3. Use arize-evaluator to set up code evals and judges, and check them against human labels.
4. Use arize-experiment to run the baseline, then hillclimb one change at a time, tracking quality, tokens and latency.

The discipline is the one Anthropic describes. The difference is that each experiment, score and trace lands where your team can find it.

## From method to habit

Anthropic has made the hillclimbing method easy to start: build the eval, climb against it, and don't fool yourself along the way. That's a real gift to anyone building agents, but it's not enough for real production work.

The catch is that a hillclimb on your laptop only runs when you remember to run it. Your agent's behavior keeps changing when nobody is looking. Users try things you didn't plan for, tools return something new, and a prompt tweak from last week interacts badly with a model update. Turning the method into a habit means something is watching production all the time. That's where Arize AX earns its place alongside Claude:

- **Online evals score live traffic.** The evaluators you hillclimb against can [run continuously against your production traces](https://arize.com/docs/ax/evaluate/run-evals-on-traces), sampled and filtered, so a drop in quality shows up on a chart instead of in a support ticket.
- **Signal finds what you didn't think to test.** [Signal](https://arize.com/blog/from-signal-to-pr/) reviews new traces on a schedule and groups recurring failures into ranked issues, including patterns nobody has written an eval for yet. With a repository connected, it can carry the investigation into the codebase, propose a fix, and open a pull request.
- **New failures become new test cases.** Every issue comes with the traces behind it. Add them to the dataset, and the next hillclimb has to handle them.
- **Humans stay in charge of "good".** Reviewers label the traces that matter, and those labels keep your judges honest as the traffic shifts.
- **It works with any model and any harness.** Claude Code, Cursor or Codex can drive the loop, and your judges can come from whichever model family grades best, mixing and matching as needed.

Claude's hillclimb gives you the method. Arize AX keeps the loop running. Your traces become the eval set, the eval set grows as your users find new edges, and every change gets a score on quality, cost and latency before it ships, with a trace behind it that anyone on the team can open.
