---
author: "Jim Bennett"
date: 2026-09-14
publishDate: 2026-09-14
draft: false
slug: "ai-sucks"
title: "AI sucks. Deal with it"
description: "AI sucks, and that is exactly the mindset you should keep when you build with it. Stay cynical, test the thing, and stop shipping on vibes."
tags: ["ai", "evaluation", "llms"]

images:
  - /blogs/ai-sucks/stay-cynical-banner.jpg
featured_image: stay-cynical-banner.jpg
---

AI sucks.

I said that on stage at [KCDC](https://KCDC.info) this year, and I meant it. Not because the tech is useless, but because "this is amazing" is the single most dangerous thought you can have while building with it. The demo dazzles you, you get the warm fuzzies, and you ship. Then it meets a real human and falls over.

![Jim Bennett on stage at KCDC delivering the "AI sucks" talk](/blogs/ai-sucks/stage.jpeg)

Let me show you what I mean.

## Exhibit A: healthcare

![Two social posts about medical AI. One: an AI doctor's receptionist in Rotherham struggling because it cannot understand the Yorkshire accent. Another: an AI intake assistant that hallucinates a cough, asking a patient how long they have been experiencing it, and the patient replying "I have no cough and never mentioned a cough"](/blogs/ai-sucks/medical.png)

One team shipped an intake bot that confidently invents a symptom the patient never had. In any other software we would call that a bug and stop the release. In AI we call it a hallucination, shrug, and ship it anyway. In the medical field it is malpractice and could lead to injury or death.

Another shipped a receptionist that does great in testing and then meets an actual Yorkshire accent, which is a problem as it was deployed to a doctor's office in... Yorkshire!

## Exhibit B: the bot that can't understand its own order

![A social post where someone tries to order "blackberry lemonade seltzer" from a customer service chatbot. The bot repeatedly fails to find the product in their order until the customer types out the exact wording, "blackberry lemonade seltzer water". The poster notes this helps no one except the company trying to cut customer service corners](/blogs/ai-sucks/customer-service-bot.png)

The product was right there, the customer knew what they bought. The only thing standing between them and an answer was a bot that needed the magic words typed in exactly the right order. That is not customer service, that is a keyword search wearing a personality.

## Cynicism is a feature

So yes, AI sucks. But that is the right mindset, not a reason to give up. The engineers who build good AI products are the cynical ones. They assume the model is lying until proven otherwise. They assume it will meet an accent it has never heard, a symptom nobody mentioned, an order phrased the wrong way, and they go looking for those failures before their users do.

The opposite of cynical here isn't optimistic. It's careless.

## Deal with sucky AI

A demo that works once is not evidence. It's a vibe. And vibes are how you end up with a receptionist that can't book appointments in part of England, or a pissed off customer who will never buy brand name blackberry lemonade seltzer water from you ever again.

The fix is boring and it works: evaluate the thing. Build a real test set out of the messy inputs your actual users will throw at it, run your model against it, and measure whether it does what you claim. When it hallucinates a cough, you want a failing eval to catch it, not a patient. Keep evaluating in production too, because the real world keeps inventing new ways to embarrass you.

Stay cynical. Test the thing. AI sucks right up until you can prove, with evidence, that yours doesn't.

![AI sucks, stay cynical. Cynical Dude, 1977-Present. A mock motivational poster of Jim Bennett looking thoughtful in the style of an Apple memorial tribute](/blogs/ai-sucks/stay-cynical.jpg)
