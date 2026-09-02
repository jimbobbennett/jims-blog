---
author: "Jim Bennett"
date: 2026-09-02
publishDate: 2026-09-02
description: "Boris Cherny says to delete your CLAUDE.md, skills, and hooks every six months. That's good advice for one kind of skill and dangerous for another. Here's how to tell them apart, and why the skills that encode your pipeline are software worth keeping."
draft: false
slug: "skills-are-pipelines"
title: "Skills are pipelines"
tags: ["ai", "agents", "skills", "claude-code", "claude"]
featured_image: cover.png
image: /blogs/skills-are-pipelines/cover.png
---

[Boris Cherny](https://www.linkedin.com/in/bcherny/), who created Claude Code and runs it at Anthropic, gave some advice recently that made a lot of people reach for the delete key. Talking at Y Combinator about what changed with the newer models, he said this:

> "For people who aren't building agentic products but are using Claude Code, every 6 months, delete your CLAUDE.md file, delete your skills, and delete your hooks. Then see what the model does. It might surprise you."

He backed it up with a number. For the latest models, Anthropic [deleted 80% of the system prompt](https://charliehills.substack.com/p/delete-your-claudemd), and the model got better. His reasoning is sound: a lot of what you write into a system prompt is a patch for something an older model got wrong. When the model improves, the patch turns into noise. It contradicts newer instructions, it eats tokens every session, and it sits in the middle of a long file where the model half-reads it.

I agree with some of this. I just think the "delete your skills" part, taken on its own, is dangerous advice. Not because auditing is wrong, but because it treats every skill as the same kind of thing. It isn't. There are two kinds, and the advice only applies to one of them.

## Two kinds of skills

Before you decide what to delete, you have to sort your skills into two piles.

The first pile is **tool skills**. These teach the agent how to drive something that already has public documentation: a command-line tool, a login flow, an API, a product's docs. You wrote the skill because the model didn't know the tool well enough, or kept getting the flags wrong.

The second pile is **pipeline skills**. These encode how *you* work. A multi-stage process that pulls data from somewhere, transforms it, and produces a report. A writing style that a reviewer has to sign off on. A sequence of steps that has to run in a specific order because you learned the hard way what happens when it doesn't.

![Tool skills, safe to prune, next to pipeline skills, kept and maintained like code](/blogs/skills-are-pipelines/two-piles.png)

Cherny's advice is a good fit for the first pile. It's a terrible fit for the second. So let's take them one at a time.

## Why tool skills are safe to delete

A tool skill is a bet that the model doesn't know something. That bet has an expiry date.

Say you wrote a skill six months ago that explains how to use a CLI, because the model kept guessing at the wrong subcommands. Since then the model has been retrained, and the tool's documentation was almost certainly in the training data. There's a decent chance the model now knows the tool cold, and your skill is just repeating what it already knows. Worse, if the tool changed and your skill didn't, you're now feeding it stale instructions it will trust over its own knowledge.

So yes, delete it and see what happens. This is exactly the case Cherny is describing, and he's right.

One caveat, though. Models lag behind products. The model's knowledge is frozen at its training cutoff, but the tool you're documenting shipped three new features last month. If your skill is the only thing telling the agent about those features, deleting it makes the agent dumber, not smarter. So don't just delete, instead delete, then retest against the thing you actually need the tool to do. If the model handles it without the skill, the skill was noise. If it fumbles the new stuff, bring the skill back and trim it to just the parts the model is missing.

That's the audit Charlie Hills actually did in the post that popularised this whole "delete your CLAUDE.md" idea. It's worth reading, because the headline sounds like a call to burn everything down, and the post is the opposite. He went through 195 skills and found he used 65. He had 21 hooks across three layers. He cut and rewrote a chunk of his config. And then he ended with this:

> "I'm not deleting mine. I'm maintaining it."

![Charlie Hills with Boris Cherny at Y Combinator](/blogs/skills-are-pipelines/hills-cherny-yc.jpeg)
*Charlie Hills with Boris Cherny at Y Combinator. Photo from [Hills' post](https://charliehills.substack.com/p/delete-your-claudemd).*

That's the right instinct. Audit hard, delete the dead weight, keep what earns its place.

## Why pipeline skills are not

Now the second pile, and this is where "delete and see what happens" falls apart.

A pipeline skill doesn't teach the model something it could have learned from public docs. It teaches the model something only you know. There is no training run that will give the model back your specific process, because your process was never on the public internet to begin with.

Let me give you a real one. On my team we have a skill called "time to wow." It measures how quickly a new user gets from signing up to hitting a defined success moment, the point where the product has actually done something useful for them. Sounds simple. It is not.

The skill encodes a pipeline. It runs a freshness check first and refuses to report if the data is stale. It merges two separate activation signals rather than trusting either one alone, because each has a blind spot the other covers. It uses a median calculated over a 24-hour window instead of a straight average, because a straight average gets wrecked by the long tail of users who sign up and come back three weeks later. Each of those decisions is a step in an ordered process, and each one is there for a reason.

![The time-to-wow pipeline: freshness check, merge two signals, windowed median, report, with the August stall it guards against](/blogs/skills-are-pipelines/time-to-wow-pipeline.png)

And here's the part a fresh model could never reconstruct. Back in August, one of our data syncs quietly stalled. The number we divide by stayed current, but the number on top froze several days earlier. Nothing errored. No alert fired. The activation rate just read 7.4% when the real number was somewhere between 12 and 22%, and it looked completely plausible. We only caught it because the number felt wrong. The fix, merging the two signals and adding an alarm for exactly that stall pattern, is now baked into the skill so it can never fool anyone again.

If I delete that skill and see what the model does, the model does not know about the sync that stalls. It does not know the median has to be windowed. It writes me a confident, clean, wrong report. The skill is not a patch for a dumb model. It's institutional memory written down as software. Retraining the model doesn't bring it back, because it was never the model's to know.

The same goes for a writing style your editor has to approve, or any process where "correct" is defined by your rules and not by public convention. Deleting those to see what the model does isn't an experiment. It's just throwing away work.

## A skill is a pipeline that calls code

Once you see the second pile clearly, the whole way you think about skills changes.

I was talking about this on a panel recently with a couple of other folks, and Anthony Campolo put it better than I had managed to:

> "It's a natural language pipeline, isn't it? That's essentially all it is. It's a natural language pipeline that calls out to code-based components."

That's exactly it. When you build with skills, the harness is your agent framework and the skill is the prompt that drives it. The skill sets out the steps in plain language, and where a step needs real work done, it calls out to code. A natural-language pipeline that orchestrates code.

Which means the good pipeline skills are not throwaway prompts. They're software. And if they're software, you should build them the way you build software.

## So build them like code

We've spent 40 or 50 years working out how to keep code from rotting. Most of that applies here.

Don't repeat yourself. If three skills all explain the same setup step, pull it into one place they can share, so you fix it once instead of three times.

Don't cram everything into one file. A skill can be split across several. Load the instructions for instrumenting a Python app only when someone's working on Python, instead of shipping the Python, Go, and JavaScript instructions every single time. It keeps each run lean and keeps the model reading the part that actually matters.

And write evals. This is the piece that makes Cherny's audit safe instead of scary. If you have a test that checks a skill still produces the right output, you can delete the skill, run the eval, and see exactly what degraded. No degradation means the skill was noise, so leave it deleted. A failed eval tells you precisely what the model can't do on its own, so you know what to keep. The audit stops being a vibe check and becomes a measurement.

This is not hypothetical. I ran exactly this loop on a skill and [wrote up the numbers](https://arize.com/blog/quantifying-skill-changes-arize-ax/). I treated the skill as an agent, built a golden dataset, ran the changes in a sandbox so the agent couldn't cheat, and scored the traces before and after. Editing one skill moved trace correctness from 74% to 83% and cut token use by 9%. That is the difference between "I think this skill helps" and knowing by how much.

The engineers I respect most right now spend a serious chunk of their time building and maintaining skills. Not writing them once and forgetting them. Maintaining them, the way you maintain a codebase you depend on.

## Audit, don't amnesia

So here's where I land. Cherny is right that you should audit. Every six months, go through your setup, delete the dead weight, retest the tool skills, and see what the model can now do on its own. That's good hygiene and you should do it.

But "delete your skills and see what happens" is only safe for the skills the model could have learned somewhere else. For the skills that encode your pipeline or your voice, deletion isn't a test. It's amnesia. You're not finding out what the model knows. You're finding out what you forgot to write down anywhere else.

Sort your two piles. Prune the first one hard. Guard the second one like the code it is.
