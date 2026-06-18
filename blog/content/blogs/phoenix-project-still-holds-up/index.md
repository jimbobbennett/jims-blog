---
author: "Jim Bennett"
date: 2026-07-10
publishDate: 2026-07-10
description: "I reread The Phoenix Project and asked whether Gene Kim's 2013 DevOps framework still applies to AI agents. Most of it does. The parts that hold up are the parts you'd expect — and the part that aged the best is the one about Brent."
draft: true
slug: "phoenix-project-still-holds-up"
title: "The Phoenix Project still holds up, even if you replaced all the code with agents"
tags: ["ai", "agents", "devops", "phoenix-project", "evals", "observability"]

images:
  - /blogs/phoenix-project-still-holds-up/banner.png
  - /blogs/phoenix-project-still-holds-up/translation.png
  - /blogs/phoenix-project-still-holds-up/work-centers.png
featured_image: banner.png
---

I reread [The Phoenix Project](https://bookshop.org/p/books/the-phoenix-project-a-novel-about-it-devops-and-helping-your-business-win-gene-kim/f604a0a3952a6b88?ean=9781950508945&next=t) last month. I do this every year or two — it's one of those books that gets better the more production systems you've shipped, because each time you've broken your environment in a new way since the last read.

This time the question that wouldn't leave me alone was a different shape. Half the work I do now involves agents, the other half is shipped by people who work with agents. Code that used to be written deterministically is now produced by a system that's confidently wrong often enough that you have to check. Tests that used to be authored before the code now get generated *from production traffic*. The artefacts I'd built a career around had all been replaced.

So I sat there reading Erik teach Bill about the Four Types of Work and thinking: does any of this still apply? It's a 2013 book set in a factory analogy from a 1984 book that's about scheduling MRP through bottleneck machines. Has anything Gene Kim wrote survived contact with non-deterministic agents?

The answer, surprisingly, is yes. Most of it still holds up. And the parts that don't hold are the parts you'd expect — the bits that were always specific to deterministic code, like binary test pass-fail and after-the-fact postmortems. The architecture survives because the book was never really about code. It was about the movement of work through a constrained system. Code was just the artefact that moved.

I want to walk through what survived, what didn't, and what I'd tell a team setting up to ship agents on Monday morning. Some of the survival is obvious — telemetry and feedback loops were always going to matter more for non-deterministic systems, not less. Some of it took the re-read to see, and I'll show you the bit I missed both times before.

It matters because something has gone wrong at the population level. DORA's 2024 report found that for every 25% increase in AI adoption inside a team, throughput drops 1.5% and delivery stability drops 7.2%. That's the opposite of every prior DORA finding about pipelines, automation, and small-batch flow. Whatever's going on, the framework either explains it or it doesn't.

## Two Phoenixes

Quick disambiguation before we go anywhere. *The Phoenix Project* is Gene Kim's 2013 DevOps novel. **Arize Phoenix** is the open-source agent observability project from Arize, the company I work for. Same word, no relationship. The book has nothing to do with Phoenix the tool, and this post is about the book.

## Why it should not hold

The case against the framework surviving is real, and worth stating properly.

The DORA finding above is the most uncomfortable piece of it. Adding the most powerful productivity tool of a generation is making delivery *worse*. If Kim's framework predicts elite performers can have both throughput and stability, the early agent era is contradicting it.

Then there's Charity Majors, who saw this coming in September 2023. The person who popularised observability in modern software wrote a piece called *LLMs Demand Observability-Driven Development*. The argument: LLMs break the test-driven development assumption that you can write your tests before the code. *"With software, you typically start with tests and graduate to production. With ML, you have to start with production to generate your tests."* The pipeline runs backwards. That's not a small caveat. That's an inversion of one of the most basic premises Kim's deployment pipeline rests on.



Hamel Husain has been saying the practitioner version of this since 2024 in *Your AI Product Needs Evals* and the follow-up *Field Guide to Rapidly Improving AI Products*. He's seen 30+ AI deployments, and his diagnosis is sharp: *"Teams invest weeks building complex AI systems, but can't tell me if their changes are helping or hurting."* The feedback loop the Three Ways assume — change, observe, learn, repeat — doesn't run if you don't know whether your change helped.

There's also a category of failure that traditional DevOps doesn't have a name for. An agent can return a fast, schema-valid, fluent response that's factually wrong. APM doesn't see it, latency is green, error rate is green. The user gets a hallucinated answer and either acts on it or never trusts your product again. Kim's "unplanned work" — the predator that eats planned work — used to mean pager-duty incidents. Now it means an entire class of silent failure that has no signal in the traditional monitoring stack.

And there's the autonomy claim, which is genuinely incompatible with the framework. The whole point of *"You build it, you run it"* (Werner Vogels, ACM Queue, 2006) is that a human team owns the page when their system breaks. The marketing around "self-improving agents" implies that ownership transfers to the agent. If the agent is improving itself, who's getting paged when it ships a regression?

So that's the steelman. The pipeline runs backwards. The feedback loop is broken. There's a new class of silent failure. The autonomy claim breaks the accountability premise. The empirical data is pointing the wrong way. The framework should be dead.

It isn't. But it took me a re-read of the book — paying attention to the flow parts rather than the war-story parts — to see why.

## The artefacts changed

Here's what I noticed on this re-read that I'd missed the first three times. Kim isn't writing about code. He never was. Open The Phoenix Project to any random page and you'll find Brent dealing with a payroll system, or Bill arguing about an SAN, or Erik explaining a heat-treat oven from a manufacturing plant. The book is studiously indifferent to what the work *is*. It cares only about how the work moves.

That makes the framework portable. Every artefact in modern AI engineering is just a substitution of the manufacturing-and-then-software-engineering versions Kim already wrote about.

**Code became harnesses.** When you ship an agent, the thing you write isn't the model. The model is a dependency. The thing you write is the harness — the prompt, the tool definitions, the retrieval logic, the routing rules, the retry-and-reflection loop, the guardrail wrapping. It's where the work lives. Improving an agent's reliability is less about improving the model and more about improving the harness. Treat the harness like the system Kim cared about, and the rest falls into place.

**Tests became evals.** A traditional test is binary: did the function return the expected value? An eval is statistical: across a representative dataset, did the agent's behaviour stay within an acceptable distribution of correctness? You author them differently — evals tend to be LLM-as-a-judge prompts or code-based checks running against curated examples — but they do the same job. They're the executable specification. The deployment pipeline blocks a merge on a failing test suite; an eval pipeline blocks a merge on a failing eval run. Same gate. Different statistic.

**Telemetry became traces.** This is the cleanest mapping. Production agent systems emit spans for every LLM call, tool call, retrieval, reasoning step, and multi-agent handoff. Group those spans by session and you have the unit of work — the agent's equivalent of a deployment. The instrumentation contract is OpenInference, which is OpenTelemetry semantic conventions extended for GenAI. The principle Kim's Second Way rests on — *"if it moves, we track it."* — is back, just attached to a different kind of moving thing.

**Releases became eval-gated promotion.** A traditional deployment pipeline runs tests, blocks on failure, promotes on green. An agent pipeline runs evals against a curated dataset, blocks on threshold failure, promotes on pass. The Definition of Done shifts from "all tests pass" to "this candidate beats the baseline on the dataset that encodes what the system should do." A prompt change is a candidate. A model swap is a candidate. A retrieval re-index is a candidate. They all run the same gate. They all promote the same way.

**Incidents became regression dataset entries.** This is where the postmortem ritual genuinely breaks down — and we'll come back to that — but the substitution itself is clean. A traditional incident produces a timeline, a contributing-factors list, and a set of corrective actions. With an agent, the artefact that prevents recurrence is a regression example — the specific input that failed in production, frozen into the eval dataset so the next candidate change has to handle it. The reproduce-and-prevent work the postmortem ritual does for systems is now done by the dataset.

**Daily work became improving the system that improves the agent.** Kim's slogan from the novel: *"Improving daily work is even more important than doing daily work."* In an agent shop, daily work is the agent's runtime behaviour. The work that improves daily work is everything one layer up — adding new evals when failure modes appear, expanding regression datasets, calibrating judges, updating prompts, tightening guardrails. The work that improves *that* is one layer up again. The Third Way wasn't about a specific kind of improvement work. It was about valuing that work as work.

Once you stop reading the book as being about code, the artefact replacements become obvious — and what's left underneath them is a framework that survives the swap.

## The architecture did not

Look at the substitutions together and what's underneath them is the same shape. The Three Ways are still there. Different artefacts, same flow.

**Flow.** Work still moves left to right. A change to a prompt, a model, or a tool definition needs to make it through experimentation, evaluation, and promotion to production before it produces value. *"until code is in production, no value is actually being generated"* — Kim wrote that in 2013, and the only word that's stale is "code." Replace it with "prompt" and the sentence is identical.

**Feedback.** Production tells you what went wrong. Online evaluators run continuously against live traces, raising alerts when faithfulness or tool-call accuracy crosses a threshold. Charity Majors saw this in 2023; Kim saw it in 2013; John Allspaw at Etsy had articulated the blameless-postmortem version of it in 2012. The mechanism is older than the noun.

**Continual learning.** Kim extended his own framework into the AI era in *Vibe Coding* (2025, with Steve Yegge). His unifying principle for AI-assisted work — *"Prevent problems, detect issues early, correct course quickly."* — is the Three Ways with the word "AI" added. The application needed an extension; the framework didn't.

What survives across all three is the part Kim was most insistent on. *"You build it, you run it"* (Vogels, 2006) is the precondition. Twenty years later, Kim restates it in *Vibe Coding*: *"Delegation of implementation doesn't mean delegation of responsibility. Your users, colleagues, and leadership don't (or shouldn't) care which parts were written by AI — they rightfully expect you to stand behind every line of code."* Same principle, two decades apart. The agent is a tool, not a colleague.

That's the part of the framework that didn't need to change. It was already the abstract version.

![Diagram: a two-column comparison showing six artefact substitutions from the deterministic-software era (code, tests, telemetry, releases, incidents, daily work) to the agent era (harnesses, evals, traces, eval-gated promotion, regression dataset entries, improving the system that improves the agent), with the Three Ways — Flow, Feedback, Continual Learning — labelled as unchanged underneath.](/blogs/phoenix-project-still-holds-up/translation.png)

## The constraint moved

The most useful idea in the entire Phoenix Project isn't the Three Ways. It's the bit about Brent.

If you've read the book you remember Brent — the engineer through whom every change ends up being routed. Every incident pulls him into firefighting. Every "improvement" elsewhere just queues more work behind him. Erik teaches Bill that *"Any improvements made anywhere besides the bottleneck are an illusion."* — borrowing directly from Goldratt's Theory of Constraints. The framework's whole operational lever, the thing it tells you to *do*, is: find your Brent, exploit his capacity, subordinate everything else to him, elevate him, then go find the next constraint because it'll have moved.

Agent teams have a Brent too. He's just not a person anymore.

Here's the move that took me the longest to see. AI did not remove work centers from the value stream. It added stochastic ones. Codegen agents are work centers. Eval gates are work centers. LLM-as-judge evaluators are work centers. Labelling queues are work centers. Datasets are work centers. Guardrails are work centers. Harnesses are work centers. Each has a queue, a throughput rate, a setup cost, and a rework rate. What changed is that several of those work centers are *probabilistic*. Their outputs vary even with the same inputs.

![Diagram: two work centers side by side. The deterministic one on the left takes an input, runs it through a single processing step, and produces a tight cluster of outputs — low variance, low rework. The stochastic one on the right takes the same input, runs it through a probabilistic processing step, and produces a wide spread of outputs with an arrow looping back as rework. Footer: AI raises throughput at the work centers that got AI. It raises rework at the work centers AI feeds into. That's the DORA finding.](/blogs/phoenix-project-still-holds-up/work-centers.png)

This is the mechanism behind DORA's 2024 finding. AI adoption raises throughput at the work centers that got AI — codegen, drafting, summarisation. It raises rework at the work centers AI feeds into — review, testing, production support. If the rework rate goes up faster than the throughput, delivery stability degrades. That's the −7.2% number, in operational terms. The framework didn't fail. It predicted exactly this. Kim is explicit that improvements not made at the constraint are illusions, and dumping output volume into a downstream work center that can't process it is the textbook anti-pattern.

So who's Brent now? On most agent teams I've seen, he's one of:

- **The dataset.** Your golden and regression sets are too small to catch real production failure modes. Evals pass; production fails. Elevating means investing in dataset curation — promoting failed traces into the regression set, expanding coverage, getting humans to annotate the edges. Not in shipping faster.
- **The annotator.** Labelling queues back up. You can't train an LLM-as-judge because you don't have enough labelled disagreement data. You can't expand the golden set because nobody's looking at the candidate examples. Elevating means hiring SMEs, or shifting work to synthetic-dataset generation, or both.
- **The evaluator.** The judge has drifted. Or the code-based check is measuring the wrong thing. Or the eval is so loose that everything passes. Elevating means investing in evaluator authoring and calibration, not in candidate-change throughput.
- **The harness.** The agent is misbehaving because of how the routing or the planning or the tool definitions are structured, not because the model or the prompt is wrong. Adding evaluators won't move this metric. The constraint is one level up.

The bottleneck moved. Kim told you it would. Step 5 of Goldratt's Five Focusing Steps is "go back to step 1" — because the constraint always moves once you elevate it. The corollary every agent team underestimates is that the constraint will move *again* once you've fixed the dataset, and *again* once you've fixed the evaluator, and *again* once you've fixed the harness. A working agent program is one that knows which constraint it is currently working on.

DORA's 2025 report sharpens this further. *"AI's primary role is as an amplifier, magnifying an organization's existing strengths and weaknesses."* That's exactly the Phoenix Project's argument restated for the AI era. Teams that already have flow discipline, feedback loops, and constraint awareness get faster. Teams that don't, get pulled apart by their own bottlenecks at higher speed. The framework didn't fail. It became more load-bearing.

That's the part of the book that aged the best. Not the chapters about flow, or feedback, or learning. The bit about Brent.

## Where Phoenix needs repair

The framework holds up, but it's not lossless. Three places where applying it 1:1 to agents would actually mislead you.

**The pipeline gate is probabilistic, not deterministic.** Kim's "no defects pass downstream" rule assumes a binary test suite. The eval gate is an LLM-as-judge or a code-based check producing a score distribution against a sampled dataset. Gates pass at thresholds, not at green. The rule becomes "no statistically significant regression passes downstream," which is contestable in ways the original wasn't — what's the sample size, what's the threshold, what's the judge's calibration drift. Charity Majors put the sharper version in 2023: *"With software, you typically start with tests and graduate to production. With ML, you have to start with production to generate your tests."* Production is the source of the test suite, not the destination of it. The First Way still works, but the gate it relies on is statistical, not binary.

**"Self-improving" is not autonomy.** The loop today is a human-in-the-loop loop with automation that progressively narrows the human role. Without the human-authored gates, an agent isn't improving — it's just changing. The framework is fine with this; what would break the framework is the autonomy claim itself. Vogels in 2006: *"You build it, you run it."* Kim in 2025: *"Delegation of implementation doesn't mean delegation of responsibility."* The principle scales down from service to agent without changing. Any "self-improving" framing that implies the human stops owning the production loop is doing rhetoric, not engineering.

**Blameless postmortems and the improvement kata don't transfer cleanly.** Both rituals were designed around the *human* loop — give engineers room to learn from failure without fear of blame; give them a structured daily routine for improving daily work. Apply them to agents and the rituals don't fit. There's no agent to be blameless toward. There's no daily coaching session with an LLM. The Third-Way *substance* survives — failed traces become regression entries, daily work includes building the systems that build better systems — but the rituals don't. Don't run a blameless postmortem on an agent failure. Run it on the team that owns the agent. The agent goes into the regression dataset.

A whole category of observability and eval tools now ships this loop as product — distributed tracing, online and offline evaluators, dataset curation, experiment-gated CI. Arize Phoenix is the open-source version of it; Arize AX is the commercial one. The framework was waiting for the products to catch up.

## What I'd do Monday

If you're building agents in production, here's what the re-read leaves me wanting to tell you.

**Instrument everything as traces.** Spans for every LLM call, tool call, retrieval, and reasoning step. Sessions for multi-turn work. Use OpenInference so you're not locked in. The Second Way doesn't work without telemetry, and telemetry doesn't work without a contract that survives your vendor choice.

**Promote production failures into your dataset.** When something goes wrong in prod, the artefact that prevents recurrence isn't a JIRA ticket. It's the failed trace, frozen into your regression set, so the next change you ship has to handle it. The dataset is your Definition of Done.

**Gate changes on evals in CI.** Treat a prompt change or a model swap the same way you'd treat a code change. Run the eval suite. Compare against baseline. Block the merge on a failing gate. The pipeline mechanic is unchanged from the deterministic era; only the test type is different.

**Find your current Brent.** Walk the work centers. Where's the queue? Is it the dataset waiting for annotation? The evaluator drifting out of calibration? The harness that needs restructuring? Wherever it is, that's the only work that moves the bigger metric. Everything else is the illusion Kim warned about.

**Run the loop, then improve the loop.** Then improve the system that improves the loop. The Third Way isn't a checkpoint you hit. It's the standing instruction.

The book was about flow through a constrained system. The constrained system is now an agent fleet. The flow is the same.

It still holds up.
