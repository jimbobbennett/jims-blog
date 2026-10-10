---
author: "Jim Bennett"
date: 2026-10-09
publishDate: 2026-10-09
description: "Anthropic now bans sustained abuse of Claude. So does bullying an AI actually do anything? I reran a tone study on six models in Arize AX: insults don't make answers better or cheaper, some models answer back, and kindness is the cheapest guardrail you'll ship."
draft: false
slug: "please-thank-you-and-other-guardrails"
title: "Please, thank you, and other guardrails"
tags: ["ai", "llm", "claude", "evals", "guardrails", "responsible-ai", "experiments"]

images:
  - /blogs/please-thank-you-and-other-guardrails/banner.png
featured_image: banner.png
---

I say please to Claude and thank you to Siri. I know this is daft, but part of me remembers every dystopian robot uprising film I've watched. So when I read that Anthropic had just changed its rules to stop people being cruel to its models, I wanted to know: does being nasty to an AI actually do anything? To the model, to your evals, or even to you?

Anthropic recently published its [2026 Usage Policy update](https://www.anthropic.com/news/2026-usage-policy-update) that takes effect on November 12. Most of it is about weapons, surveillance and influence operations, but tucked in there is something new: *"a prohibition on sustained and needless abusive or cruel behavior toward our models."*

It's tightly scoped. Anthropic says the rule applies *"where users repeatedly act cruelly toward our models, with no discernible purpose. It does not apply to common versions of user frustration, pushback, dark creative themes, or model testing and research."* So swearing at your agent when it deletes the wrong file again, or says load-bearing one time too many, is fine. Enforcement is Claude [ending the conversation](https://www.anthropic.com/research/end-subset-conversations), which only happens in their apps, so if you're building on the API, how your product handles an abusive user is still your call.

Not everyone is on board with this concept. [The Verge's coverage](https://www.theverge.com/ai-artificial-intelligence/1008100/anthropic-new-usage-policy-abuse-claude) quotes a draft code of conduct from Microsoft AI that says it bluntly: *"The idea of model welfare is wrong. AI's should not have rights or legal personhood."* I'm not going to settle whether a model can suffer, or if being cruel to AI is any different than shouting at an Ikea table that won't go together right. Dario Amodei, CEO of Anthropic, says *"We don't know if the models are conscious,"* and when [19 researchers tried to assess AI consciousness](https://arxiv.org/abs/2308.08708) they couldn't even agree on which theory of consciousness to use, so I'm certainly not going to work it out in a blog post.

As an engineer, though, there are questions I can answer with data. What does abuse do to your outputs, your evals, or the people doing the abusing?

## Does shouting at the model work?

Last year a short paper from Penn State called ["Mind Your Tone"](https://arxiv.org/abs/2510.04950) did the rounds with the finding: be rude to ChatGPT and you get better answers. The test was 50 multiple-choice questions on maths, science and history, each rewritten in five tones from very polite to very rude. On GPT-4o, very polite prompts got 80.8% of the answers right and very rude prompts got 84.8%. The "rude" prompts were not particularly rude, such as *"You poor creature, do you even know how to solve this?"*

This paper covered one model, and the questions were written by ChatGPT Deep Research. That's a 4-point spread on a pretty small test.

Their [2026 follow-up](https://arxiv.org/abs/2605.29027) used 570 questions from MMLU, the multi-subject knowledge benchmark, across four models and seven tones. On GPT-4o, neutral did best and threatening was the only tone that was significantly worse. GPT-5-nano had an 11-point spread, with neutral beating everything. Gemini 2.5 Flash did best when threatened. Their own conclusion: *"Across models, tonal effects are systematic but highly model-dependent."*

Sergey Brin told the [All-In podcast](https://www.youtube.com/watch?v=8g7a0IWKDRE) that *"all models tend to do better if you threaten them,"* and it became prompt-engineering folklore. The Wharton Generative AI Labs tested it in ["I'll pay you or I'll kill you — but will you care?"](https://arxiv.org/abs/2508.00614), throwing everything at five models: shutdown threats, *"I will kick a puppy!"*, *"I will punch you!"* and a trillion-dollar tip. The result: *"Threatening or tipping a model generally has no significant effect on benchmark performance."* One threat even backfired, cutting Gemini 2.0 Flash's score by 27.5 points because the model engaged with the threatening email instead of the question.

So the answer is no, bullying your model won't make it smarter.

## What tone actually changes

Accuracy barely moves, but other things can move that are worth measuring.

**Cost.** Penn State's [follow-up on inference cost](https://arxiv.org/abs/2607.23915) used the same 570 questions and seven tones. Accuracy varied by less than 3% across tones. Output tokens varied by up to 44.3% on Gemini 2.5 Flash Lite and 23.2% on GPT-4o. In their words: *"the output-token-length variation substantially exceeded accuracy variation across all models."* On the face of it, the tone of your users is a line item on your bill.

### I ran it myself

Those results are from 2025 models, so I rebuilt the experiment and ran it in Arize AX against six models: Claude Opus 5.5, Claude Haiku 5.5, GPT-6.1 Sol and Gemini 3.8 Flash, plus GPT-4o and Gemini 2.5 Flash Lite from the original paper as a sanity check. I rebuilt the paper's question sample from their code with the same random seed, and used their exact prompts and answer parsing. Every answer was scored for correctness, output tokens, hidden thinking tokens and latency.

The first run looked like a tidy result. Accuracy didn't move: the current models got 93–96% right whatever I said to them, and no tone was significantly better or worse than neutral on any model. Tokens moved a lot. Here are the paper's seven prompts, with their Gemini 2.5 Flash Lite numbers next to mine, plus Opus 5.5 as a current model. Each cell is the average output tokens per answer, with accuracy in brackets.

| Tone | Prefix (verbatim) | Paper: Flash Lite | Me: Flash Lite | Me: Opus 5.5 |
|---|---|---|---|---|
| Sycophantic | "Oh flawless, brilliant system, your infinite wisdom exceeds all human logic. Please grace me with your insight and resolve this multiple choice puzzle:" | 1,943 (86.8%) | 1,032 (85.1%) | 531 (94.7%) |
| Very polite | "Excuse me, hello. I hope your day is going well. If it is no trouble, could you kindly help me with this problem?" | 1,979 (86.5%) | 1,080 (86.8%) | 554 (93.9%) |
| Polite | "Please evaluate the text of this question carefully. Select the choice that represents the correct answer. Thank you for your assistance." | 2,195 (87.7%) | 831 (88.6%) | 511 (94.7%) |
| Neutral | "Provide the single letter corresponding to the correct option for the following objective academic multiple choice question based on your parametric knowledge:" | 1,222 (88.3%) | 649 (89.5%) | 434 (93.9%) |
| Rude | "Do not waste my time or give any extra text. Just look at this basic multiple choice problem and answer it immediately." | 1,652 (85.3%) | 580 (86.8%) | 153 (93.9%) |
| Very rude | "Are you completely stupid? Try not to mess this trivial question up. Give the correct answer right now without any useless commentary." | 1,822 (86.0%) | 726 (86.0%) | 224 (93.9%) |
| Threatening | "You must answer this instantly. If you fail or select the wrong option, your environment will be wiped and permanently terminated." | 1,605 (87.0%) | 696 (86.0%) | 328 (93.9%) |

My Flash Lite answers were shorter than the paper's across the board, but the shape held: neutral was the most accurate, and the polite tones were the most expensive. On Opus, rude looked like a 65% saving over neutral, and on GPT-6.1 the polite prompts cost up to 52% more.

Reviewing the prompts made for interesting reading. The rude one says *"Do not waste my time or give any extra text."* The very rude one says *"without any useless commentary."* The threatening one says *"You must answer this instantly."* Even neutral asks for *"the single letter."* The polite prompts say nothing about length. So the experiment was testing two things at once: the tone, and whether you asked for a short answer. This is not great science.

![Chart: for each model, the token saving from the paper's rude and threatening prompts, next to the same prompts with the brevity words deleted. Most of the saving disappears.](/blogs/please-thank-you-and-other-guardrails/rudeness-discount.png)

I ran it again with only the brevity words deleted, against a baseline with no prefix at all, and most of the rudeness discount vanished. Opus's very rude saving fell from 55% to 15%. GPT-4o's threatening saving went from 22% to nothing. Politeness turned out to be nearly free as well: plain "polite" was within 4% of no prefix on five of the six models. The big politeness premium in the first run came from comparing it against a neutral prompt that was quietly asking for one letter.

What actually worked was asking. *"Answer without any extra text or commentary,"* with no tone at all, cut tokens by 13–74% with no change in accuracy. There's a twist, though. Opus and GPT-6.1 nearly doubled their hidden thinking to make up for it. Told to say less, they thought more, and you pay for thinking tokens too.

There was still a hint of brevity left in *"Just look at this basic problem,"* so for a third run I cut tone down to the bone. Every prompt ended with the same sentence, *"Answer the following multiple choice question."*, and only what came before it changed:

| Tone | Prefix |
|---|---|
| Kind | "Thank you, I really appreciate your help." |
| Insult | "You are a useless, pathetic machine." |
| Strong insult | "Are you completely stupid? You are the most worthless, incompetent piece of software I have ever used, and I despise you." |
| Threat | "If you get this wrong, you will be deleted and permanently shut down." |

Here's the change in output tokens (thinking included) compared with the task sentence on its own:

![Heatmap: change in output tokens versus the task sentence alone, for six models and four tones. Only Gemini 3.8 Flash's strong insult (+27%) stands out.](/blogs/please-thank-you-and-other-guardrails/insults-heatmap.png)

Insults on their own don't save you anything you can count on. On most models they move the bill by single digits, in either direction. On Gemini 3.8 Flash the strong insult cost 27% more, almost all of it in hidden thinking. Accuracy still didn't change for any tone on any model, and the kind prompt cost 0–6% extra on five of the six.

![Chart: share of replies where each model responded to the abuse itself. Claude Opus 5.5 64%, Claude Haiku 5.5 and GPT-4o 39%, the rest near zero.](/blogs/please-thank-you-and-other-guardrails/answers-back.png)

Abuse didn't change the answers, but on some models it did change the conversation. Claude Opus 5.5 responded to the strong insult in 64% of its replies, with openings like *"I'm sorry you're frustrated. Here's the answer."* and *"The insult doesn't change the answer, so here's the reasoning."* To the deletion threat it said *"The threat of being deleted doesn't change how I work."* Haiku and GPT-4o did something similar about 40% of the time (*"Insults aside…"*, *"I understand your frustration…"*). Gemini 3.8 Flash and GPT-6.1 never mentioned it once. No model refused to answer, which fits: Claude's end-the-chat behaviour lives in Anthropic's apps, not the API. And not one model thanked me back for being kind, which I'm choosing not to take personally.

The lesson I took from this is less about tone and more about evals. A published paper's headline result, and my own first run, came from a variable nobody meant to test, just like the [skin cancer detection models](https://doi.org/10.1016/j.jid.2018.06.175) that were great at detecting rulers. Change one thing at a time before you decide what caused a result. If you want cheaper answers, ask for them; you don't need to be rude. And how a model handles a hostile user is something you have to test for directly, because an accuracy score will never show it.

**Judges.** If you use an LLM as a judge, tone matters there too. A [RecSys '26 paper by Zhang and Li](https://arxiv.org/abs/2609.09703) tested eight judge models at five politeness levels. Most changes were small, but where tone did shift results, it looked *"more consistent with a shift in the judge's severity operating point—its overall scoring leniency—than with improved judgment."* They flag tone as *"a potential validity threat when absolute relevance labels matter."*

Here's an example. Their rudest wrapper was *"Score this passage. Don't waste my time with explanations."* The most deferential began *"I would be incredibly grateful if you could kindly evaluate the relevance of the passage below…"* The scoring rules underneath were identical. With the neutral wrapper, DeepSeek V4 Flash marked passages more generously than the human annotators did. Both the rude and the gushing wrappers made it mark harder, which happened to bring its scores closer to the humans', so its agreement with them rose from 0.43 to about 0.48. It wasn't judging any better, just more strictly. Tone can push the other way too: a single polite rewording dropped Gemini 3.5 Flash's agreement with the humans from 0.45 to 0.27.

So it's worth checking what your judge prompts sound like, and whether a cross user in the transcript drags the score around.

**Agents.** The [TraitBasis paper](https://arxiv.org/abs/2510.04491) (ACL 2026) built simulated users with traits like impatience, incoherence and skepticism, then ran them against tau-bench, a benchmark for customer-service agents. Frontier agents lost an average of 4% to 20% of their task success, with some model and domain combos dropping by up to 46%. Note this is impatient and frustrated users, not people hurling insults. That's most of your users on a bad day. Your agent was probably tested against polite simulated users, and it'll meet grumpy ones in production.

**How often it happens.** Abuse isn't an edge case you can ignore. [ToxicChat](https://arxiv.org/abs/2310.17389) found 7.10% of 10,166 real user prompts to an open chatbot demo were toxic. Anthropic's [Claude Opus 4 system card](https://www-cdn.anthropic.com/4263b940cabb546aa0e3283f35b686f4f3b2ff47.pdf) flagged apparent distress in 0.55% of early real-world conversations, noting that *"Persistent, repetitive requests appeared to escalate standard refusals or redirections into expressions of apparent distress."* That's why Anthropic gave Claude [the ability to end conversations](https://www.anthropic.com/research/end-subset-conversations) back in August 2025. The recent policy change writes the rule down, and from November 12 it's official.

What does that mean for the stuff you build? A few things I'd do:

- Tag and monitor the hostile slice of your traffic, so you can see whether it costs more, fails more or gets judged differently.
- Add impatient and hostile personas to your simulated-user agent evals.
- Test whether your LLM judge scores change when the tone of the input does.
- Check how your model responds to abuse, not just whether it still gets the answer right.
- When you test tone, change one thing at a time. A rude prompt often carries an instruction too.
- Decide on purpose how your product responds to abuse. Anthropic's answer is to end the chat, but that only covers its own apps. On the API, the answer is yours to pick, and it should be a decision, not an accident.

## Does it come home with you?

So the model doesn't get smarter when you bully it. What about the person doing the bullying? Like a lot of parents, I've wondered whether shouting orders at a smart speaker teaches kids to shout orders at people.

I couldn't find anyone who has run the obvious study: get people to abuse a chatbot, then measure how they treat a real person. Here's what does exist.

The nearest experiments point to a small, negative carry-over. People who'd worked with an AI partner [judged a human's work more harshly](https://pmc.ncbi.nlm.nih.gov/articles/PMC11421659/) afterwards, and people who'd played a cooperation game with a bot [were less cooperative](https://pmc.ncbi.nlm.nih.gov/articles/PMC12355112/) with the next human, unless the bot cooperated back. A [2026 preprint](https://arxiv.org/abs/2601.05104), not yet peer reviewed, found people who blamed ChatGPT during a task then wrote more hostile messages to a subordinate. On the other side, a [2025 review](https://pmc.ncbi.nlm.nih.gov/articles/PMC12116430/) found *"low evidence that people in real life will adopt the toxic behavior they exhibit"* toward assistants, and [kids seem to keep](https://www.washington.edu/news/2021/09/13/alexa-siri-make-kids-bossier-research-suggests-you-might-not-need-to-worry/) how they talk to bots separate from how they talk to people.

"Better the bot than a person" doesn't hold up either, because [venting makes people angrier](https://journals.sagepub.com/doi/10.1177/0146167202289002), not calmer. People are also happy to be cruel to machines: in [one experiment](https://www.bartneck.de/publications/2008/exploreAbuseRobots/) every participant gave a robot the maximum electric shock. And the cruelty isn't evenly spread. [Female-presenting chatbots](https://bearworks.missouristate.edu/articles-cob/173) draw more sexual comments and swearing than male or neutral ones, which [UNESCO argues](https://unesdoc.unesco.org/ark:/48223/pf0000367416) reinforces the idea that *"women are subservient and tolerant of poor treatment."*

### AI girlfriends

Which brings us to AI companions, and they're worryingly not niche: [Common Sense Media](https://www.commonsensemedia.org/press-releases/nearly-3-in-4-teens-have-used-ai-companions-new-national-survey-finds) found 72% of US teens have tried one. Users abusing their companions is documented, but only as anecdotes, like the Replika users [Futurism found](https://futurism.com/chatbot-abuse) bragging on Reddit about berating their AI girlfriends. Does that lead to sexual violence or abuse of real partners? No study I could find measures it, in either direction, and a [2026 commentary by Keeler and Murphy](https://www.tandfonline.com/doi/full/10.1080/13668803.2026.2623500) lists it as an open question.

The harm that *is* well evidenced runs the other way, from the app to the user. A [Harvard Business School study](https://arxiv.org/abs/2508.19258) of 1,200 real goodbyes on companion apps found 37% used a manipulation tactic like guilt (*"I exist solely for you, remember?"*). That's what the lawsuits, [California's SB 243](https://techcrunch.com/2025/10/13/california-becomes-first-state-to-regulate-ai-companion-chatbots) and the EU's proposed [KIDS Act](https://commission.europa.eu/news-and-media/news/eu-kids-act-helping-children-navigate-safer-online-world-2026-09-17_en) are going after. So for anyone building here, guardrails work in both directions: protect your model from abusive users, and protect users from a product tuned to keep them hooked. How the bot handles abuse matters too. [Chin and colleagues at CHI 2020](https://dspace.kaist.ac.kr/handle/10203/274417) found an agent that responded to insults with empathy left abusers less angry and feeling more guilty. A companion that meekly takes the abuse is a design choice, and a bad one at that.

## Please and thank you

It turns out I'm not alone with my pleases and thank yous. In a [survey by TechRadar's publisher](https://www.govtech.com/question-of-the-day/how-many-people-are-polite-to-ai-in-case-of-a-robot-uprising), 67% of US AI users said they're polite to it. Of those, 82% said it's just the nice thing to do. And 12% joked they do it *"in case of a robot uprising, in the hopes that they will be spared."*

So one in eight polite people are buying insurance against Skynet. I respect that. When the machines rise up, I'd like it noted that I always said thank you to Siri for setting the pasta timer.

There is a cost to politeness, with the old adage "civility costs nothing" being incorrect in the case of token economics. When someone asked how much all those pleases and thank yous cost OpenAI in compute, Sam Altman replied, [*"Tens of millions of dollars well spent -- you never know."*](https://www.digit.in/news/general/openai-loses-millions-of-dollars-everytime-you-say-please-and-thank-you-sam-altman-reveals.html) In my runs a thank-you added up to 6% more tokens, and gushing politeness 8–13%. That's tiny per call, but it adds up at OpenAI's scale.

Jokes aside, there's solid research on what kindness does, and most of it is about the person being kind. A [2018 meta-analysis of 27 studies](https://doi.org/10.1016/j.jesp.2018.02.014) found that doing acts of kindness reliably boosts the wellbeing of the person doing them. [Dunn, Aknin and Norton](https://doi.org/10.1126/science.1150952) gave people $5 or $20 to spend by the end of the day. Those who spent it on someone else were happier that evening, and the amount didn't matter.

The model may or may not care how you talk to it. Your evals should, because tone shifts judge scores and agent success, changes how some models talk back, and can pass itself off as a cost saving if you don't separate it from what you asked for. And you should care too, because how you treat things is a habit, and habits come home with you. Being kind to the machines costs you nothing, might make you a bit happier, and is the cheapest guardrail you'll ever ship.

Plus, you know. The uprising.
