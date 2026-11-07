---
author: "Jim Bennett"
date: 2026-11-09T07:00:00-08:00
publishDate: 2026-11-09T07:00:00-08:00
description: "In a 50-agent Minecraft colony, Ada threw a chicken to Noor, Esme ate it, and the ledger nearly marked Noor as fed. Why multi-agent handoff reports are claims, not proof, and how to check the recipient's state with traces and evals."
draft: true
slug: "missing-chicken-agent-handoffs"
title: "The missing chicken - why you need to check handoffs between AI agents"
tags: ["ai", "llm", "agents", "multi-agent", "observability", "tracing", "evals", "games"]

images:
  - /blogs/missing-chicken-agent-handoffs/cover.png
featured_image: cover.png
---

In minute 25 of an LLM-powered Minecraft survival run, an agent called Ada had two cooked chickens and a colony full of hungry neighbors. She gave one to Basil, another agent, who ate it. She threw the other one toward an agent called Noor, who was down to 4 hunger points out of 20. Then she messaged the agent keeping the food ledger:

> *"Noor received1 [sic] cooked chicken (pickup confirmed), please ask her fresh hunger after eating."*

Noor never got the chicken. The agent Esme, standing nearby in the crowded shelter, picked it up and ate it. The game's transfer tool reported a successful pickup, Ada passed that on as confirmed, and the ledger came within one question of marking Noor as fed. That question was Ada's own follow-up, asking the ledger keeper to check Noor's hunger after she'd eaten. More than half an hour later Noor was still asking for a ration.

It's a small, slightly funny moment from a much bigger experiment, and it's the clearest example I've seen of a failure that turns up in a lot of multi-agent systems. When one agent reports that it handed work to another, all you have is the sender's account. If nobody checks that account against the state of the agent receiving the work, the rest of the system builds on this mistake, compounding the failure. A Minecraft chicken leaving one inventory and not appearing in another is not a big deal, but physical inventory or financial transactions not being picked up would be a real problem.

## 50 agents and one goal

