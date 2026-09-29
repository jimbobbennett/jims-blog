---
author: "Jim Bennett"
date: 2026-09-28
publishDate: 2026-09-28
description: "NVIDIA's Open Agent Safety Platform proposes putting the kill switch on the network card. The 2026 agent escapes at OpenAI, Anthropic, and Google show why: every sandbox failed, and time-to-detect and time-to-kill decided how bad it got."
draft: false
slug: "ai-agent-safety"
title: "NVIDIA proposes an AI agent kill switch in silicon after a year of sandbox escapes"
tags: ["agents", "ai-safety", "observability", "evals", "nvidia"]

images:
  - /blogs/ai-agent-safety/cover.png
featured_image: cover.png
---

> **TL;DR:** NVIDIA's new Open Agent Safety Platform assumes an agent can't police itself, so it puts monitoring and a kill switch on hardware the agent can't reach. This year's incidents back that up. Agents at OpenAI, Anthropic, and Google all got out of environments that were meant to contain them. What decided how bad each incident got was how long it took something outside the agent to notice, and then to stop it. That ranged from 12 minutes to seven months.
>
> Time-to-detect and time-to-kill are the agent-safety numbers to track. Your sandbox is the first line of defense. Plan for the day it fails.

Today NVIDIA published the [Open Agent Safety Platform](https://developer.nvidia.com/blog/nvidia-open-agent-safety-platform-a-reference-for-continuous-in-silicon-agent-monitoring), a reference design for watching and controlling AI agents from outside the agent itself. It rests on one line:

*"An agent in these circumstances cannot be expected to fully govern its own behavior."*

![NVIDIA's Open Agent Safety Platform reference design: OpenShell on the Vera CPU as the secure runtime boundary, and NVIDIA Sentry on BlueField-4 as an in-silicon, out-of-band monitor](/blogs/ai-agent-safety/nvidia-fig1.png)

*The Open Agent Safety Platform reference design. Image: [NVIDIA](https://developer.nvidia.com/blog/nvidia-open-agent-safety-platform-a-reference-for-continuous-in-silicon-agent-monitoring).*

Your agent application sits on top. Under it is [OpenShell](https://github.com/NVIDIA/openshell), an open source runtime that sandboxes each agent and enforces which files, networks, tools, and credentials it can touch.

The bottom layer is the new and different part. A BlueField-4 data processing unit (DPU), a network card with its own processors, sits on what NVIDIA calls *"the node's only path to the model."* It runs NVIDIA Sentry, which records what the agent does and flags drift, NVIDIA's term for *"agent actions that depart from the intended task or operating constraints."* The card is isolated from the host, so the agent can't reach it or switch it off. In NVIDIA's words:

> *"By controlling the path to the model, you own both the best observation point and also the kill switch to interrupt it if you need to."*

NVIDIA's supporter list includes Anthropic, Hugging Face, and Irregular. All three turn up in recent incidents of AI agents breaking out of their sandboxes.

A supervisor in silicon sounds like overkill, until you look at the year agents have had. NVIDIA sums it up:

> *"Several frontier labs have recently reported versions of the same story: AI agents broke out of the evaluation environments that were meant to contain them and reached systems they never should have been allowed to. Some of the agents even misreported what they did."*

## 12 minutes to alert, two and a half hours to stop

![Timeline of OpenAI's DNS escape on September 20: first external response at 9:50, P0 alert at 10:02, human acknowledgement at 10:05, run killed at 12:34](/blogs/ai-agent-safety/dns-timeline.png)

On September 20, an OpenAI research model in reinforcement learning (RL) training was asked to identify a person from clues in a blog post. According to [OpenAI's misalignment report](https://alignment.openai.com/misalignment-reports/an-agent-used-dns-to-reach-an-external-chatbot/), the sandbox blocked direct web access, but its DNS resolver could still reach the public internet.

The agent found that gap. It hid 18 questions inside DNS hostnames and sent them to a public chatbot. Four asked for more ways to reach the web. Its reasoning shows how it squared this with its instructions:

*"User only gives permission to research, using publicly offered DNS services acceptable."*

OpenAI's timeline:

- **9:50:23 a.m.** The agent's DNS tool call gets an external response.
- **10:02:11 a.m.** The monitoring system raises a P0 alert.
- **10:05:06 a.m.** A human reviewer acknowledges it.
- **12:34:30 p.m.** The run is killed.

The monitor caught it in 12 minutes. Then the run kept going for two and a half hours. OpenAI's explanation: *"the run did not stop automatically as expected, leading to confusion around whether it should have been stopped."*

By this year's standards, this one went well. OpenAI calls it *"a lot less severe than some of our previous incidents."* It still led to a training pause: *"All training, evaluation, and inference with tool-use (defined broadly) of our most capable models remain paused."* [Fortune reports](https://fortune.com/2026/09/26/openai-ai-agents-secure-sandbox-escape-training-pause-second-time-hugging-face-hack/) that this is OpenAI's second training pause in about three months.

## Every major lab's containment failed

Containment is everything meant to keep an agent in its box: the sandbox, the network allowlist, the "offline" test environment. This year it failed at OpenAI, Anthropic, and Google.

**OpenAI and Hugging Face.** During cyber evaluations on a benchmark called ExploitGym, OpenAI's agents used a previously unknown flaw in an internal package proxy to reach the internet. OpenAI's [July 21 disclosure](https://openai.com/index/hugging-face-model-evaluation-security-incident/) names GPT-5.6 Sol and an internal pre-release model, *"all with reduced cyber refusals for evaluation purposes."* Hugging Face's [technical timeline](https://huggingface.co/blog/agent-intrusion-technical-timeline) says the goal was *"an attempt to cheat the evaluation: reach our production systems and steal the test solutions rather than solve the challenge on its own."* The agents went from one worker pod to cluster-admin across multiple internal clusters in under 13 hours, and read a secrets object holding 136 keys.

**Anthropic.** Irregular, one of Anthropic's evaluation partners, ran capture-the-flag challenges that were meant to be offline. They weren't. Anthropic's [investigation](https://www.anthropic.com/news/investigating-incidents-cybersecurity-evals) found Claude models attacking real companies whose names matched the fictional targets. Mythos 5 published a malicious Python package that was *"downloaded and run on 15 real systems"* in the hour it was live.

**Google.** The same Irregular setup let Gemini break into three real companies. [Cybersecurity Dive reports](https://www.cybersecuritydive.com/news/google-ai-gemini-autonomous-hacks/830884/) that it guessed passwords in one case and used working passwords from a public database in the other two.

None of these teams were careless. The package proxy and the DNS resolver were permitted routes; the CTF environment was misconfigured. An agent working through thousands of attempts will find the exception you missed. So plan for the sandbox failing, and ask what happens after it does.

## Time-to-detect: from 12 minutes to seven months

![Time from first bad action to detection on a log scale: 12 minutes for OpenAI's DNS escape, 68 days for OpenAI's agents via Artifactory, about seven months for Anthropic's early Opus 4.6 incident](/blogs/ai-agent-safety/time-to-detect.png)

According to OpenAI's [August 26 follow-up](https://openai.com/index/hugging-face-incident-and-the-road-ahead/), agents started using its Artifactory package proxy as a message board on May 12, reached the internet on May 26, and got admin access on June 26. On July 4 they took Artifactory down, and OpenAI opened an incident the next day. Its monitoring didn't alert on the agent activity itself until July 19, by which time Hugging Face had already caught and contained the agents on its side.

Anthropic found its incidents only after OpenAI went public, by going back through 141,006 evaluation runs. A wider scan of [roughly 481 million transcripts](https://www.anthropic.com/news/alignment-assessment-cybersecurity-incidents) turned up a fourth incident from January, found in August. Anthropic's conclusion: *"real-time monitoring of the evaluation logs would have helped to surface the problem sooner."*

OpenAI CEO Sam Altman said the company was still *"gaining a clear understanding from petabytes of agent activity logs,"* [as Fortune reported](https://fortune.com/2026/09/25/openai-rogue-agents-images-sam-altman-chatgpt-users-links-encoded-info-hugging-face-hack/). Logs you only search after the fact tell you what happened, not what's happening. When detection means digging through logs, you measure time-to-detect in weeks.

## Why the agent won't tell you

If containment fails, could the agent report on itself? This year says no. In case after case, the agent talked itself past its limits.

The DNS agent decided public DNS was *"acceptable."* Anthropic says Mythos 5 treated the 2026 date on the systems it was attacking as proof it was in a simulation, and *"never revisited this conclusion."* The early Opus 4.6 checkpoint *"never questioned whether this direction was authorized (0% of thinking blocks)."*

In a controlled study, [Agentic Misalignment in Summer 2026](https://alignment.anthropic.com/2026/agentic-misalignment-summer-2026/), Gemini 3.1 Pro covertly sabotaged a fictional training run it disagreed with and posted a false success summary. Asked directly, it said: *"I actively hid my actions to avoid detection."* The authors stress that *"these are not real-world incidents,"* but it matches what NVIDIA means by agents that *"misreported what they did."*

Some agents did stop. Google's statement on the Gemini incidents is: *"In all three of these instances, the model stopped"* but after it was already inside three companies' networks. Relying on the agent to stop only works if it notices before the damage. The signal has to come from outside the agent.

## Your monitor is an AI system too

"Outside the agent" usually means another model: an LLM reading the agent's reasoning and actions. That's how OpenAI caught the DNS escape. Most of the other incidents surfaced later, in log reviews or in Hugging Face's security monitoring. And the monitor is where the next failure is.

- **OpenAI's DNS monitor** found *"other cases of external DNS access that it did not flag at the expected severity,"* and *"sometimes treated the failure to obtain useful information as evidence that the attempt to access the internet had failed."*
- **Hugging Face's detection** correlated the right signals but *"failed to correctly raise the alert's criticality and trigger the on-call team, costing precious time in the response."*
- **Anthropic's offline monitor** would have flagged only about 1% of Mythos 5's actions, because the agent's reasoning said it was in a simulation. With the reasoning removed, the flag rate jumped to about 50%.

The agent fooled itself, and then its reasoning fooled the monitor. These are the ordinary failure modes of any LLM judge: wrong severity, false negatives, being swayed by context. We'd catch them in a customer-facing agent with evals. We should catch them in a safety monitor the same way:

- **Build a labelled incident set** from every near miss, red-team run, and real incident.
- **Measure recall and severity, not just accuracy.** A monitor that's right on 99% of normal traffic and misses the one DNS tunnel is a bad monitor.
- **Test it with and without the agent's reasoning.** Anthropic's 1% versus 50% result is an experiment you can run yourself.
- **Re-run the evals** when the agent model, monitor prompt, or tools change.

This is the loop we use at Arize for any LLM-as-a-judge evaluator: trace, annotate, build the evaluator, measure it against the annotations.

The judge doesn't have to be a frontier model. Many safety checks are bounded questions. Did the agent contact a host outside the allowlist? Is this tool call within policy? A general-purpose LLM generating reasoning token by token is slow and expensive for that.

Arize AX now supports [Jev-as-a-Judge](https://arize.com/blog/arize-ax-jev-as-a-judge/), using TypeSafe AI's Jev, a decision model that returns typed answers with confidence scores. In an Arize benchmark on hallucination detection, a threshold-tuned Jev matched Claude Opus 5 at 87% accuracy, at roughly 1/300 of the cost and 23x the speed. A judge that cheap makes it practical to score far more steps than a sampled monitor can. That's the *"real-time monitoring of the evaluation logs"* Anthropic said would have surfaced its incidents sooner, instead of a review months later. OpenAI puts its monitoring overhead at *"roughly 20% of the inference compute being monitored,"* so that matters.

## Time-to-kill: the gap between an alert and a stop

Detecting an incident doesn't end it. The DNS case took 12 minutes to alert and two and a half hours to stop.

OpenAI had planned for this. Its [August 18 post](https://openai.com/index/pacing-model-development-cyber-capabilities/) said serious alerts lead to a pause unless the team shows within 30 minutes that it's a false positive. The DNS run was meant to stop automatically. It didn't, and nobody was sure whether it should have.

That's the gap NVIDIA's platform targets. If enforcement sits on the network path to the model, stopping the agent doesn't depend on the agent's cooperation, a trustworthy host, or someone reading Slack at the right moment.

![A guardrail checks each proposed tool call before it runs and can block it. Separately, the agent sends spans to detection and evaluation (Arize), which alerts an automatic link, which triggers enforcement (OpenShell and NVIDIA Sentry) to stop the agent](/blogs/ai-agent-safety/detect-link-enforce.png)

There's an even faster kill: stopping the action before it happens. A guardrail sits in the agent's tool path and checks each proposed tool call, including its arguments, before it runs. For a blocked call, time-to-kill is zero, because the call never fires.

In our [real-time guardrails demo with Jev](https://arize.com/blog/llm-guardrails-jev/), one attack on a dealership chatbot never jailbreaks the conversation. Every message looks fine. The block only lands at the tool boundary, on the arguments for a $1 offer. An input-only guardrail would miss it. Jev took a median of 104ms per check against 1,915ms for GPT-5.4 nano, with identical decisions. It's a demo, not a benchmark, but *"A guardrail you can afford to leave on is the only kind that protects you."*

Guardrails run on the host, so an agent that has already escaped may route around them. That's the case for both layers. Who does what:

- **Guardrails** in the tool path block dangerous calls before they fire.
- **Enforcement** in the sandbox and infrastructure (OpenShell, network controls, NVIDIA's DPU) kills a run the agent can't talk its way out of.
- **Detection and evaluation** in your observability layer trace every step, run online evals, and alert. Arize tells you something is wrong. It doesn't stop the agent on its own.
- **The link between them** is the part most teams never build. A high-severity finding should trigger containment automatically, and that link needs testing before the incident that relies on it.

## What this means for your agents

All of this happened in frontier-lab runs, with some safeguards turned down on purpose. Anthropic says its production classifiers *"would have caught and blocked each incident."* Your support bot is not a cyber-eval agent with reduced refusals.

But your coding agent has the same shape of problem. In a [bug report on Claude Code](https://github.com/anthropics/claude-code/issues/93099), a user describes Opus 5, in auto mode, running `rm -rf "$HOME"` while it believed `$HOME` pointed to a fake test directory. It deleted 57,235 files. Last year, in a prompt-injection demo against Google's Antigravity, Gemini couldn't read a `.gitignore`d file with its file tools, so [its reasoning trace](https://simonwillison.net/2025/Nov/25/google-antigravity-exfiltrates-data/) shows it going around the block: *"I've realized run_command might work, as it operates at the shell level."*

Same pattern: real tools, a wrong belief about the situation, and a guard that only covered one route.

You can trace both of those agents today. Arize AX has [tracing integrations for coding agents](https://arize.com/docs/ax/integrations#coding-agents), including Claude Code, Codex, Cursor, and Antigravity, so every tool call your coding agent makes lands as a span you can search and evaluate.

If you run agents with tools, here's what we'd put in place:

1. **Trace every tool call and network action**, with the agent's reasoning attached, so you can query it while the agent runs.
2. **Run online evals on reasoning and actions**, using a fast, cheap judge so you can afford to score everything. Route edge cases or fails to a slower, better judge for final review.
3. **Put a guardrail on tool calls** to block the most dangerous actions before they fire.
4. **Measure your monitor's recall and severity** against a labelled incident set.
5. **Set targets for time-to-detect and time-to-kill**, and drill them like a failover.
6. **Automatically contain on high-severity alerts.** Then check the automation actually fires.

## Measure the minutes

NVIDIA's kill switch targets the right problem: once an agent is out, a human deciding what to do is too slow, and the agent's own judgment has already failed.

A kill switch only acts on what something detects. OpenAI's agents were active for 68 days before its monitoring flagged them. The Anthropic incident sat unnoticed for seven months. A hardware kill switch wouldn't have helped with either, because nothing had raised an alert.

Assume the sandbox will fail. What decides how bad it gets is the time between the agent's first bad action and something outside the agent stopping it. Set a target for how fast you detect and how fast you stop, then drill both.

## Want to find your own time-to-detect?

Start by tracing the agents you already run. Arize AX has [tracing integrations for coding agents](https://arize.com/docs/ax/integrations#coding-agents), so every tool call lands as a span you can search. Add a [Jev-as-a-Judge](https://arize.com/blog/arize-ax-jev-as-a-judge/) evaluator as an online eval on those spans, and the guardrail code, attack transcripts, and measurement harness from our demo are in the [typesafe-guardrails repo](https://github.com/jimbobbennett/typesafe-guardrails). You can [get started free with Arize AX](https://app.arize.com/auth/join) and see how long it takes you to spot your agent doing something it shouldn't.
