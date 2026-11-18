---
author: "Jim Bennett"
date: 2026-11-18T07:00:00-08:00
publishDate: 2026-11-18T07:00:00-08:00
description: "Before LLMs we had small task models like LUIS that handed back a label and a score. Then we used one giant LLM for everything. Now DiffusionGemma, Jev, Clef and Clairic are swinging us back to specialised models, and this time they'll run on hardware you already own."
draft: false
slug: "small-models-are-back"
title: "Small models are back, and they're coming to your devices"
tags: ["ai", "llm", "small-models", "on-device", "system-one", "luis", "diffusion"]

images:
  - /blogs/small-models-are-back/cover.png
featured_image: cover.png
---

I've been playing with a load of the new models that have popped out over the last few months, and they feel really familiar. Some of them give you back exactly the kind of answer LUIS from Microsoft used to: a label and a confidence score. I spent a lot of time with LUIS back when I was a Cloud Developer Advocate at Microsoft, so this is familiar territory. When Jev launched in September I wrote about how [everything old is new again](/blogs/genai-hammer-nail/), and how we'd spent three years using LLMs as a hammer on problems that were never nails. Since then, more of these models have arrived, and the pattern is getting harder to ignore.

For the last few years the answer to almost every AI problem has been "throw it at a large language model (LLM)". Now we're seeing a swing back to smaller models built for one job, and I think the next step is growth in those models running on hardware you already own.

![Timeline of four eras: small task models like LUIS from 2015, LLMs for everything from 2022, specialised models in 2026, and models on your own hardware next](/blogs/small-models-are-back/timeline.png)

Let's take a quick wander through how we got here, and where I think it's going.

## Remember LUIS?

