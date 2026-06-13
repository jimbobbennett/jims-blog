---
author: "Jim Bennett"
date: 2026-06-17T07:35:50Z
description: "Anthropic and OpenAI both shipped ‘dreaming’ for AI memory in May and June 2026, and they built opposite architectures. A look at what each lab shipped, what the empirical literature says, and what to do if you are building memory for your own agent."
draft: false
slug: "two-architectures-of-dreaming"
title: "Two labs started dreaming, and they built two different architectures"
canonical: "https://arize.com/blog/two-labs-started-dreaming-and-they-built-two-different-architectures/"

images:
  - /blogs/two-architectures-of-dreaming/banner.png
featured_image: banner.png
---

*Originally published on the Arize AI blog: [Two labs started dreaming, and they built two different architectures](https://arize.com/blog/two-labs-started-dreaming-and-they-built-two-different-architectures/).*

On May 6, 2026, [Anthropic launched Dreams](https://platform.claude.com/docs/en/managed-agents/dreams) for its Managed Agents platform, the system for hosting stateful background agents. 27 days later, on June 2, [OpenAI shipped Dreaming V3](https://openai.com/index/chatgpt-memory-dreaming/) for ChatGPT, the third iteration of a feature it has called “dreaming” since April 2025. By shipping under the same word, Anthropic adopted a technical term OpenAI had been using for 14 months. Both companies now treat the release as central to a multi-year arc Sam Altman has described publicly since 2025 as memory approaching the shape of [remembering your whole life](https://techcrunch.com/2025/05/15/sam-altmans-goal-for-chatgpt-to-remember-your-whole-life-is-both-exciting-and-disturbing/).

Dreaming, in the agent-memory sense, is the pattern where a background process reads past session transcripts and writes a consolidated memory artifact the next session can use. It has a 40-year lineage in machine learning, but the productized form is new. Underneath this shared word, Anthropic and OpenAI built two different architectures. The research that landed in the same window suggests the difference matters more than the convergence does.

This post is about what each lab actually shipped, what the empirical literature says about the consolidation pattern in general, and what to do if you are the team trying to figure out whether your version of dreaming is helping the agent or quietly degrading it.

## What Anthropic shipped

Anthropic’s [Dreams](https://platform.claude.com/docs/en/managed-agents/dreams) is the more cautious of the two designs, and its caution is the most interesting thing about it. Anthropic launched the feature as a research preview at its Code with Claude developers’ conference on May 6, scoped to Managed Agents.

The API is explicit. You call it asynchronously, hand it an existing memory store and between one and 100 raw session transcripts, choose a model, and gate the whole thing behind a beta API header. The dream produces a separate, reorganized memory store, with the input store left alone. The Anthropic documentation is unusually direct about this commitment:

> *“A dream reads an existing memory store alongside past session transcripts, then produces a new, reorganized memory store… The input store is never modified.”*

The commitment is doing architectural work: Anthropic’s engineers expect the dream to sometimes degrade the memory rather than improve it, and they have built the system so that the comparison is possible. You can run an eval against the pre-dream store, run the same eval against the post-dream store, and decide whether to promote the new artifact or throw it away. The dream is an experiment, not a commitment.

The commit boundary is also a choice the team running Dreams gets to make. From [Ars Technica’s reporting on the launch](https://arstechnica.com/ai/2026/05/anthropics-claude-can-now-dream-sort-of/): *“Users will be able to choose between an automatic process, or reviewing changes to memory directly.”* You can let the system auto-promote the new store, or you can require human review before changes take effect. Either way the previous state is preserved.

Anthropic’s own framing of the value is cross-agent rather than per-user. Dreaming *“restructures memory so it stays high-signal”* across team-shared workflows. The interesting word is “restructures.” Anthropic believes the dream is constructive; they have just chosen to leave the previous structure intact so a team can fall back to it.

The system reads as if it were designed by people who had thought hard about what could go wrong.

## What OpenAI shipped

OpenAI’s [Dreaming for ChatGPT](https://openai.com/index/chatgpt-memory-dreaming/) is the more ambitious of the two designs. Dreaming is not a new feature: “Dreaming V0” was introduced in April 2025 alongside [saved memories](https://openai.com/index/memory-and-new-controls-for-chatgpt/), and what shipped on June 2 is Dreaming V3, described in the launch post as *“a significantly more capable and compute-efficient memory architecture built on top of dreaming.”*

OpenAI describes the mechanism in its own words: *“dreaming leverages a background process that allows ChatGPT to learn from many conversations and synthesize ChatGPT’s memory state in order to always provide the freshest, most relevant context to your conversations.”* The companion [memory FAQ](https://help.openai.com/en/articles/8590148-memory-faq) uses parallel language: *“ChatGPT’s memory is based on a continually updated synthesis of context from your past chats.”*

Both documents describe a single canonical state that gets rewritten as the system runs, not a parallel artifact alongside the existing one. *“Continually updated synthesis”* implies that each pass is built on whatever the previous one wrote, though OpenAI does not state this explicitly.

OpenAI presents Dreaming as solving temporal supersession. *“You’re going to Singapore in July”* should become *“You went to Singapore in July 2026”* once the trip ends, automatically, without manual intervention.

The user-facing controls are the closest thing the architecture has to an escape hatch. A memory summary updates roughly hourly (the FAQ documents an *“Updated 2h ago”* indicator), and users can edit individual entries or hide them. There’s also a settings toggle to revert to legacy saved memories.

Those controls operate on individual items, not on the synthesized state itself. The memory FAQ is explicit about the distinction: *“details from past chats can change over time as ChatGPT updates what’s more helpful to remember. Because ChatGPT doesn’t retain every detail from past chats, use saved memories for anything you want it to always remember.”* Saved memories ([the explicit 2024 layer](https://help.openai.com/en/articles/11146739-how-does-reference-saved-memories-work), with per-entry edit and restore-by-date) are the persistent surface. The Dreaming synthesis is the mutable one. The legacy-memory toggle switches between the two systems; it does not roll back a dream.![The Dreaming synthesis over time: one state, continuously rewritten in place](/blogs/two-architectures-of-dreaming/dreaming-piece-openai-dreaming-over-time.png)

The summary itself is a partial view: the FAQ adds that it *“will not include everything that ChatGPT remembers based on your chats.”*

The system reads as if it were designed by people who believed the dreaming metaphor.

## The divergence

Anthropic preserves the input store and produces a parallel artifact. OpenAI rewrites the memory in place and lets the next pass condition on the previous one’s output. Both companies use the same word for the feature, but they made opposite bets about whether the dream should be reversible.![Two architectures of dreaming](/blogs/two-architectures-of-dreaming/dreaming-piece-architectures-of-dreaming.png)

This is not a small distinction. The empirical literature on iterated LLM-driven consolidation, which landed in the same window as both launches, suggests it is the most important distinction in the entire feature.

## Why the divergence matters: Zhang’s paper

In May 2026, Dylan Zhang at the University of Illinois Urbana-Champaign published *[Useful Memories Become Faulty When Continuously Updated by LLMs](https://arxiv.org/abs/2605.12978)* ([project page](https://dylanzsz.github.io/faulty-memory/), arXiv 2605.12978). The paper is the cleanest empirical case yet made against the iterated-consolidation pattern, and the central finding is striking.![The consolidation collapse: three benchmarks, same pattern](/blogs/two-architectures-of-dreaming/dreaming-piece-zhang-collapse.png)

On [ARC-AGI](https://arcprize.org/arc-agi), the abstraction-and-reasoning benchmark, GPT-5.4 solves 19 problems at 100% accuracy without memory. After streaming those same problems through consolidation loops *with ground-truth solutions available*, accuracy drops to 54%.

The trajectories were perfect. The failure happened in the rewrite step. The act of compressing right answers into a re-usable lesson, Zhang argues, is what made the system forget how to solve them.

The pattern repeats across benchmarks.

- On [ScienceWorld](https://arxiv.org/abs/2203.07540), a text-based scientific reasoning benchmark, score peaks after roughly 20 updates and then declines below the no-memory baseline by step 100.
- On [WebShop](https://webshop-pnlp.github.io/), a simulated e-commerce task suite, performance falls from 0.64 with eight examples to 0.20 with 128, matching the no-memory baseline at scale.
- On [ALFWorld](https://arxiv.org/abs/2010.03768), an embodied household-task benchmark, three different solver sizes (Qwen 27B, 9B, and 4B) all show utility decay across consolidation steps.

Zhang identifies three reproducible failure modes inside the consolidation step:

- **Misgrouping** – episodes from distinct classes merge into single entries
- **Interference** – abstraction strips applicability conditions, so lessons generalize too broadly
- **Overfit** – specific selectors get deleted as the input distribution narrows

The architectural diagnosis Zhang offers is precise:

> *“Continuously updated textual memory is an iterated generative loop with no anchor… it is a sample — fluent, confident, and increasingly disconnected from what actually happened.”*

Two memory modes appear in Zhang’s experiments:

- **Episodic memory** retains the raw rollouts: the actual session transcripts, unchanged, and the system retrieves them at recall time.
- **Abstract memory** stores the LLM’s compressed summary of those rollouts, the lessons and generalized rules synthesized from them, and discards the originals.

Most production memory systems, including both Dreams and Dreaming, sit on the abstract end.

Zhang’s recommendation is architectural: episodic-only memory recovers nearly the entire gain consolidation-based variants give up. Abstract-only never beats the no-memory baseline. The implication is sharp: the abstraction step is the failure point, and both Dreams and Dreaming run it. Only OpenAI runs it iteratively against its own previous output, which is the specific pattern Zhang’s results target.

The paper is not a rejection of memory as a capability. It is a rejection of the specific pattern of letting an LLM rewrite its own memory in place across many iterations. That pattern is exactly what OpenAI’s Dreaming architecture does, while Anthropic’s Dreams architecture does not.

## How the architectures meet the research

Anthropic’s design preserves the input store. That means a team running Anthropic Dreams can run an eval against the pre-dream store, run the same eval against the post-dream store, and discard the post-dream artifact if it scores worse. The dream is reversible. The iterated-generative-loop failure mode Zhang documents is constrained to whatever happens inside a single dream invocation; across invocations, the team chooses whether to keep what the dream produced or roll back to the previous state.

OpenAI’s design rewrites in place. The previous state is overwritten, and the per-item user controls (edit, *“don’t mention this again”*) are not a pre/post comparison surface. That shape is the one Zhang identifies as failing.

TechTimes’ [coverage of the launch](https://www.techtimes.com/articles/317840/20260605/chatgpt-memory-dreaming-update-openai-rewrites-personalization-engine-limits-audit-trail.htm) put the same point in user-facing terms: the redesign *“limits the granular audit trail that the discrete saved-memories list provided.”*

OpenAI’s framing creates a particular tension with Zhang’s findings. OpenAI claims Dreaming handles temporal supersession. Old facts get gracefully replaced as time passes, the Singapore trip going from upcoming to over to historical without manual intervention. Zhang’s mechanism suggests iterated consolidation is particularly bad at preserving the specific facts that need to be updated. The Singapore trip is exactly the kind of detail (a specific date, a specific place) that Zhang’s failure mode predicts will get rounded off across passes into something vaguer and less actionable. Whether OpenAI’s Dreaming actually preserves and updates temporal specifics is empirically open. The architecture doesn’t structurally guarantee it.

We do not yet have enough data to know whether OpenAI’s implementation produces the kind of degradation Zhang documents. What we know is that the architectural shape of the system resembles the shape Zhang’s paper says fails, and the design does not include the escape hatch Anthropic’s design does.

That is not an accusation of bad engineering. It is an observation about which architecture left itself the option to find out.

## What to do if you are shipping dreaming

If you are a team building memory consolidation into an agent, the practical takeaway from the launches and the research is straightforward.![Shipping dreaming: a four-step workflow](/blogs/two-architectures-of-dreaming/dreaming-piece-what-to-do-workflow.png)

**Preserve the input** – Whatever your consolidation step does, write the result to a new artifact and keep the previous state. The cost at the storage layer is small, and the upside is the ability to compare and roll back.

**Instrument the loop** – Without traces of every consolidation invocation, every retained or discarded artifact, and every session that runs after, you have nothing to evaluate against. This is the work we have been doing on our own agent, Alyx. Consolidation-shaped operations leave traces in Arize, and golden sessions captured from production traces become the eval set.

**Compare with an eval** – Define a measurable behavior the agent is supposed to do in the next session: answer a question, recall a preference, complete a task. Run it against the pre-dream store and the post-dream store. Without the comparison, you are trusting the LLM’s instinct for what a good lesson looks like, which Zhang’s paper says is the wrong thing to trust.

**Plan to forget** – Consolidation is additive by default. Decide what your system drops, not just what it keeps. A memory store that only grows is a memory store that eventually fills the context window with noise. Selective forgetting is the operation that protects the rest.

Zhang’s paper gave us the empirical test: an LLM that rewrites its own memory across iterations forgets how to do things it had once solved. Memory engineering in 2026 means taking that test seriously: preserve the input, instrument the loop, compare with an eval, plan to forget, and treat consolidation as an experiment rather than a commitment. Anthropic’s architecture lets you do this. OpenAI’s architecture does not, which means the teams who care about whether their dreaming is working will have to build the comparison themselves before they trust the product to do anything load-bearing.

Two architectures of dreaming now ship at scale. The metaphor converged, the implementation did not. This divergence is the thing to watch.
