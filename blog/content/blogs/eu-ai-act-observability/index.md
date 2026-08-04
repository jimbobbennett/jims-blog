---
author: "Jim Bennett"
date: 2026-08-04
publishDate: 2026-08-04
description: "The EU AI Act's record-keeping duties ask for exactly the kind of log an observability tool already produces. Instrumenting your app is the cheapest do-it-anyway first step toward compliance, as long as you remember a trace is a claim, not a certificate."
draft: true
slug: "eu-ai-act-observability"
title: "The EU AI Act wants a record. Your traces are already most of one."
tags: ["ai", "eu-ai-act", "observability", "compliance", "tracing", "openinference", "arize-ax"]
featured_image: cover.png
---

I read a piece by Angie Jones from the Agentic AI Foundation this week, [The EU AI Act and the new rules for building AI agents](https://aaif.io/blog/the-eu-ai-act-and-the-new-rules-for-building-ai-agents), and one line stuck: *"Autonomy does not move responsibility from the company to the agent."* Building an agent does not offload your obligations onto it. You still owe everything the company that shipped it owes. Her practical point is that agents make record-keeping hard, because *"the important event is often an action,"* so *"a useful record needs to show what the agent requested and what actually happened."*

Reading that, I had a mildly heretical thought for someone in this field: this regulation is asking me to build something I would build anyway.

I should say where I stand, because this is an opinion piece and you deserve to know the bias. I am pro-regulation, with a condition. Left alone, companies will take the cheap (or more likely profitable) shortcut, especially when the shortcut is invisible or nobody is checking. A rule that forces AI systems to be transparent about what they did, and to keep a record of it, is a rule I want. But regulation only earns its keep when compliance is cheap. A rule that costs a fortune to satisfy and produces nothing you would have wanted otherwise is just a tax on building things. The interesting question about the EU AI Act is which kind it is, and for one slice of it, the record-keeping slice, I think the answer is the good kind.

## Not every app is high-risk, and the clock has moved

The record-keeping duties I am talking about in this post apply to [high-risk AI systems](https://artificialintelligenceact.eu/article/6/), a specific category: systems that are a safety component of a regulated product, or that fall into one of the [Annex III](https://artificialintelligenceact.eu/annex/3/) use cases like employment, essential services, law enforcement, or biometrics. The Commission's own estimate is that this is a minority of AI applications. If you are building an internal summarizer that never sees a customer, it is probably not high-risk. If you are building the thing that screens job applicants, it probably is. Classify honestly before you do anything else.

The clock matters too, because it recently changed. The [Digital Omnibus on AI](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai) was published in the Official Journal on 24 July 2026 as Regulation (EU) 2026/1744, in force from 27 July 2026, and it [postponed the high-risk deadlines](https://www.gibsondunn.com/eu-ai-act-omnibus-agreement-postponed-high-risk-deadlines-and-other-key-changes/). The Annex III use-case rules now apply from 2 December 2027, and the Annex I product-embedded rules from 2 August 2028. So the logging duties are not enforceable today, but are coming soon. December next year may not sound soon to a fast moving startup, but for larger, slower enterprises this is something that needs to be scoped and planned for now so that it is ready before the deadline hits.

Other prohibitions have applied since February 2025. The general-purpose AI documentation and evaluation duties have applied since August 2025, and the [Article 50](https://artificialintelligenceact.eu/article/50/) transparency duties, telling a person they are talking to an AI and marking synthetic content, came into general application in August 2026. The runway is for the high-risk logging rules specifically, and a runway is not a reason to defer. It is the cheapest possible window to design logging in as a normal part of the system instead of a panicked retrofit the week before an audit.

## What the Act actually asks for

Here is the part that reads, to an engineer or PM, like a feature request.

[Article 12](https://artificialintelligenceact.eu/article/12/) says high-risk systems *"shall technically allow for the automatic recording of events (logs) over the lifetime of the system,"* and it ties that to *"traceability,"* recording the events relevant to spotting risks, enabling post-market monitoring, and watching how the system operates. [Article 19](https://artificialintelligenceact.eu/article/19/) sets a hard floor on how long you keep them: the logs *"shall be kept for a period appropriate to the intended purpose... of at least six months,"* a duty on providers, with a parallel six-month duty on deployers in Article 26 for logs under their control. [Article 13](https://artificialintelligenceact.eu/article/13/) then asks you to document the mechanism, to describe *"the mechanisms included within the high-risk AI system that allows deployers to properly collect, store and interpret the logs in accordance with Article 12."*

Read those together and the shape is: record what happened automatically, keep it for at least six months, and be able to explain how the record works. That is an observability requirement written in legal prose.

One thing the Act asks for that a log does not satisfy: Article 50 transparency. Marking content as AI-generated and telling a user they are talking to a machine is a product decision, not a logging one. It is easy to bundle it in because it sits under the same "transparency" heading, so keep it separate in your head. A trace cannot be the disclosure, but observability still helps you keep it honest. You can run an eval over your responses to confirm they actually carry the required AI disclosure, and when a chatbot hands a conversation to a human, that handoff is itself a moment to tell the user they are now talking to a person, not the AI.

## A trace is most of that record

If you have instrumented an LLM app, you already produce most of what Article 12 is describing.

The mechanism is a trace: a tree of spans, where each [span](https://opentelemetry.io/docs/concepts/signals/traces/) is one step of work with a name, a start and end time, and a bag of attributes. One run of your agent becomes one tree. [OpenInference](https://github.com/Arize-ai/openinference/blob/main/spec/semantic_conventions.md), an open standard built on OpenTelemetry, gives that tree an AI-specific shape: span kinds like LLM, TOOL, RETRIEVER, and AGENT, each tagged with the model name, token counts, and, when you opt in, the actual prompts, completions, and tool results.

That lines up almost exactly with what the Act wants recorded. What the system was asked to do, what it invoked, what came back, which model version served it, and when, is precisely what a span tree already holds. Not the model's private reasoning, and not a legal "decision," but the observable facts of the run, which is what Article 12 is after.

![A span tree on the left, with model call, prompts, tool calls and arguments, retrieval, timestamps and errors, mapped by lines to what the Act asks for on the right: traceability, automatic logging, and six-month retention.](/blogs/eu-ai-act-observability/diagram-1-article12-mapping.png)

Laurie Voss, writing about the same overlap in [The EU Just Wrote an Observability Spec into AI Regulation](https://www.linkedin.com/pulse/eu-just-wrote-observability-spec-ai-regulation-laurie-voss-civpc/), puts the practical version of this as a discipline: *"Keep sample trajectories per evaluation run, deliberately. Not aggregate scores."* The record that earns its keep is the run itself, the actual sequence of prompts, calls, and returns, not a dashboard number that averages the trajectory away. If you only keep the score, you have kept the grade and thrown away the exam.

The Act does not mandate OpenInference, or a prompt-capture schema, or any observability platform. It asks for automatic logging of risk-relevant events, and it is your job to make sure the events you capture are the ones that matter for your system's risks. Prompts and completions are captured only when you opt in. A default trace can be both too thin, missing an event the regulator cares about, and too broad, capturing personal data you now have to protect. A trace gives you the substrate. Designing it to be the right record is still work, and it is work that is far easier to do at the start than to bolt on later. The best time to instrument an app is when you write the first line of code, and the second best time is now.

## What turns a trace into an audit trail

A trace gives you the raw material for an audit trail. Turning it into one is a design job, and it is worth being clear-eyed about that job before anyone treats a pile of spans as proof.

The sharpest version of the point comes from Jaroslaw Wasowski, who writes about LLM audit trails and the EU AI Act, in [Your logs are claims, not evidence](https://medium.com/@wasowski.jarek/your-logs-are-claims-not-evidence-llm-audit-trails-eu-ai-act-9e4dc6d55d46): *"Between observability ('I can see what happened') and auditability ('I can prove to a skeptic that it happened') lie ninety percent of current LLM observability deployments."* A log produced by the party being audited is, without more, a claim. His line for what "more" looks like: *"without independent verification, a record stops being evidence and becomes a hypothesis from an interested party."* Igor Ganapolsky, who writes on AI agents and compliance, makes the adjacent point that teams often [log the wrong layer](https://dev.to/igorganapolsky/your-compliance-team-will-ask-for-an-ai-agent-audit-trail-before-august-2-heres-the-part-most-h2n): prompt and completion logs are *"a record of intent and response, but it is not a record of governance."*

![Two columns. On the left, what a trace gives you by default: visibility into what happened. On the right, the four things you design in to make it hold up: integrity and tamper-evidence, completeness, the six-month retention floor, and privacy.](/blogs/eu-ai-act-observability/diagram-2-trace-vs-audit-trail.png)

So there are four things you design in to close the gap, and a skeptical reviewer will push on each.

- **Integrity:** decide who can alter or delete a span after the fact, and make the record tamper-evident. [ISMS.online](https://www.isms.online/iso-42001/eu-ai-act/article-12/) suggests *"cryptographic hashes, append-only write-once media, or blockchain to make logs unalterable,"* and warns that *"retroactive bulk logging or stitching after the fact is explicitly insufficient,"* so the record has to accrue as the system runs.
- **Completeness:** prompts and tool results are recorded only when you turn them on, so decide up front which events matter and capture those.
- **Retention:** point the record at storage that meets the six-month floor, rather than the shorter windows debugging tends to default to.
- **Privacy:** capturing full prompts and completions can mean storing personal data, so be deliberate about what you keep, because the fix for one obligation can create another under GDPR.

And beyond the record-keeping duties, there is a whole set of things a trace does nothing for. Risk management, data governance and training-data quality, human-oversight design, conformity assessment and the technical documentation a general-purpose model provider owes: none of those live at runtime, so none of them show up in a span. Observability is a down payment on the logging duties. It is not a payment on the rest of the Act.

## You would build it anyway, so build it well

Here is the part that makes me pro-regulation on this specific rule: instrumentation is not a cost you take on for the regulator. It is a cost you take on for yourself, and the compliance value is a byproduct.

In my experience you instrument an agent because you cannot debug what you cannot see, because your evals need real traces to score, and because you want to know which tool call is burning your token budget. The record that Article 12 asks for falls out of the work you would do to ship a system you can actually operate. That is what a good regulation looks like from an engineer's chair. It rewards the thing you should have been doing and asks for very little on top.

There is also a commercial pull, separate from the legal one, and it is the reason the runway is shorter than the deadlines suggest. The direct burden of the Act falls on a fairly small set of large providers today, but the requirements do not stay there. As Laurie Voss points out, they travel downhill through the supply chain and arrive as security questionnaires and procurement templates from your enterprise customers, who need their own vendors to produce this kind of record before they will sign. The practical effect is that you are likely to be asked to show an operational trail long before any regulator asks for one, and by whoever is trying to buy your software. Instrumenting now answers that question before it is put to you.

The little on top is vendor-neutral and worth doing in this order. Instrument with OpenTelemetry and OpenInference so you are writing to an open standard and not painting yourself into one backend. Send the spans to a tracing backend that will hold them; [Arize AX](https://arize.com/docs/ax/instrument/what-are-traces) is the one I reach for, and because it is built on OpenInference nothing above is proprietary. Then close the gaps from the last section: make retention meet the six-month floor, lock down who can edit records, and be deliberate about what personal data you capture. On retention specifically, I would not lean on any vendor's default window to satisfy Article 19. The durable move is to keep a copy of the record in storage you own, for example an open [Iceberg export into your own warehouse](https://arize.com/docs/ax/security-and-settings/data-fabric), so you retain it on your own terms.

## The record does not exist until the system runs

Instrumenting now does not mean the Article 12 record already exists. It means the logging is designed, deployed, and tested, so the record accumulates as the system operates instead of being conjured the week before the audit, which the regulators are inclined to treat as no record at all.

That is the whole case for using the runway. The high-risk deadlines are December 2027 and August 2028, and the cheapest move available is to make logging a normal, tested part of the system between now and then. You get a system you can debug and evaluate today, and a compliance head start you barely had to pay for.

Good regulation should reward good engineering rather than punish it. On the record-keeping slice of the EU AI Act, it does. Instrument your app because it makes the app better, keep the record complete, durable, and hard to tamper with, and you will find you walked most of the way to compliance while you were just trying to build something you could see.
