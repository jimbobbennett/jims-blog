---
author: "Jim Bennett"
date: 2026-07-24
publishDate: 2026-07-24
description: "Your eval criteria already exist, scattered across the PRD, the Jira tickets, and the shipped code. Mining them into one rubric does two jobs: it grounds the eval in what the system was meant to do, and it shows you early whether the thing you built is still the thing you meant to build. A companion to the context graph post: same move, different source."
draft: false
slug: "your-eval-criteria-are-already-written"
title: "Your eval criteria are already written, just scattered across three systems"
tags: ["ai", "evals", "requirements", "llm-as-judge", "annotation", "arize-ax"]
featured_image: cover.png
---

In [an earlier post](https://arize.com/blog/self-improving-agent-with-context-graph) I built a self-improving agent by mining a context graph out of data the team already had. The source of truth wasn't in a spec, it was in the traces: every time a human reviewer overrode the agent, that override was a signal, and joined together across hundreds of decisions those signals told you what the agent should have done. Mine them, feed the patterns back, and the agent gets measurably better without retraining a thing.

That post was about runtime, what the agent did, and how people corrected it. This one is about the other end of the timeline, and it turns out to have the same shape.

Before you can tell whether an agent did the right thing, you need a definition of **right**. And that definition almost never lives in one place. It's split across the product requirements doc, the Jira ticket where the edge case got renegotiated, and the function nobody documented that quietly encodes the real rule. You already wrote the eval criteria, but you wrote them three times, in three systems, and never joined them up.

## The requirements diaspora

![Three columns — PRD, tickets, and code — each telling a different story and diverging toward the question of which is the source of truth](/blogs/your-eval-criteria-are-already-written/requirements-diaspora.png)

Think about where the actual spec for an AI feature lives by the time it ships.

The PRD holds the intent. It's the clean story: here's what we're building, here's who it's for, here's what good looks like. It was also written before anyone hit the hard parts, so it's the least accurate of the three by the time you're evaluating.

The tickets hold the negotiation. This is where "actually, do it this way" lives, buried in a comment thread on a ticket that was closed four months ago. The edge cases, the reversals, the "we'll handle that later" that became permanent. If you want to know why the agent behaves the way it does, the answer is usually in a Jira comment, not the PRD.

The code holds what actually shipped. Including the rules nobody wrote down anywhere else: the threshold someone hardcoded, the special case for one customer, the fallback that fires more often than anyone realizes.

These three drift apart, and the drift is not a bug in your process, it's the default. Keypup describes it as [context drift](https://www.keypup.io/blog/why-your-pull-requests-and-jira-issues-are-out-of-sync-and-how-ai-powered-analytics-can-fix-it/) between your tickets and your code: *"at any given moment, the two systems tell different stories."* Their sharper line is the one worth pinning up: *"Gaps between what a ticket describes and what a specification actually defines are where most production bugs start their life."* Jama makes the same point about specs and implementation, where the [traceability gap](https://www.jamasoftware.com/blog/ai-requirements-management/) between the detailed requirement and what engineering built often isn't caught until sprint review.

So the source of truth exists. It's just fragmented, and the fragments disagree.

## Why this breaks AI evals specifically

![Two panels — traditional software with tests pinned to code catching drift, versus an AI system with a rubric floating disconnected from requirements while the eval passes green](/blogs/your-eval-criteria-are-already-written/why-it-breaks-evals.png)

Traditional software has a defense against this. The tests live next to the code, they run on every change, and a red build tells you something moved. The spec is imperfect, but the test suite pins the behavior down.

AI systems don't get that for free. A model is non-deterministic, so you can't `assert output == expected`. Instead you judge quality against a rubric, either with human labelers or with an LLM acting as a judge. And here's the problem: that rubric usually gets invented from scratch. Someone sits down in a fresh doc and writes out what good looks like, disconnected from the PRD, the tickets, and the code that already defined it.

There's a popular framing that building this rubric is fundamentally a product exercise, that it's essentially writing a PRD for AI behavior. That's half right, and the wrong half is the expensive one. You don't need to author a PRD for AI behavior. You already have one, well three, actually. Writing a fresh rubric means re-deriving requirements that already exist, and re-deriving them badly, because the person writing the rubric doesn't have the Jira comment or the hardcoded threshold in front of them. You end up evaluating against a guess.

Even a passing eval doesn't save you here, and this is the part that should worry you. Tricentis has a name for it: [intent drift](https://www.tricentis.com/blog/intent-drift-ai-code-fix-regression-blind-spots), *"the gradual divergence between what code actually does and what it was originally designed to do."* Their line lands harder in the eval context than the code one: *"A green pipeline doesn't mean your code still does what you intended."* If your rubric was invented separately from your requirements, a green eval run tells you the system matches the rubric. It tells you nothing about whether the system still matches what you meant to build. You can pass every check and have quietly shipped something nobody asked for.

## Mining requirements into one source of truth

![A mining agent reads the PRD, Jira tickets, and source code in one run, extracts structured requirement nodes, and surfaces the conflicts between them as the signal](/blogs/your-eval-criteria-are-already-written/mining-source-of-truth.png)

This is the same move as the context graph, pointed at a different corpus.

In the context graph post, a mining agent read the traces and extracted structured nodes: the request, the decision, the override, the precedent it set. Here, you point an agent at the three requirements systems and extract requirements the same way, as structured nodes rather than prose. A requirement, the source it came from, its acceptance criteria, and the ticket where it last changed. The [Claude Agent SDK](https://docs.claude.com/en/api/agent-sdk/overview) is well suited to this: it traverses a repo natively, and with the right MCP tools wired up it can also read a Confluence space and walk a Jira project in the same run, which is exactly the three-system sweep the job needs.

The interesting output isn't the clean list of requirements. It's the conflicts. When the PRD says one thing, the ticket renegotiated it to another, and the code does a third, that disagreement is the most valuable thing the mining produces. Tricentis arrives at nearly the same recipe from the code-quality side, arguing you have to look at [three inputs together](https://www.tricentis.com/blog/intent-drift-ai-code-fix-regression-blind-spots): the original intent, the current result, and the changes that got you from one to the other. Swap in PRD, code, and tickets and you have the reconciliation this post is about. The conflicts are where drift is hiding, and surfacing them is half the value before you've evaluated anything.

Treating the code as a first-class requirements source is not a hack, either. The [ReqToCode work](https://arxiv.org/html/2603.13999) argues traceability should be a structural property of the codebase rather than a matrix bolted on afterward. The code isn't just the implementation. It's a requirements document that happens to be executable, and it's the closest of the three to what actually shipped — with the caveat that for an AI system the deployed prompt, model version, and runtime config often live outside the repo, so the code is authoritative about the logic, not the whole system.

## From source of truth to a grounded eval

![A Cohen's kappa scale from 0 to 1, marking a miscalibrated judge at 0.31, production-acceptable judge-to-human agreement at 0.60, clear-rubric human agreement at 0.70, and strong agreement at 0.80](/blogs/your-eval-criteria-are-already-written/kappa-payoff.png)

Once the requirements are mined and reconciled, they stop being documentation and become eval infrastructure.

Acceptance criteria become pass/fail checks. The edge cases you dug out of ticket comments become test cases in your dataset. The undocumented rules in the code become graders. The rubric isn't authored, it's compiled from a source of truth that already carried the answers.

And this is where grounding stops being a nice word and starts being a number. Vague rubrics fail measurably. FutureAGI's [work on LLM-as-judge](https://futureagi.com/blog/llm-as-judge-best-practices-2026) puts it bluntly: *"A vague rubric prompt produces a vague judge."* They track it with Cohen's kappa, the standard measure of agreement between two labelers beyond chance. A human pair should hit kappa of at least 0.7 for you to trust the rubric is clear. A judge that agrees with humans at 0.6 or above is acceptable for production, 0.8 is strong, and a miscalibrated judge working from a fuzzy rubric can fall as low as 0.31. Maxim frames the same idea from the annotation side: you want acceptance criteria specific enough that [two experts reach the same conclusion](https://www.getmaxim.ai/articles/guide-to-managing-human-annotation-in-ai-evaluation-best-practices/) independently, because *"your evaluation system is only as good as its source of truth."*

Grounding the rubric in mined requirements is what moves those numbers. When a labeler judges an output, they're not guessing against vibes. They're checking it against the acceptance criterion that came from a real ticket, so two labelers reach the same verdict, and the LLM judge you calibrate against them inherits that clarity.

There's a second payoff, and for my money it's the bigger one. A rubric built from how the system actually works, code and tickets and PRD reconciled, is a mirror you can hold up early. Show it to the people who asked for the feature before you run a single eval. If the mined rubric describes an app they don't recognize, you've caught the drift while it's still cheap to fix. The requirements moved, the code followed, and nobody stepped back to check the result was still the thing they wanted. The reconciled rubric surfaces that mismatch before you waste a cycle evaluating against the wrong target.

## The rubric is a first draft

None of this means mining hands you a finished rubric. It hands you version one.

The honest version of this is that criteria don't fully emerge from a spec at all. As Lenny's guide to eval systems puts it, [criteria emerge from grading](https://www.lennysnewsletter.com/p/building-eval-systems-that-improve): *"the first version of any rubric is wrong in ways you can't predict until you watch it fail on real examples."* You mine the requirements, you compile the rubric, and then you grade real output against it, and the grading is what exposes where the requirements were ambiguous, contradictory, or silent.

That's a loop, and it's the same loop as the context graph. There, each cycle of mining and feedback improved the agent, from 53.8% agreement to 76.2% and up toward a plateau. Here the loop improves something one level up: the definition of correct. Grading reveals a gap, the gap points back at an ambiguous requirement, you resolve it in the source, and the next rubric is sharper. The context graph tightened what the agent does. This tightens what you measure it against.

## Don't leave your requirements fragmented

The closer from the last post applies here almost word for word: don't throw your data away. You already wrote the requirements. The failure isn't missing knowledge, it's leaving it scattered across three systems that disagree.

Whether the source of truth is override signals in your traces or acceptance criteria in your tickets, the job is the same. Mine the systems you already have, join the fragments nobody joined, and reconcile them into one thing you can evaluate against. Do that and you get two wins at once: an eval grounded in what the system was meant to do, and an early warning the moment the thing you built stops being the thing you meant to build.