Back in April 2015, Microsoft announced [Project Oxford at Build](https://www.infoq.com/news/2015/05/microsoft-project-oxford/), a set of AI APIs that included the Language Understanding Intelligent Service, or **LUIS**. It hit [public beta in October 2015](https://visualstudiomagazine.com/articles/2015/10/28/language-api-project-oxford-beta.aspx), and for a good few years it was how a lot of us built chatbots.

The idea was simple. You defined *intents* (the things a user might want to do, like book a flight) and *entities* (the bits of data you care about, like a city or a date). You gave it a pile of example sentences for each one, trained a model, and then sent it whatever your users typed. It sent back something like this:

```json
{
  "query": "fly me to Seattle on Friday",
  "topScoringIntent": { "intent": "BookFlight", "score": 0.97 },
  "entities": [
    { "entity": "seattle", "type": "City" },
    { "entity": "friday", "type": "Date" }
  ]
}
```

No prose, no chat. Just a typed answer with a score, so your code could decide what to do next. If the score was low, you'd ask the user to rephrase.

It worked, but it was a lot of effort to get working. Every app needed its own model, you had to come up with all those example sentences yourself, and anything your users said that you hadn't thought of fell flat on its face. LUIS, and tools like it, were small models that each did one narrow thing, and you needed a lot of them.

## Then one type of model ate everything

On 30 November 2022, ChatGPT launched, and [it hit around 100 million monthly users in two months](https://www.techspot.com/news/97486-chatgpt-adds-100-million-users-two-months-making.html). For comparison, TikTok took about nine months to get there.

Overnight, the approach changed. Why train a separate intent model when you could write "classify this message as one of these options and return JSON" in a prompt? Classification, extraction, routing, summarising, writing replies: all of it went to the same giant model. It was a massive step forward, LLMs understood the weird stuff users typed far better than anything we'd trained by hand.

But LLMs came with costs. You were paying a big model to generate text, and then writing code to parse that text back into the structured answer you wanted in the first place. Responses took seconds instead of milliseconds. Ask the same question twice and you might get two different answers. (Anyone who's had a model wrap its "JSON only" output in a friendly paragraph knows the pain.)

LUIS didn't make it. Microsoft stopped new LUIS resources in 2023 and [fully retired it on 31 March 2026](https://learn.microsoft.com/en-us/answers/questions/1031241/retirement-announcement-language-understanding-lui), pointing everyone at its replacement, conversational language understanding (CLU). An end to the first era of understanding models.

## 2026: the year models started specialising again

This year, something different started happening. Instead of every new release being "the same kind of model, but bigger", we started getting models that are a different *shape*. I want to look at three of them.

### DiffusionGemma changes how text gets made

Every LLM you've used writes text the same way: one token (roughly a word or part of a word) at a time, each one depending on the ones before. In June, Google DeepMind released [DiffusionGemma](https://deepmind.google/models/gemma/diffusiongemma/), which does it differently.

![Comparison: a standard LLM writes one token at a time left to right, while DiffusionGemma starts with a noisy block of tokens and refines the whole block in parallel](/blogs/small-models-are-back/diffusion.png)

*Diffusion* is the technique behind most image generators. You start with noise and refine it, step by step, until a picture appears. DiffusionGemma does this with text. It generates text by iteratively denoising blocks of tokens (a 'canvas') in parallel, working on 256 tokens at once, keeping the tokens it's most sure about, and then has another go at the rest.

The result is speed. Google says it's up to 4x faster than a standard model, with over 1,000 tokens per second on an H100 GPU and over 700 on a gaming-grade RTX 5090. It's an open-weights model under the Apache 2.0 licence, and it runs in about 18GB of memory when quantised (squashed down to use less precise numbers). It's 25.2 billion parameters in total, but only 3.8 billion are active for any given token.

It's not as smart as its sibling, though. On the MMLU Pro benchmark it scores 77.6 against 82.6 for the standard Gemma 4 model it's based on. The bit I find really interesting is where Google says it shines. [Google's developer guide](https://www.plushcap.com/content/google-cloud/blog/google-cloud-diffusiongemma-the-developer-guide) says the standard approach may stay more efficient for high-volume serving in the cloud. The speed win is for one user on one GPU. In other words, it's a model built to run locally.

### System One models change what comes back

In September, a startup called TypeSafe AI came out of stealth with a model called **Jev** and a new category it calls *System One*. The name comes from Daniel Kahneman's *Thinking, Fast and Slow*, where System 1 is your quick, instinctive thinking and System 2 is the slow, careful kind.

A System One model is an AI model that answers typed questions about an input with probabilities instead of generated text. You ask it a yes/no question, a multiple choice question, or ask it to score something against a rubric, and you get back an answer with a calibrated probability. If it says 0.9, it should be right about 90% of the time. Unlike an LLM, it doesn't write any explanations in the output.

So far, these models come in two flavours: ones that make decisions, and ones that pull data out.

#### Decisions: Jev and Clef

Decision models have LUIS's output, a label and a score, but with LLM-level understanding of language and no training a model for every app. [Jev answers in 70 to 500 milliseconds](https://www.vktr.com/ai-platforms/chatgpt-cocreator-launches-typesafe-ai-with-jev/), and charges $0.042 per million input tokens, with output free.

![Side by side: a LUIS response with an intent, score and entities next to an illustrative System One answer, with intent mapped to decision and entities mapped to extraction](/blogs/small-models-are-back/spot-the-difference.png)

Cloudflare has jumped in too. On 1 October it released [Clef](https://letsdatascience.com/news/cloudflare-releases-open-weight-clef-decision-models-c52886d6), an open-weights decision model in two sizes, 27 billion parameters and a 9 billion parameter Clef-flash, both under Apache 2.0. Like Jev, you give it a situation and a set of questions with fixed answers, and it picks one for each, with a probability.

#### Extraction: Clairic

On 19 October Cloudflare previewed [Clairic](https://www.unite.ai/cloudflare-releases-clairic-its-first-system-one-extraction-model/), which it calls the first System One *extraction* model. You give it messy input like an email or a photo of a form, plus a list of the typed fields you want (numbers, dates, durations, text spans), and it fills them all in, each with a confidence score, usually in under a second.

### The LLM becomes one step in a pipeline

The part that convinced me these new models are a real shift, and not just a few interesting launches, is how Cloudflare puts these together. Clairic extracts the data, Clef makes the decision, and then an LLM writes the reply. The LLM goes from being the whole app to being one step at the end. LUIS had intents and entities. Clef does the intents, Clairic does the entities. Things really do come back around.

![Comparison: one LLM handling an insurance claim end to end versus a pipeline of Clairic extracting, Clef deciding and an LLM writing the reply, with Cloudflare's own time and cost figures](/blogs/small-models-are-back/pipeline.png)

[In Cloudflare's own test](https://ppc.land/cloudflares-clairic-model-cuts-ai-pipeline-cost-49-in-its-own-test/) on processing insurance claims, that pipeline took 19.3 seconds against 61.7 seconds for an LLM doing everything, and cost $6,032 per million claims instead of $11,740. That's 49% cheaper and about 3x faster. The extraction was also consistent. Clairic's repair estimate was identical each time, while GLM-5.3's changed on every run.

Now, a big caveat. These are all numbers from the companies selling the models, and nobody has independently benchmarked them yet. Cloudflare is pretty upfront about the limits too: *"The architecture makes every answer well formed, not necessarily correct."* A confident wrong answer is still wrong, so you still need to test these things on your own data. But the direction is clear.

## Where this goes next: your own hardware

Here's my prediction. The next few years are about smaller, specialised models running on the device in front of you, and the cloud becoming the overflow.

I've written before about [when small models beat frontier ones on custom tasks](/blogs/slms-for-custom-tasks/), like the finetuned 0.8 billion parameter model at Shopify that outscored the frontier model that trained it. Small models winning on narrow jobs isn't new. What's new is where they'll run.

Two things make me think so. The first is that the models are finally small enough. Gartner has already [predicted that by 2027 organisations will use small, task-specific models three times more than general-purpose LLMs](https://www.gartner.com/en/newsroom/press-releases/2025-04-09-gartner-predicts-by-2027-organizations-will-use-small-task-specific-ai-models-three-times-more-than-general-purpose-large-language-models). A 9 billion parameter decision model, or a diffusion model with 3.8 billion active parameters, is the kind of thing a decent laptop can run.

The second is that a growing percentage of the devices out there have powerful AI hardware in them. Gartner [forecast AI PCs](https://www.gartner.com/en/newsroom/press-releases/2025-08-28-gartner-says-artificial-intelligence-pcs-will-represent-31-percent-of-worldwide-pc-market-by-the-end-of-2025), meaning PCs with a neural processing unit (NPU) built for AI work, at 31% of PCs shipped in 2025 and around 55% in 2026, and Canalys expects that to reach 70% by 2028. Copilot+ PCs need an NPU that can do at least 40 trillion operations per second, and ship with [Phi Silica](https://learn.microsoft.com/en-us/Windows/ai/apis/phi-silica-transparency-note), a small language model that runs on the device. Every recent Mac has Apple Silicon, and Apple's [Foundation Models framework](https://www.macrumors.com/2025/06/09/foundation-models-framework/) gives developers an on-device model of about 3 billion parameters, free to call and working offline. Add in all the gaming GPUs out there and that's a lot of AI compute sitting on desks, mostly doing nothing.

That's not because PC sales are booming. [PC shipments actually fell about 20% in the third quarter of 2026](https://www.windowslatest.com/2026/10/11/ai-was-supposed-to-sell-pcs-instead-pc-shipments-just-crashed-20-as-ai-eats-the-worlds-ram-and-windows-11s-copilot-agents-arent-convincing-buyers/), because AI data centres are buying up so much memory that it's pushed prices through the roof. But a growing share of the machines that do ship have AI hardware built in, and the ones bought over the last couple of years already do. If anything, expensive hardware is one more reason to make better use of what you've already paid for.

![Local first routing: requests go to your own device first, then spare capacity on your company's machines, and only overflow to the cloud](/blogs/small-models-are-back/local-first.png)

One product I've been playing with that leans right into this is [Cloudless AI](https://gocloudless.ai), and I'm pretty excited about it. You install an agent on your company's desktops and laptops, and it routes LLM requests to whichever machine has spare GPU or NPU capacity, only falling back to a cloud model when the fleet is busy or your policy allows it. Your app just points at a different URL. It's a really nice idea: your desktops and laptops become the cluster, and sensitive data stays on your own machines.

So here's what I expect to see:

- **Pipelines of small models.** Extraction, classification, and routing get handled by specialised models like Clef and Clairic, with an LLM saved for the bits that really need writing or reasoning.
- **Local first, cloud second.** Apps try the device first and only go to the cloud when they need a bigger model. Your laptop's NPU stops being a spec sheet bullet point and starts doing real work.
- **More models built for the device.** DiffusionGemma is designed around a single user on a single GPU. I think we'll see a lot more models tuned for that from the start, instead of squeezed down afterwards.

The circle is now complete. We went from lots of small task models to one giant model for everything, and now we're swinging back to specialised models. The difference this time is that they understand language properly, and they'll run on hardware you already own.
