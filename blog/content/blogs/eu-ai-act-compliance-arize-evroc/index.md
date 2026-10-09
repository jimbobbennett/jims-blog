---
author: "Jim Bennett"
date: 2026-10-13
publishDate: 2026-10-13
description: "The EU AI Act's high-risk obligations read like an engineering spec: automatic logs, retention, human oversight, monitoring and explanations. Here's how Arize and evroc map to each one, from our joint webinar."
summary: "The EU AI Act's high-risk obligations read like an engineering spec: automatic logs, retention, human oversight, monitoring and explanations. Here's how Arize and evroc map to each one, from our joint webinar."
draft: true
slug: "eu-ai-act-compliance-arize-evroc"
title: "EU AI Act compliance for AI agents: building the engineering foundation with Arize and evroc"
tags: ["ai", "llm", "eu-ai-act", "compliance", "observability", "tracing", "evals", "phoenix", "evroc", "agents"]

images:
  - /blogs/eu-ai-act-compliance-arize-evroc/banner.jpg
featured_image: banner.jpg
hero: false
---

{{< youtube zK56LzfwJ5U >}}

## Key takeaways

- **The high-risk deadline is 2 December 2027, and transparency duties already apply.** The dates have moved once already because the work is hard to put in place. Start now rather than betting on another move.
- **Most high-risk obligations are engineering work.** Automatic logs, six months of retention, human oversight, post-market monitoring, incident handling, and explanations of decisions are things you build. Most of them are already good practice for running agents in production.
- **Know where your AI data is stored and who controls it.** Model calls, prompts, documents, and traces all live somewhere. Traces are the one teams forget.
- **evroc and Arize cover different layers.** evroc provides EU-only infrastructure and open-weight model hosting. [Phoenix](https://arize.com/docs/phoenix) and Arize AX provide tracing, [online evals](https://arize.com/docs/ax/evaluate/run-evals-on-traces), human review records, and versioned prompts.
- **Logs only count as evidence if you can prove what they say.** Integrity, completeness, retention, and privacy have to be designed in from the first trace.

If you build or deploy AI systems for the EU market, your agent's traces are your compliance evidence, and where they live is a compliance decision.

The EU AI Act places obligations on the builders and users of AI tools that are classed as high-risk: scoring credit, pricing life and health insurance, screening CVs, and supporting decisions in education or critical infrastructure. Those obligations read like an engineering spec: record events automatically, keep the logs, let humans oversee decisions, monitor after launch, and explain individual decisions. They're also close to what good teams already do to run agents in production, so if you already trace and evaluate your agents, then you have much of this in place.

Every log, prompt, document, and trace your agent produces is stored somewhere, and someone controls it. *Somewhere* means the country the data sits in, which decides which laws apply to it. *Someone* means the company that can read, change, or delete it, which decides whether the logs are "under your control," as the Act puts it. Under the Act and GDPR, you need to control both.

That was the focus of a recent webinar we ran with [evroc](https://evroc.com/), a European sovereign cloud provider headquartered in Stockholm. [Jim Bennett](https://www.linkedin.com/in/jimbobbennett/), principal developer experience engineer at Arize, and [Korey Stegared-Pace](https://www.linkedin.com/in/koreyspace/), developer relations engineer at evroc, walked through the parts of the Act that were relevant to engineering teams. They showed how an agent calling an LLM hosted on evroc, with its traces in self-hosted Phoenix, produced the evidence the Act asks for.

This post covers the timeline, the high-risk requirements, and how the two platforms help with each one. It's engineering guidance, not legal advice. Talk to your legal team about how the Act applies to what you are building.

## The EU AI Act timeline

The Act applies in phases. Some duties already apply, and the high-risk deadline is just over a year away.

![The EU AI Act timeline, with today falling between the August 2026 transparency rules and the December 2026 watermarking deadline](/blogs/eu-ai-act-compliance-arize-evroc/eu-ai-act-timeline.png)

### Already in force

| Date | In short | What applies |
|---|---|---|
| 2 Feb 2025 | Banned practices | Prohibited practices, such as social scoring and manipulative AI |
| 2 Feb 2025 | AI literacy | Take steps so the people who build, run, and use your AI understand it, for example through training for their role. Applies to every AI system, not just high-risk ones |
| 2 Aug 2025 | General-purpose AI | Obligations for providers of general-purpose AI models, such as documentation and transparency |
| 2 Aug 2026 | Transparency | Tell people they're dealing with an AI, and label AI-generated content |

### Still to come

| Date | In short | What applies |
|---|---|---|
| 2 Dec 2026 | Watermarking | Machine-readable marking for systems already on the market before 2 Aug 2026 |
| 2 Dec 2027 | High-risk systems | Logging, human oversight, monitoring, and the other obligations apply to high-risk use cases such as credit, insurance, hiring, and education |
| 2 Aug 2028 | Regulated products | The high-risk obligations extend to AI inside regulated products |

Transparency is already live, so user-facing agents should disclose that they're AI today, along with disclosing when content is AI generated. The model providers are starting to handle the labelling side. Anthropic now [watermarks text from new Claude models](https://www.anthropic.com/news/claude-text-watermark) worldwide, with no hidden characters added, and has signed the EU's code of practice on marking AI-generated content. OpenAI is [rolling out a text watermark for ChatGPT and Codex in the EU](https://openai.com/index/eu-text-provenance/), and API developers can switch it on for selected models. On the API it's off by default, so check what applies to the models your agent calls.

For most teams building high-risk systems, the important date is 2 December 2027. Despite being over a year away, it's not actually that long for the amount of work involved, especially for an org-wide collaboration between engineering and legal. During the webinar, one attendee said the EU AI Act was a significant engineering focus for their team this year, and a lot of engineering teams are now being told the same thing: get compliant, and start now.

## What the EU AI Act requires from high-risk AI systems

### Is your system high-risk?

The Act covers four tiers of AI application: unacceptable (banned), high-risk, limited (transparency duties), and minimal. High-risk is defined by use case. This includes credit scoring and creditworthiness, life and health insurance pricing, recruitment and CV screening, education, and critical infrastructure. If it has a significant impact on your life, it is high-risk.

![The four risk tiers of the EU AI Act, with Annex III high-risk examples and the fraud detection exclusion](/blogs/eu-ai-act-compliance-arize-evroc/eu-ai-act-high-risk-tiers.png)

Notably, fraud detection isn't covered. Annex III excludes AI systems used to detect financial fraud, so a bank's fraud model and its credit-scoring model can sit in different tiers.

### Provider or deployer?

The provider builds the AI system or sells it under their own name, such as a bank building its own credit assistant on a hosted model, or a recruitment software company selling a CV screening tool. The deployer uses it in their business, such as an employer building against a model, or using a vendor's CV-screening tool.

You can become the provider without building the system. You're treated as the provider if you put your name on a high-risk system, change it substantially, or use it for a new purpose that makes it high-risk. Fine-tuning a hosted model for a high-risk use may count, or re-branding a whitelabelled application.

The role matters because it decides what you own. Providers keep the logs, monitor the system after launch, and need written agreements with their suppliers. Deployers keep the logs under their control, and when they make a decision using a high-risk system, the affected person can ask them for an explanation for that decision.

For example, if you build a CV screening tool that you sell as a SaaS platform, you are the provider and you need to keep logs tracking all usage. Your customer who uses your tool is the deployer and keeps logs around which CVs are sent to your tool. If a candidate asks for an explanation of their screening decision, the deployer needs the logs that tracked the call to the tool, and the supplier needs the logs that show the actual decision making process.

Settle which role you're in with your legal team before you ship.

## The obligations engineering teams own

This is the part of the Act that lands on engineering.

| Article | Description |
|---|---|
| Article 12 | Automatic recording of events over the system's lifetime |
| Article 14 | Design for effective human oversight |
| Articles 19 and 26(6) | Keep logs for at least six months. For deployers, that applies "to the extent such logs are under their control." |
| Article 25(4) | A written agreement between the provider and third parties supplying tools, services, components, or models |
| Article 50 | Disclose AI interactions and label AI-generated content |
| Article 72 | Monitor the system after launch |
| Article 73 | Report serious incidents, and don't alter the system in a way that could affect the investigation before informing the authorities |
| Article 86 | People affected by a decision from an Annex III system (except critical infrastructure), with legal or similarly significant adverse effects, can obtain "clear and meaningful explanations of the role of the AI system in the decision-making procedure and the main elements of the decision taken." |

GDPR sits on top. Data minimisation makes six months the minimum, and longer retention needs a justification. You can do both, but only if you decide what goes into a log in the first place, such as using data redaction for PII.

### The compliance stack

A lot of engineers, particularly in regulated industries like banking, already track the provenance of the tools they use, such as npm or Maven packages. The idea of an SBOM, a software bill of materials, has been around for a while. The Act asks for the same discipline across the AI stack, and Article 25(4) makes it explicit through written supplier agreements. This stack has three layers:

1. **Your AI application.** The agent logic, the disclosure, and the routing to human reviewers. This is yours.
2. **Observability and evaluation.** Arize AX or Phoenix: traces, evals, annotations, and prompt versions.
3. **Infrastructure and models.** Compute, storage, and model hosting. evroc builds cloud and AI services hosted entirely in Europe, so no services or data leave the European Union.

![The three-layer compliance stack: your AI application, observability and evaluation with Phoenix or Arize, and infrastructure and models with evroc, all covered by Article 25(4) supplier agreements](/blogs/eu-ai-act-compliance-arize-evroc/eu-ai-act-compliance-stack.png)

Your agent's data lives in four places: model calls, prompts, uploaded documents, and traces. For each, ask which country it's in and who controls it. Teams usually answer that for the first three and forget traces, yet traces are the one the Act regulates directly, through Articles 19 and 26(6). The Act doesn't require any particular provider, but keeping all four in one jurisdiction makes the supply-chain questions easier to answer. Start with self-hosted Phoenix on your EU infrastructure, then migrate to a self-hosted enterprise Arize AX deployment when needed.

### How the requirements map to the stack

The application layer is yours in every row. The stack provides the engineering foundation and the evidence; your team decides how to use them.

| Requirement | What the Act asks | Arize AX/Phoenix | evroc |
|---|---|---|---|
| Art 12, record keeping | Automatic logs over the system's lifetime | Tracing across model calls, tools, and human steps |  |
| Art 14, human oversight | Effective human oversight | Human review recorded as annotations on the trace |  |
| Art 19 and 26(6), retention | Logs kept at least six months, under your control | A trace store with retention you set | EU VMs and storage for the trace store, with admin audit logs of cloud-side changes |
| Art 25(4), supply chain | Written agreements with suppliers of tools, services, and models | The observability and evaluation layer, as a named supplier | The infrastructure and model layer, as a named supplier |
| Art 50, transparency | Disclose AI interactions; label AI-generated content | Traces record what the agent said, including the disclosure |  |
| Art 72, post-market monitoring | Active monitoring after launch | Online evals on production traces, with monitoring and alerts | Hosting for the monitored models and the trace store |
| Art 73, serious incidents | Report incidents without altering the evidence first | [Versioned prompts](https://arize.com/docs/phoenix/prompt-engineering/overview-prompts) and preserved traces | Admin audit logs of cloud-side changes, such as deletions |
| Art 86, explanation | Clear and meaningful explanations of decisions | The trace as source material for the explanation | Keeps the decision record in the EU |
| GDPR, minimisation | Keep only what you need; justify longer retention | [PII masking at capture](https://arize.com/docs/phoenix/tracing/how-to-tracing/advanced/masking-span-attributes), with a join ID | No sharing with model providers |

## What it looks like in practice

In the session, we built an example credit assistant for a fictional Swedish bank, Nordbank. It's a LangGraph agent running on Qwen3 hosted on evroc, with traces in self-hosted Phoenix on an evroc VM in Stockholm. Credit scoring is an Annex III use case, so this is a high-risk system. We showed two requests made to this system that map to different parts of the Act.

### A request that goes to a human

The assistant opens with: "I'm Nordbank's AI credit assistant. I'm an automated AI system, not a person." That's the Article 50 disclosure about being an AI tool, and because it's part of the conversation, it's in the trace as well as on the user's screen.

A customer uploads their bank statements and asks for a higher credit limit. The request is over the automatic approval threshold, so the agent routes it to a human underwriter without the customer having to ask. The underwriter reviews it, records a reason, and approves. That's Article 14 human oversight, built into the flow rather than left for the customer to demand.

In Phoenix, the trace records the whole turn, which is Article 12 in action. It holds the customer's message, links to the uploaded statements, every tool call with its inputs and outputs, the model call to Qwen3 on evroc, and the final human review gate. The underwriter's decision appears as a follow-on step. The trace also records which system prompt was in use, which holds the bank's lending policy.

The customer profile tool handles addresses, account numbers, IBANs, and personal identity numbers. These are masked at capture, and the trace keeps an ID that joins back to the customer record in another system. That's the GDPR side: you can keep traces for the six months that Articles 19 and 26(6) ask for without storing anything that identifies the customer. Because the trace store runs on an evroc VM in Stockholm, the record stays in the EU and under the bank's control.

### A request that goes wrong

Then a second customer, Erik, asked to raise his limit from 20,000 SEK to 40,000 SEK. The agent approved it, counting 9,000 SEK a month in Swish transfers from his sister as income. They were loan repayments, and Nordbank's policy says transfers from family are never income.

An online eval on production traces caught it and marked the trace. That's Article 72 post-market monitoring: checking that the live system follows the rules, not just that it passed tests before launch. In production, you'd alert on failures like this through tools like Slack or PagerDuty.

The trace pointed at a version of a system prompt maintained in Phoenix. We wrote a new version, tested it against the same cases (the old version passed 4/6, the new passed 6/6), and shipped it by moving a tag to maintain traceability in the Phoenix prompt store. When we reran Erik's request, the agent picked up the new prompt, and rejected the request. The new trace showed the new version.

Nothing was overwritten along the way. Both prompt versions and Erik's original trace are preserved, so the record shows what went wrong, what changed, and when. If a mistake like this were ever a serious incident, that's what Article 73 needs: the evidence left intact until the authorities have been told.

If a customer asks why they were turned down, which is their right under Article 86, the trace is the source material for that explanation. Someone still has to write it up in plain language for them. You can't just download the trace as JSON and email that to them, but you have the building blocks to write the report.

## What makes logs count as evidence

Logs are claims. Evidence is something you can prove, and there are four properties that make this happen:

- **Integrity:** tamper-evident, append-only storage, with restricted delete rights and cloud-level audit trails for changes made outside the trace store.
- **Completeness:** capture by design, not by accident. Instrument the whole agent path, including tools and human review.
- **Retention:** six months minimum on durable storage, with a justification for anything longer.
- **Privacy:** redact personal data before it's stored.

No tool settles all of this for you. Balancing retention against minimisation, or deciding who controls logs on a managed cloud, takes your engineering and legal teams working together.

## Start building your compliance foundation

The dates have moved before. The Digital Omnibus on AI, Regulation (EU) 2026/1744, came into force on 27 July 2026 and pushed the high-risk deadlines back: Annex III systems from 2 August 2026 to 2 December 2027, and Annex I products from 2 August 2027 to 2 August 2028. They moved because the work is substantial, and they may move again. Don't plan around that. Start with one agent:

1. Work out whether any of your AI use cases fall under Annex III.
2. Instrument now.
3. Decide where your traces live, and for how long.
4. Redact personal data at capture.
5. Put evals on production traffic, not just pre-launch tests.

That checklist is also the improvement loop: trace, evaluate, fix, and ship, with the record intact. For a metrics and dashboards view of the same obligations, read [EU AI Act compliance: what AI engineering teams should monitor](https://arize.com/blog/eu-ai-act-compliance-what-ai-engineering-teams-should-monitor/).

None of this makes a system compliant on its own. It gives you the engineering foundation and evidence that support compliance.

Get started with Phoenix and Arize AX at [arize.com](https://arize.com), and try evroc's EU-hosted infrastructure and models at [evroc.com](https://evroc.com).

[Watch the full webinar](https://youtu.be/zK56LzfwJ5U).