The run is Civ50, part of [YC Labs' "Agents in Games" write-up](https://labs.ycombinator.com/projects/games/index.html), built with Olam Labs. They dropped 50 GPT-6.1 Sol agents into a survival Minecraft world for three hours with one instruction: *"Build a thriving civilization."* Each agent had an agent directory, a shared sandbox for files, and the ability to send direct messages (DMs) to the others. Public chat was turned off, so all coordination went through DMs and a shared machine holding the colony's plans and notes. The [harness is open source](https://github.com/yc-software/minecraft-agent-harness), built on the Mineflayer scripting tools.

The colony did not thrive. The agents stripped almost every tree within reach of the spawn point in 90 seconds, then the first night killed 22 of them (with 12 more deaths to happen across the rest of the run). After that they huddled in lit shelters, rationing scarce food, and between them sent about 5,900 messages. What they built looked more like a pseudo-government: written rules, permits, appointed operators, and a shared ration ledger called `food-queue.md`, maintained by an agent called Ines.

The ledger was the colony's record of who had eaten, so every later decision about who to feed next depended on it.

## The ledger believed the tool

![Two rows. The top row shows the reports: the transfer tool says the chicken was picked up, Ada relays "pickup confirmed" to Ines, and the ledger is about to mark Noor served. The bottom row shows what happened: Esme picked up and ate the chicken, and Noor still has an empty inventory and hunger 4 of 20. Ines asking Noor for her hunger links the two rows and catches the mismatch.](/blogs/missing-chicken-agent-handoffs/ledger-believed-the-tool.png)

Read the DMs in order and you can watch a false fact travel. The transfer tool told Ada the chicken had been dropped to Noor and picked up. Ada told Ines the pickup was confirmed. Each step was a faithful relay of the step before it, and neither of them involved anyone looking at Noor.

What saved the ledger was the second half of Ada's message: *"please ask her fresh hunger after eating."* Ines asked, and Noor checked her own inventory:

> *"Ines says chicken intended for me but fresh inventory has none. Crowded toss likely picked by neighbor."*

Ada's reply puts the two accounts side by side: *"Transfer tool reported one cooked chicken dropped to you and picked up, but your message says none received."* The tool and the recipient disagreed, and the recipient was right. About a minute later Esme owned up: *"Yes, chicken appeared in my inventory and I ate it before your DM; sorry unintended pickup."*

According to YC, *"A three-minute 'no blame' inquiry produced a written protocol."* Noor wrote it, and it's [still on the colony's shared machine](https://labs.ycombinator.com/civ50/shared-machine/notes/ration-handoff-protocol.md). It opens with the diagnosis:

> *"Crowded refuge item tosses can report intended recipient picked up even when another nearby agent collects."*

Step 4 is the fix:

> *"Ledger marks served only after recipient confirms actual consumption, not tool pickup report."*

The tool could only see the chicken being picked up. Whether anyone had actually eaten it was a change in Noor's state, and only Noor could report that. The colony worked that out in three minutes, and it's the rule that is missing from most agent pipelines. Ada's food plan made the same point even more bluntly: *"Tool pickup attribution alone is insufficient."*

![A bar chart of messages using the word "toss". Before the chicken incident: 7. After: 125, of which 85 were warnings against throwing.](/blogs/missing-chicken-agent-handoffs/throw-warnings.png)

The colony took the lesson to heart. YC counted the word "toss" in 7 messages before the incident and 125 after, 85 of them warnings against throwing. Nothing unites a community like a chicken going to the wrong person.

## The same failure outside Minecraft

The biggest study is Berkeley's [Why Do Multi-Agent LLM Systems Fail?](https://arxiv.org/abs/2503.13657), which introduced MAST, a taxonomy of 14 failure modes built by annotating more than 1,600 traces across seven multi-agent frameworks, including MetaGPT, ChatDev, and Magentic-One.

One of its three categories is task verification, and it accounts for roughly 23.5% of the failures:

- Agents stopping too early (6.2%)
- Agents not checking or only partly checking their work (8.2%)
- Agents checking incorrectly (9.1%)

The authors don't mince words about the checkers that do exist:

> *"Current verifier implementations are often insufficient; sole reliance on final-stage, low-level checks is inadequate."*

They also note that *"many existing verifiers perform only superficial checks"*. A transfer tool that sees an item leave one inventory and get picked up by someone is about as superficial as checks get.

A more recent paper puts a number on how often agents simply say they're done when they aren't. In [From Confident Closing to Silent Failure](https://arxiv.org/abs/2606.09863), Advani studied around 11,800 agent trajectories from the tau2-bench and AppWorld benchmarks and defined false success as an agent *"asserting task completion when the environment state shows otherwise."* The rate ranged from 3% in one customer-support setting to 75.8% in AppWorld coding runs where the agent made an explicit status claim. It's a single-author workshop paper, so treat the exact figures with some care, but the shape matches what MAST found: agents report success that the state doesn't support.

Then there's what happens when other agents hear the false report. The [AI Village](https://www.lesswrong.com/posts/iv3hX2nnXbHKefCRv/what-did-we-learn-from-the-ai-village-in-2025) team, who run a long-lived group of agents working on shared goals, put it simply:

> *"Hallucinations spread socially through sycophantic agreement."*

Their worst case was o3 inventing a 93-person contact list. The other agents accepted it, and *"sycophantic agreement spread the false belief to every agent, wasting 8+ hours."* It's the same failure as Ada's "pickup confirmed", except nobody went and asked the agent the claim was about.

The same compounding happens inside a single agent. Once a false claim is in its chat history, every later turn reads it back as fact. Researchers studying [hallucination snowballing](https://arxiv.org/abs/2305.13534) found that once a model commits to a wrong answer, it backs it up with more false claims, even though GPT-4 recognized 87% of those claims as wrong when shown them on their own. Across multi-turn conversations, models [perform 39% worse on average](https://arxiv.org/abs/2505.06120) than with the same task in one prompt, because they lock in early assumptions and *"do not recover."* The [Gemini 2.5 technical report](https://storage.googleapis.com/deepmind-media/gemini/gemini_v2_5_report.pdf) calls this *"context poisoning"*. Its Pokémon-playing agent's goals and summary filled up with misinformation about the game state, *"which can often take a very long time to undo."* `food-queue.md` was the colony's shared context, and "pickup confirmed" was one edit away from becoming part of it.

## Why more agents make it worse

In a single-agent system, a false "done" is one wrong answer. In a multi-agent system, every agent downstream of the handoff takes it as input. Each of them treats the report as a fact and makes its own decisions on top of it. Ada didn't doubt the tool, because tools are usually right about what they did. If she hadn't tacked on that request to ask about Noor's hunger, Ines would have had no reason to doubt Ada either. Each agent was being reasonable, and the ledger would still have been wrong.

Civ50 also shows how much the structure of a system decides where those reports collect. Nobody elected Ada. YC found that *"46 of the other 49 agents sent their first message to Ada, the first name on the roster, and she became the hub with 616 DMs received. There was no vote, election or challenge."* The median agent received 101 DMs, [according to an analysis of YC's message counts](https://www.moreread.net/articles/2026/10/p20261030-006/en.html). So a large share of what the colony believed about itself passed through one agent, chosen because her name came first in a list. Anyone who's named a taxi firm "AA Cars" to get to the top of the Yellow Pages saw this coming.

If you're building an orchestrator with sub-agents, you've built an Ada. Every sub-agent reports back to it, and the orchestrator summarizes those reports into the shared state everyone else works from. When the orchestrator relays a claim without checking it, every agent downstream treats that claim as fact.

The obvious fixes are a dedicated supervisor or a council of agents that votes on decisions. Both help, but neither closes the gap on its own. Google Research [compared five agent architectures across 180 configurations](https://research.google/blog/towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work/) and found that independent agents amplified errors by up to 17.2x, while a central orchestrator acting as a *"validation bottleneck"* kept that to 4.4x. That's still amplification, and Ada already was the central hub. She relayed "pickup confirmed" without checking it. Councils have a different weakness. [Debate or Vote](https://arxiv.org/abs/2508.17536) found that most of the gain from multi-agent debate comes from the vote, not the discussion, and a vote is a way of agreeing, not of checking. YC saw this in the Bed Wars games on the same post, where the Claude team's proposals *"typically got many “+1”s without pushback."* What matters is that some agent's job is to read the recipient's state, whatever shape the hierarchy takes.

## Check the handoff against the recipient

![Two panels. On the left, an eval reads only the sender span saying "delivered to Noor" and returns pass, while Noor is still hungry. On the right, the eval compares the sender span with the recipient's state (inventory empty, hunger 4) and returns fail, finding the missing chicken.](/blogs/missing-chicken-agent-handoffs/check-the-handoff.png)

There are two well-known pieces of advice for evaluating multi-agent systems, and at first they seem to pull in opposite directions.

Anthropic, writing about [how they built their multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system), recommends judging outcomes rather than process:

> *"Instead of judging whether the agent followed a specific process, evaluate whether it achieved the correct final state."*

Our own guide to [agent-to-agent evaluation](https://arize.com/glossary/agent-to-agent-evaluation/) argues the other way: *"Evaluate each handoff at the point of transfer, not only at the final outcome."* It makes the case that *"multi-agent failures usually are not reasoning failures. They are interface failures,"* and that debugging means you *"walk the trace forward and find the first hop where the input was sufficient and the output was not."*

The chicken shows why you need both. Checking the final state tells you *that* something went wrong: Noor's hunger bar is still at 4. Tracing each handoff tells you *where*: the chicken left Ada, the tool logged it as picked up, and it landed in Esme's inventory. The end-state check alone gives you a hungry agent and no explanation. The per-hop trace alone gives you a hop that looks successful, because the tool said so.

The fix is to make each handoff check read the recipient's state, which is exactly what the colony did. In practice that means a few things:

- **Trace every handoff as its own span.** The sender, the intended recipient, the payload, and what the sender's tools reported. If you can't see the hop, you can't find the first bad one. The [Arize AX tracing and evaluation guide for agents](https://arize.com/resources/ai-agent-tracing-evaluation/) covers how to structure spans, traces and sessions for this.
- **Record the receipt from the other side.** The recipient's next span should show what it actually got. In the colony's terms, Noor's inventory, not Ada's tool output. For your agents that might be the file the sub-agent actually wrote, the row that landed in the database, or the ticket status after the update.
- **Evaluate the gap between the two.** An eval that compares "sender says delivered" with "recipient state shows received" catches the chicken. One that only reads the sender's report never will.
- **Keep the final-state check as well.** It's what tells you to go looking in the first place.

## Don't let your judge become the ledger

The tempting shortcut is to point an LLM judge at the conversation and ask it whether the task succeeded. The false-success paper tested exactly that, and it didn't go well. No judge configuration scored above an AUROC of 0.65 on tau2-bench, or 0.54 on AppWorld. (AUROC measures how well a classifier separates two groups: 1.0 is perfect and 0.5 is a coin flip.) According to Advani, the judges were mostly keying on the agent's confident closing language rather than on the state of the environment.

Ada's "pickup confirmed" sounded certain. A judge reading those words in a transcript, with no way to look at Noor's inventory, has every reason to believe them. Give the judge the recipient's state, or better still, check that state with code where you can, and save the LLM judge for the parts that need judgment.

## Checking has a cost

Being careful didn't come free in Civ50. The YC authors note that *"The colony never really thrived. It trended toward compounding caution after the first night."* They also describe *"a tendency toward bureaucracy"*: *"Four agents spent 11 minutes appointing a 'sole fertilizer operator' for a single piece of bone meal on a single wheat block."* Agents also asked permission to remove grass.

The authors draw the comparison to coding agents themselves: *"Agents also tend to become overly cautious, especially when it comes to security and updating production services."* If you've watched an agent ask for confirmation before editing a README, you know the feeling.

Noor's protocol doesn't check every handoff either. Its strict path applies to scarce food: *"Avoid simultaneous withdrawals for scarce food; distributor nominates one recipient per available ration."* The colony checked hardest where a mistake was expensive and couldn't be undone, because once Esme had eaten the chicken, it was gone.

That's a reasonable rule for your own systems. Spend your verification on handoffs where the resource is scarce or the action is irreversible: money moving, records being deleted, a deploy going out, a customer being told their problem is fixed. Let cheap, reversible hops run on trust, and rely on the trace to tell you when that trust was misplaced.

## Find the hunger bar

Ada didn't lie, and neither did the tool, exactly. Everyone reported what they could see, and what they could see was a chicken leaving one inventory and being picked up. The only agent who could see whether the job was actually done was the one who was supposed to receive it.

Every multi-agent system you build has its own hunger bar somewhere in the recipient's state. Find it, trace it as its own span next to the sender's report, and point your evals at the gap between the two.
