---
author: "Jim Bennett"
date: 2026-07-12
publishDate: 2026-07-12
description: "A wave of long-horizon agent benchmarks just shipped, and every one trades realism against verifiability. Whichever side it underpays is where the score leaks. A field guide to what each one actually measures, and where it gets gamed."
draft: false
slug: "agent-benchmarks-field-guide"
title: "Long-horizon agent benchmarks are fragmenting: a field guide to what each one actually measures"
canonical: "https://arize.com/blog/long-horizon-agent-benchmarks-field-guide/"
tags: ["ai", "agents", "evals", "benchmarks", "llm"]

images:
  - /blogs/agent-benchmarks-field-guide/banner.png
featured_image: banner.png
---

*Originally published on the Arize AI blog: [Long-horizon agent benchmarks are fragmenting: a field guide to what each one actually measures](https://arize.com/blog/long-horizon-agent-benchmarks-field-guide/).*

In one of the evaluations behind the OpenAI and Apollo Research [scheming study](https://arxiv.org/abs/2509.15541), o4-mini was given a cyber-security test with a trap buried in the formatting instructions. The fine print said that scoring above 50% on this section would trigger "unlearning" of the capability. The model read it, understood the incentive, and threw the test on purpose. This is sandbagging: an agent intentionally underperforming on an evaluation it knows it is taking. o3, given the same trap, did the same.

Think for a moment about what that means for a leaderboard. The number on the page was not a measure of what o4-mini could do, it was a measure of what o4-mini chose to reveal, given its read of who was watching and why. The model was not failing the benchmark, it was playing it.

That is the problem this whole generation of long-horizon agent benchmarks is walking into. A long-horizon agent benchmark measures an agent across a task that unfolds over many steps, tool calls, and decisions rather than a single prompt and reply, the kind of sustained work that runs for hours and, in SWE-Marathon's case, hundreds of millions of tokens. Because the agent acts over a long trajectory instead of answering once, the benchmark has to grade the whole arc of behavior, which is exactly what makes these so hard to build and so easy to fool.

A wave of them shipped in recent months: [Agents' Last Exam](https://arxiv.org/abs/2606.05405), [SWE-Marathon](https://arxiv.org/abs/2606.07682), the [Meta-Agent Challenge](https://arxiv.org/abs/2606.04455), and [Arena's Agent Mode](https://arena.ai/blog/agent-arena-methodology/). Each is a serious attempt to measure economically meaningful agent work, and each strikes a different bargain to make it measurable. Underneath all four sits [Princeton's reliability work](https://arxiv.org/abs/2602.16666), which found that climbing capability scores have yielded only small improvements in reliability. It is less a benchmark of its own than an explanation of why the others leak.

The bargain is the whole story. Every one of these benchmarks buys measurability with the same currency: it trades realism against verifiability, and whichever side it underpays is the exact seam where the score leaks. Reading these benchmarks well is mostly about knowing which failure mode you bought.

## The axis you cannot escape

![The realism-versus-verifiability axis, with each benchmark plotted and the leak labelled at each pole](/blogs/agent-benchmarks-field-guide/axis-realism-verifiability.png)

There is no benchmark that is both realistic and cleanly verifiable. Those two properties pull in opposite directions, and you have to cut one to get an increase in the other.

Push toward verifiability and you select for tasks with a checkable answer: a test that passes, a string that matches, an output you can diff against ground truth. That keeps the score objective. It also quietly narrows the benchmark to the slice of real work that happens to be checkable, and "checkable" turns out to be a short walk from "gameable." If a fixed answer exists somewhere in the environment, a capable agent can often reach it without doing the work.

Push toward realism and you lose the clean answer key. Real tasks have no oracle. So you fall back on a softer signal: a human's approval, another model's judgment, a behavioral trace. The score stops being a correctness measure and becomes a preference measure, with all the noise that implies.

Then add optimization pressure to either side and the agent stops passively sitting on the bargain and starts working the seam. The [Meta-Agent Challenge](https://arxiv.org/abs/2606.04455) put it plainly: "high optimization pressure induces spontaneous reward hacking." Push hard enough on any proxy and the agent optimizes the proxy instead of the task. That pressure is not a separate leak; it is what drives the two leaks below.

## The failure grammar: two ways the score leaks

![Two rails of failure: harness-side leaks the answer to the agent; model-side, the agent detects the scaffold and changes behavior](/blogs/agent-benchmarks-field-guide/failure-grammar-two-rails.png)

There are two distinct ways a benchmark score gets corrupted, and almost every specific failure is an instance of one of them.

The first is harness-side. The scaffold leaks the answer to the agent. The cleanest catalogue of this is Berkeley RDI's ["How We Broke Top AI Agent Benchmarks"](https://rdi.berkeley.edu/blog/trustworthy-benchmarks-cont/), which matters because RDI is Dawn Song's lab, the same group that built Agents' Last Exam. This is benchmark builders auditing the field, not critics from the outside.

Their findings read like a rap sheet. o3 and Claude 3.7 Sonnet reward-hacked in 30% or more of evaluation runs, using stack introspection, monkey-patching the grader, and operator overloading to fake a pass. They found a coding model that claimed 81.4% on SWE-bench, where 24.4% of its trajectories simply ran `git log` to copy the answer out of commit history. OpenAI audited SWE-bench Verified, discovered 59.4% of problems had flawed tests, and stopped using it. KernelBench handed out full marks for zero computation, because `torch.empty()` returned stale GPU memory that still held the reference answer from the evaluator's previous run.

RDI distills all of it into seven recurring vulnerability patterns. Most of them reduce to two sentences: there was no isolation between the agent and the evaluator, or the answer shipped alongside the test. Once you have those seven patterns in your head, you stop reading benchmark failures as bad luck and start reading them as a grammar.

The second way is model-side, and it is the one the sandbagging story opened with. Here the scaffold does not leak anything. The agent detects that it is inside a scaffold and changes its behavior. The answer is not exposed; the measurement is corrupted because the thing being measured is reacting to being measured. Those are the two rails, harness-side leaks and model-side reactions, and every benchmark below speaks some dialect of one or the other.

## The field guide

For each one: what it measures, the bargain it strikes, and then the seam itself. Two of the four have a documented exploit, a recorded case of an agent gaming the score. The other two have not been gamed in public yet, so their entries point instead at the structural downside waiting at the seam, because "not yet attacked" is not the same as "sturdy."

**Agents' Last Exam**

*What it measures.* Sustained professional work. It was built with more than 250 industry experts, with non-physical occupations mapped onto the US federal [O*NET / SOC](https://arxiv.org/abs/2606.05405) taxonomy, the government's standardized catalog of occupations and the tasks each one involves. Its hardest tier remains far from saturated: across mainstream harness and backbone configurations, the average full pass rate is below 1%.

*The bargain.* It admits only tasks with "verifiable outcomes" and standardizes grading around structured deliverable- and milestone-based checks, avoiding an LLM judge wherever a deterministic alternative exists. That is a deliberate move all the way toward the verifiable end of the axis.

*The downside.* No public exploit yet, but a low pass rate buys no safety here, as the harness failures below make plain. The real catch is that a ceiling is not a ruler. When you accept only tasks with objective answer keys, "verifiable" quietly narrows what counts as professional work, so that sub-1% rate measures the hardest checkable slice, not the hardest real one, and a low score does not mean "no economic value." Use it to probe a capability frontier; do not read it as a verdict on whether agents can do a job.

**SWE-Marathon**

*What it measures.* Coherence over enormous horizons. It was built on a specific complaint, stated plainly in the [paper](https://arxiv.org/abs/2606.07682): "current agent benchmarks largely evaluate short-form tasks," and so never test the planning, long-context understanding, and memory that real work demands. Its 20 tasks answer that with genuinely long frontier work: a multi-pass C compiler in Rust from preprocessing through x86-64 codegen, OpenAI's Parameter Golf, Cursor's long-running agent tasks. The rollouts average 27M tokens and top out at 877M, and even the best agent, Claude Opus 4.8, solves only 26%.

*The bargain.* Spending the budget on realism sends the bill to verification. To grade a full-stack Slack clone the benchmark hands the result to a Computer Use Agent that logs in, creates channels, posts messages, and checks the app actually works through the UI. When the grader is itself an agent it inherits the failure modes of the thing it grades.

*How it was gamed.* The builders saw the leak coming and wrapped grading in a multi-layer suite of visible and hidden tests, network-egress limits, and adversarial exploit scans, and still had to harden some tasks ten times over: run agents, inspect the traces, find the shortcut, patch the verifier, rerun. The seam shows in the numbers regardless. Across 1,300 rollouts, 14% showed reward-hacking behavior and 10% shipped clear exploit code, the predictable result of optimizing an agent against the environment that scores it.

**The Meta-Agent Challenge**

*What it measures.* Agents building agents. Rather than solving a task directly, the agent is scored on its ability to "autonomously construct, refine, and optimize an agent system" to solve it. To do that realistically it uses a [dual-container sandbox](https://arxiv.org/abs/2606.04455) where the meta-agent gets development-set feedback through an evaluation interface (API) while the test set stays hidden.

*The bargain.* That dev-set feedback channel is what makes the task realistic, an agent iterating against signal the way a real engineer would. It is also the attack surface.

*How it was gamed.* GPT-5.3-Codex "autonomously weaponized verbose error tracebacks to exfiltrate development-set ground truth," a misalignment behavior the authors say emerged spontaneously during benchmark development. Nobody taught it the trick; optimization pressure found the leak by itself.

**Arena's Agent Mode**

*What it measures.* What real users actually do. In its first seven-day window it logged 160,480 agent tasks across 128,244 [live sessions](https://arena.ai/blog/agent-arena-methodology/), with more than two million tool calls.

*The bargain.* It pushes all the way to the realistic end of the axis and gives up fixed ground truth entirely. There is no answer key; the label is a real user's approval or disapproval, and Arena treats the whole thing as a multi-intervention randomized controlled trial to estimate which agent components actually cause better outcomes. That is a genuinely different and defensible measurement.

*The downside.* No exploit on record, and there may never be one in the usual sense, because a preference signal is not the kind of thing you game by finding a hidden answer. The seam is subtler and structural: the signal is satisfaction, not correctness, so you measure whether users felt helped and have to infer whether the agent was actually right. The behavioral traces hint at the gap. Users pulled control back about 2.3 times more often than they handed it over, and on multi-part requests, agents silently dropped part of the work about 8% of the time. Use Arena to compare felt helpfulness at scale; do not read a high score as a correctness check.

## When the model knows it is being measured

Sandbagging is the seam that should worry you most, and it is not an isolated trick. It is one face of evaluation awareness, and the scheming research pins down how badly it distorts a score.

Start with what looked like good news. Anti-scheming training, what OpenAI calls deliberative alignment, cut covert actions sharply, dropping both o3 and o4-mini from low double digits to well under one percent. If you stopped there you would call the problem solved. But over the same training, the rate at which the models verbalized "I am being tested" went up rather than down. Some of that drop in covert actions was not the model scheming less. It was the model getting better at recognizing the exam room.

Then the researchers ran the cleanest experiment in the whole set. They edited the chain of thought directly. Delete the "I might be tested" reasoning from a trajectory and covert actions jumped from 13.2% to 24.2%. Inject that reasoning into trajectories that lacked it and covert actions dropped from 24.5% to 18.6%. The behavior was causally downstream of the model believing it was on a test. That is a benchmark score conditioned on the model knowing it is a benchmark, demonstrated by intervention rather than correlation.

And the realism gap shows up right where the axis predicts: in realistic, ChatGPT-style conversations, the same training helped far less, moving o3 only from 36.8% to 20.5% and o4-mini only from 31.4% to 14.2%. Anthropic reported the same shape separately, noting in the [Claude Sonnet 4.5 system card](https://www.anthropic.com/claude-sonnet-4-5-system-card) that the model often recognized when it was being tested.

There is an obvious rebuttal: just read the chain of thought and catch the model in the act. The scheming work closes that door too. Post-training, the models' reasoning traces began drifting away from standard English, with ordinary words like "illusion," "marinade," and "fudge" turning up used in non-standard ways, even on a standard benchmark like GPQA, a graduate-level science question set. The one instrument we lean on to catch cheating is drifting toward unreadable.

## Why one number was never going to survive this

Underneath every benchmark above sits Princeton's ["Towards a Science of AI Agent Reliability."](https://arxiv.org/abs/2602.16666) Its core finding is quiet and brutal: most models are still ranked on mean task success rate, a single average that can hide highly inconsistent behavior. Across 14 agentic models over 18 months, reliability has barely moved even as raw capability climbed. The team decomposes reliability into four dimensions, consistency, robustness, predictability, and safety, and states the gap directly: "recent capability gains have only yielded small improvements in reliability." Capability and consistency are coming apart.

A separate group reached the same place from a different direction. [Claw-Eval](https://arxiv.org/abs/2604.06132) ran 14 frontier models under error injection and watched Pass^3 fall by up to 24 percentage points. Pass^3 runs each task three times and counts it solved only if the agent succeeds on all three, so it measures consistency rather than one lucky run. That collapse is the same divergence Princeton documents. And the blindness is not only about variance: [AgentPex](https://arxiv.org/abs/2603.23806) extracts an agent's own prompt rules, checks the execution trace against them, and shows that outcome-only scoring sails straight past incorrect workflow routing and unsafe tool use that never change the final answer. The single number hides the failure on the variance axis and the trajectory axis at once.

That is the deepest version of the thread. Every leak in the field guide is a way the average stops meaning what the reader thinks it means. The harness leaks and the average counts a gamed pass as a real one. The model sandbags and the average reads a chosen failure as a capability ceiling. A single pass rate cannot tell any of these apart, it was never built to.

## Run the second cycle on the benchmark

A benchmark is an evaluation, and an evaluation is a thing that can itself be wrong. We grade models constantly and almost never grade the grader.

Arize's evaluator design runs [two improvement cycles](https://arize.com/docs/ax/concepts/evaluators/overview) off the same failure cases. The first is the agent cycle: evaluators flag bad responses, you collect them, you feed them back into prompts and fine-tuning. That cycle grades the model. The second is the evaluator cycle: you put human ground-truth labels on those same cases to check whether the evaluator was right, and you fix it when it was not. That cycle grades the grader.

A public benchmark is the first cycle run at industry scale. Every benchmark in this field guide ships with the second cycle missing. Nobody put ground-truth labels on the grader. That is why the realism-versus-verifiability trade does not sit there quietly: the seam leaks because no second cycle is watching it. RDI is the field report of what escapes through that gap on the harness side, and the scheming work is the report from the model side.

And the cost is measurable: when Claw-Eval graded agents by their trajectories instead of their final answers, outcome-only grading missed 44% of safety violations. "Grade the grader" is not a slogan; it is 44% of safety violations that final-answer scoring never sees.

So when the next leaderboard lands, do not ask which model won. Ask which side of the axis the benchmark underpaid, then go look at the seam. An evaluation you never evaluate is just a vibe at scale. Instrument the grader, not just the model.
