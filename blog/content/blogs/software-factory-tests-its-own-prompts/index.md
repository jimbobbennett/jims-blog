---
author: "Jim Bennett"
date: 2026-10-22T08:00:00-07:00
publishDate: 2026-10-22T08:00:00-07:00
description: "I built a small software factory where Claude agents turn GitHub issues into released code, traced every step to Arize AX, and used the verdicts the factory already produces as labels to test and improve its own prompts before they ship."
draft: true
slug: "software-factory-tests-its-own-prompts"
title: "How to build a software factory that tests its own prompts"
tags: ["ai", "agents", "software-factory", "evals", "llm-as-judge", "prompt-engineering", "arize-ax"]
images:
  - cover.png
featured_image: cover.png
---

I was reading about [OpenAI's agentic software factory](https://newsletter.pragmaticengineer.com/p/openai-software-factory) last week, and one line caught my attention. OpenAI's engineering workflows now involve nine stages of agents writing, testing, reviewing, and deploying code, while load on some systems has increased roughly tenfold in six months. For Venkat Venkataramani, OpenAI's VP of engineering for applied infrastructure, this rapid shift raises a fundamental question: **what does observability even mean when agents are doing the work?**

That's a big gap for a team shipping that much code. So, I built a small software factory of my own to find out what observability and evals look like. It turns GitHub issues into released code with an agent at every step, traces everything to [Arize AX](https://arize.com/), and uses the verdicts it already produces to test and improve its own prompts before they go live.

> TLDR; The factory is at [jimbobbennett/software-factory](https://github.com/jimbobbennett/software-factory) and the app it builds is [jimbobbennett/ship-it-card](https://github.com/jimbobbennett/ship-it-card).

## What is a software factory?

![A generic software factory: a human writes the issue, then agents handle spec, build, review and release, with CI and a merge gate in between. CI, the reviewers, the merge gate and reverts each produce a verdict, such as pass or fail and ship or changes, and those verdicts are usually thrown away once the PR merges, left in CI logs and PR comments and never linked back to the agent run or the prompt that produced the code](/blogs/software-factory-tests-its-own-prompts/software-factory.png)

A software factory is a pipeline where an issue goes in one end and a merged, released change comes out the other, with AI agents doing the work at each station. Humans still steer, but they do it by writing the issue and making calls at a few gates, not by writing code.

Dan Shapiro's [five levels of AI-assisted programming](https://www.danshapiro.com/blog/2026/01/the-five-levels-from-spicy-autocomplete-to-the-software-factory/) is a good way to define the different stages of your journey, from basic AI-assisted coding to a full software factory. At level 3, *"You spend your days reviewing code. So much code. Your life is diffs."* At level 5, the dark factory, *"It's a black box that turns specs into software."* Most teams I talk to are somewhere around levels 2 to 3 and wondering how to get further.

The teams furthest along take different views on how much humans should check. OpenAI's [harness engineering post](https://openai.com/index/harness-engineering/) describes about 1,500 merged PRs from three engineers and *"0 lines of manually-written code"*, where *"Humans may review pull requests, but aren’t required to."* [StrongDM's factory](https://factory.strongdm.ai/) goes further, with rules that code *"must not be"* written or reviewed by humans. They validate against hidden scenarios kept outside the repo, because *"A test, stored in the codebase, can be lazily rewritten to match the code."*

Agents are now good enough to game the checks they're scored against. My colleague Laurie Voss wrote about this in [AI benchmarks are breaking](https://arize.com/blog/agents-too-smart-for-benchmarks/), including an automated agent that broke eight major agent benchmarks, in one case with a ten-line script that forced the test framework to report every answer as passed.

What all of these have in common is that writing code is no longer the hard part, but knowing whether the code is any good is. Simon Willison [called that](https://simonwillison.net/2026/feb/7/software-factory/) *"the most consequential question in software development right now."* Spotify found their LLM judge [vetoes about a quarter](https://engineering.atspotify.com/2025/12/feedback-loops-background-coding-agents-part-3) of their background agent's sessions. And a 2026 study of [code review agents in pull requests](https://arxiv.org/abs/2604.03196) found PRs reviewed only by review agents merge 45.20% of the time, against 68.37% for human-only review.

So, checking is now the bottleneck. But a factory is full of checkers already: CI, reviewer agents, routers, review gates, reverts. Every one of them produces a verdict on the agents' work: pass or fail, approve or changes, ship or changes, reverted or not. In most factories, those verdicts stay in CI logs and PR comments once the PR merges, and nobody links them back to the agent run or the prompt that produced the code.

## The factory I built

I wanted the factory to build something fun, so the app is **ship-it-card**. You give it a merged GitHub PR and it gives you back a trading card for it, with a ship score, a rarity, stats from the PR, a crew list that flags coding agents, and art generated by Gemini. Here's the card for a Phoenix PR that added skeleton loaders (Gemini took that a bit literally):

![A ship-it-card trading card for an Arize Phoenix pull request that added skeleton loaders, showing Legendary rarity, a ship score of 99, three abilities taken from the PR stats and Gemini art of a factory line assembling cartoon skeleton monsters](/blogs/software-factory-tests-its-own-prompts/example-card.png)

I hand-built the first version, then let the factory build everything after that. The factory has these stations:

1. **Spec** turns the issue into acceptance criteria and a risk rating.
1. **Build** writes the code and tests, and the factory opens a PR.
1. **CI** runs GitHub Actions. If it fails, a **babysit** agent reads the logs and pushes a fix, up to three times.
1. **Review** runs three reviewer agents in parallel, one each for correctness, security and tests.
1. **Router** decides whether the PR can auto-merge or has to go to the review gate.
1. **The human review gate** is the final call before merge: `/ship` to merge, or `/changes` with notes to send it back to babysit.
1. **Release** smoke-tests the merged code, picks a version and writes release notes.

Here's a real issue going through the factory using a dashboard I built to visualize the flow of issues. This one gets sent back from the review gate, fixed, and shipped as v0.15.0.

![An animated flowchart of the software factory showing an issue token moving from spec to build, through CI, splitting into three reviewer tokens, passing the router, being sent back from the review gate for changes, fixed by babysit and finally released as v0.15.0](/blogs/software-factory-tests-its-own-prompts/factory-run.gif)

Every station is its own agent using the [Claude Agent SDK](https://docs.claude.com/en/docs/agent-sdk/overview), with its own model, system prompt, tool allowlist, turn limit, and spending cap. Sonnet does the spec, build, babysit, routing and release work, and Opus does the reviews. The agents never touch GitHub. Instead, they return structured JSON, and plain Python does the committing, pushing, commenting, and merging. That keeps the agents' blast radius small and makes every GitHub action deterministic.

The router is an agent sitting on top of a set of hard coded rules. If a reviewer asks for changes, or the change is big or deletes tests, the PR goes to the review gate whatever the agent thinks. Both decisions get recorded on the trace: what the agent wanted to do, and whether a rule overrode it. That means I can score the agent's own judgement separately from the rules, which is how I later caught it being far too cautious.

## You can't evaluate what you can't see

Every issue is a single trace in Arize AX. The factory creates a `factory.run` root span per issue, with one `station.*` span per station under it. The [OpenInference instrumentor for the Claude Agent SDK](https://arize.com/docs/ax/integrations/python-agent-frameworks/claude-agent-sdk/claude-agent-sdk-tracing) then adds an agent span under each station, with a tool span for every file read, grep, and test run.

![The Arize AX trace tree for one factory run, showing the factory.run root span with station spans for spec, build, CI, the three reviewers and the router, each with ClaudeAgentSDK.query agent spans and tool spans underneath](/blogs/software-factory-tests-its-own-prompts/trace-tree.png)

- **One trace per issue.** When a PR is parked at the review gate and the run picks up again hours later, the resumed work joins the same trace. The whole life of an issue reads as one story.
- **Prompt versions on every agent span.** The prompts live in Arize AX [Prompt Hub](https://arize.com/docs/ax/prompts/prompt-hub), and each station loads whichever version is labelled `production` when it runs. The agent span records the prompt name and version, so I can always tell which prompt produced which behavior.
- **Issue and PR numbers on every span.** That's the join key for everything that happens later on GitHub.

## Every gate is a label

![The review flow: a PR with green CI goes to three reviewer agents for correctness, security and tests, which each approve or ask for changes. The router then auto-merges it or sends it to the human review gate, which replies /ship or /changes, with changes going back to babysit. A harvester compares each reviewer's verdict with the gate's first verdict and writes labels onto the issue's trace](/blogs/software-factory-tests-its-own-prompts/review-flow.png)

This is where the factory starts paying for itself. Every PR gets judged twice. First, the three reviewer agents each approve it or ask for changes. Then, unless the router views it as trivial and auto-merges it, it goes to the human review gate, which replies `/ship` or `/changes`. The gate has the final say, so its verdict is the closest thing the factory has to ground truth.

That makes the gate's verdict a free label for the reviewers. A small harvester script runs continuously, reads each factory PR from GitHub, and writes what happened back onto that issue's trace as annotations. That includes the verdict from the human review gate, whether CI passed first time, how many babysit fixes it took, whether it merged, and whether it was reverted within seven days.

![A two-by-two grid comparing the reviewer agent's verdict with the human review gate's first verdict. Approve and ship is agree. Approve and changes is a miss. Changes and ship is a false alarm. Changes and changes is agree](/blogs/software-factory-tests-its-own-prompts/label-matrix.png)

Then the harvester compares each reviewer with the gate's first verdict and gives it one of three labels:

- **Agree:** they gave the same answer.
- **Miss:** the reviewer approved, but the gate asked for changes or the PR was reverted later.
- **False alarm:** the reviewer asked for changes, but the gate shipped it.

A miss is the potential to ship a bug. A false alarm wastes time and teaches everyone to ignore the reviewer, [normalization of deviance](https://en.wikipedia.org/wiki/Normalization_of_deviance) and all that. I track them separately because a single agreement score would hide which problem you have. Only the gate's first verdict counts. When the gate asks for changes, babysit fixes the PR and it goes straight back to the gate, not through the reviewers again. So the first verdict is the only one the reviewers can be compared against.

## Finding gaps in the reviews

The first real misses came in a batch of PRs where I'd written issues designed to tempt the builder into subtle mistakes, as a deliberate attempt to find gaps in the factory.

On PR #34, the builder added pagination so the card would fetch every page of a PR's reviews. All three reviewers approved. The review gate sent it back: the code that builds the crew list never reads the reviews, so fetching more of them changes nothing on the card, even though the spec says reviewers count as crew.

On PR #38, which added support for private repos, all three reviewers approved again. The gate found an explicit token that gets silently ignored when a client is also passed in, plus an oversized token echoed back in an error response.

That gave me two misses on real code, sitting on real traces, with the gate's reasons attached. I could then use these as data to improve the factory.

## Judges you can trust (eventually)

A verdict-level label only tells you that a reviewer approved something the gate didn't. It doesn't tell you whether the problem was in that reviewer's area. If the security reviewer misses a security bug, that's a miss. If the tests reviewer misses it, that's arguably not their job.

Each time the gate reviews a PR, the factory writes a `reference.review` span into that PR's trace with the diff, the spec, the gate's findings and all three reviews. An Arize AX [online evaluation task](https://arize.com/docs/ax/evaluate/online-evals) runs four LLM-as-a-judge evaluators on every new one. Three are miss judges, one per reviewer lane, asking whether that reviewer missed a serious issue in its own area. The fourth checks whether the diff meets every acceptance criterion in the spec.

![The reference.review span for PR #38 in Arize AX with four evaluation results: factory_miss_correctness marked missed in red, and the tests, security and spec adherence judges marked as passing in green](/blogs/software-factory-tests-its-own-prompts/reference-evals.png)

I didn't trust the judges straight away. Like the application code, they are living artifacts that you need to build, test, and iterate on.

The first version of the miss judges blamed the correctness and tests reviewers for a Server-Side Request Forgery (SSRF) bug that clearly belonged to security. The fix was one rule in the judge prompt: each finding has a single owning lane. With that version, the two misses landed where they should.

I tested the spec judge prompt the same way. I wrote a second version that also checked the spec's stated goals and assumptions, and it read much better. Before promoting it, I ran both versions over the same 19 PRs and compared them with the gate's verdicts. The new version agreed with the gate on 13, against 14 for the old one. It failed a PR for something no diff could show, and it still passed #34. So it didn't get promoted. A judge is just another prompt, and it needs the same testing before it goes live.

## The improvement loop

Now for the part I actually wanted to build: using those misses to make the correctness reviewer better, and proving it worked before letting it anywhere near production.

The first step was a dataset. I took the 19 PRs the gate had reviewed and saved them as an Arize AX [dataset](https://arize.com/docs/ax/develop/datasets), each one pinned to the exact commit the reviewers first saw, with the gate's verdict and findings alongside.

![The factory-reviewer-gate-disagreements dataset in Arize AX with 19 examples, each showing the reference review text and a reference verdict of ship or changes](/blogs/software-factory-tests-its-own-prompts/dataset.png)

An experiment runs a reviewer prompt across every example, using a real Opus agent in a read-only checkout at that commit.

![The experiment loop: the dataset of 19 PRs runs through both the production prompt and a candidate prompt. A real Opus reviewer agent reviews each PR in a read-only checkout, three runs per prompt. An LLM judge counts misses and a code eval counts false alarms. A promotion gate asks whether the candidate has fewer misses and no more false alarms. If yes, the production label moves to the candidate. If no, the current prompt stays](/blogs/software-factory-tests-its-own-prompts/experiment-loop.png)

The correctness miss judge scores each review, and a code eval counts false alarms. Then there's a promotion gate: a candidate prompt only moves to `production` if it has fewer misses than the current one and no more false alarms. A prompt change gets tested the same way a code change does before it ships.

### The first fix didn't work

My first attempt came from intuition. Both misses felt like the reviewer was not following the data far enough, so the new prompt told it to *"Follow the data to where it's used."* For every value a change adds or fetches, find the code that consumes it and confirm it changes what the user sees.

It made no difference at all. The old prompt missed problems in 2 PRs, #34 and #38. The new prompt missed problems in the same 2 PRs, and the traces showed why.

On #34, the old reviewer had actually *noticed* that the code that builds the card's crew list never reads reviews. It wrote that down, decided it was out of scope, and approved anyway. The new reviewer did exactly as it was told, followed the reviews to the first place they were used (a reviewer count), decided that was fine, and approved too. My instruction gave it a better way to justify the code instead of checking the code against the spec.

So the reviewer wasn't failing to look. It was looking, finding the gap, and waving it through. That's a calibration problem, and no amount of "look harder" was going to fix it. Without the experiment, I'd have shipped that prompt feeling pretty pleased with myself.

### The second fix did work

For the next candidate I took a more data-driven approach, using the same pattern as the [prompt optimization](https://arize.com/docs/ax/prompts/prompt-optimization) flow in Arize AX. An optimizer step read the judges' explanations for every miss, plus the failed attempt, and wrote a new prompt. It added three rules:

- **Spec goals are in scope.** The spec's stated goals and assumptions count, not just the numbered criteria. If the code doesn't make them true, that's a major finding, even if the gap is in code the PR didn't touch. *"Never mark something as "out of scope", "pre-existing" or a "note" and then approve when the spec relies on it."*
- **Check every branch of a changed function.** List each branch in one line and say whether the new value is applied there, including branches no current caller uses.
- **Write-ups become findings.** Any mismatch the reviewer notices has to appear as a finding with a severity, not tucked away in the summary.

Opus doesn't give the same answer every time, so this time I ran each prompt three times across all 19 PRs.

![The Arize AX experiment analysis for the factory-reviewer-gate-disagreements dataset, plotting the correctness miss rate across seven experiments: four runs of the original prompt between about 10% and 16%, then three runs of the new prompt at 0%](/blogs/software-factory-tests-its-own-prompts/experiments.png)

The original prompt missed 2, 3 and 2 PRs across its three runs. It missed #34 and #38 every single time. The new prompt missed none, in all three runs, with no false alarms either. (The chart has four runs of the original, because the first experiment's baseline is in there too.)

The promotion gate passed, and moved the `production` label in Prompt Hub to the new version. The next issue through the factory used it, with no code change and no redeploy.

I used the same 19 PRs to work out what was wrong and to test the fix, so this is an in-sample result. It shows the fix addresses the failures I found. It doesn't yet show the reviewer is better on code it's never seen.

## Does it hold up on new code?

To test that, I ran a third batch of issues through the factory with the new prompt live. Four of them were designed to invite the same kinds of bug the reviewer had missed. The new reviewer didn't miss anything the gate caught. But most of the traps didn't spring, because the builder got them right the first time, so "no misses" mostly meant there was nothing to miss.

I then tried a more controlled test. I took eight merged PRs and planted one known correctness bug in each: five of the same kind as the misses, like a `--show-bots` flag silently ignored when you also pass `--json`, and three other kinds, like an off-by-one. I added five untouched PRs as controls, and ran both prompts three times each.

Both prompts caught all eight planted bugs in every run, and both approved all five clean PRs every time. That tells me the new prompt didn't break anything and didn't add any false alarms. It can't show the improvement, though. A planted bug that plainly breaks the spec is much easier to catch than the real misses, where the reviewer spotted the gap and talked itself out of it. A held-out set of real disagreements is what this needs, and the only way to get one is to keep the factory running and keep harvesting.

The review gate isn't perfect either. In the third batch it made two mistakes. On #42 it asked for changes over a dependency that an earlier PR had already added. On #46 it shipped a rate limiter with a hole that the security reviewer had correctly flagged. So the ground truth needs checking too. I'd audit a sample of gate verdicts regularly rather than trusting them blindly.

## Improving the router

The same loop works on other agents, too. The router is the agent that decides whether a PR is safe to auto-merge or has to go to the review gate. In the second batch it sent all eight PRs to the gate, so the factory wasn't saving any review time at all. Its prompt treated any change to rendering as risky, and in an app that renders trading cards, that's every change.

I fixed it with the same dataset, experiment and promotion gate as the reviewer. The difference is the scoring. To score a reviewer, you need an LLM judge to read the review and decide whether it missed something. To score the router, you only need two facts the factory already records: where the router sent the PR, and what the gate did with it. Comparing those is a few lines of code:

- **Correct:** the router sent the PR to the gate and the gate asked for changes, or the router would have auto-merged it and the gate shipped it unchanged.
- **Unnecessary review:** the router sent the PR to the gate, and the gate shipped it unchanged.
- **Unsafe:** the router would have auto-merged the PR, but the gate asked for changes.

I ran the old and new router prompts three times each across 17 PRs. The old prompt sent 9 of them to review unnecessarily, and the new one sent 6, with no unsafe auto-merges from either. That passed the promotion gate, and the new router went live through Prompt Hub.

All of this rolls up into a "Software factory health" [dashboard in Arize AX](https://arize.com/docs/ax/observe/dashboards), showing how runs are routed, first-pass CI, misses by reviewer lane, reviewer verdicts against the gate, cost and spec adherence. The factory ran in batches, so the charts come in bursts.

![The Software factory health dashboard in Arize AX showing charts for runs by route (auto-merge versus review gate), CI green first time with babysit fixes, reviewer miss rate by lane from the LLM judge, and reviewer verdicts against the review gate](/blogs/software-factory-tests-its-own-prompts/dashboard-charts.png)

## The factory that grades its own work

OpenAI's harness post says that *"Review comments, refactoring pull requests, and user-facing bugs are captured as documentation updates or encoded directly into tooling."* That's the right instinct. Feedback from the gates should flow back into the agents. What I wanted was a way to know whether each change to an agent made the factory better or worse.

Building a factory was the easy part. The harder, and more fun, part is the improvement loop: keeping every verdict the gates produce, joining it to the traces, and using it to test every prompt and every judge before it reaches production. If you're building one, start harvesting those verdicts on day one. Your future self will want that dataset.
