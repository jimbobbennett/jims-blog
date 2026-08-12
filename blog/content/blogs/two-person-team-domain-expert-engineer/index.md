---
author: "Jim Bennett"
date: 2026-08-12
publishDate: 2026-08-12
description: "At RenderATL I had the same conversation twice, from two sides: Mat Biilmann sees domain experts prompting apps into existence, Danny Thompson sees engineers afraid of being replaced. Both describe the same team. The engineer's new job is the connective tissue, and proving it holds."
draft: false
slug: "two-person-team-domain-expert-engineer"
title: "The two-person team: the domain expert prompts, the engineer connects"
tags: ["ai", "coding-agents", "vibe-coding", "engineering-teams", "connectivity", "evals"]
featured_image: cover.png
---

At [RenderATL](https://renderatl.com) I had the same conversation twice, from two different sides.

The first was at the Commit Awards with [Mat Biilmann](https://www.linkedin.com/in/mathias-biilmann-christensen-a5a3805), Netlify's CEO. The second was the next day, in the expo hall, with [Danny Thompson](https://www.linkedin.com/in/dthompsondev), developer advocate and one of the most grounded voices on what AI actually changes about the job.

Mat is watching a new kind of builder show up: the domain expert who no longer needs an engineer to translate their idea into an app. Danny is watching engineers panic that this makes them obsolete. Both of them are right, and the interesting thing is that they're describing the same team from opposite ends.

Here's the team I think is forming.

## The new two-person team

Picture an HR business partner who is tired of the sentiment survey tool her company pays for. She knows exactly what she wants: the questions, the cadence, how the results should roll up. What she's never had is a way to build it without filing a ticket and waiting two quarters for it to climb the engineering backlog.

Now she prompts a coding agent and gets a working app. Mat tells a version of this story about a real HR partner who replaced Culture Amp with her own app, built alongside a single developer, "cutting out the product-manager-to-engineer translation loop entirely." She decides *what* to build. The agent handles most of *how*.

![The two-person team: the domain expert prompts the app into existence on the left, the engineer owns the seam of APIs, auth, and integrations that connects it to real systems on the right](/blogs/two-person-team-domain-expert-engineer/two-person-team.png)

That split is the whole story. Anthropic's Economic Index put it plainly earlier this year: "people decide what to build, and the agent decides how to build it," and the more understanding a person brings to the agent, the better the work that comes back. Non-engineers in that study landed within a few points of professional software engineers on task success. The domain expertise turns out to be the scarce part. The code was never the point.

The temptation is to read this as "agents replace engineers," which is wrong.

This isn't about replacing engineers. It's about the enormous queue of software that domain experts need and can't get, because it sits too far down engineering's backlog to ever ship. The internal tool that would save one team ten hours a week but doesn't clear the bar against revenue work. The one-off app for a single department, all the software that matters to somebody but never matters *enough* to fund, that's the queue that's about to drain. And it drains by empowering the people who feel the pain, not by firing the people who build.

## Where the agent stops

The agent gets you a long way, fast, and then hits a wall. Addy Osmani named this the "70% problem": non-engineers "get 70% of the way there surprisingly quickly, but that final 30% becomes an exercise in diminishing returns." The last stretch, the requirements you didn't know to state, the edge cases, the security, the performance, still needs human judgment.

And notice *where* the wall is. The app itself, the thing the agent generates, is usually the easy part now. The wall is everything the app has to touch. Real authentication, the existing database that already holds the company's data, the internal API that speaks a format nobody documented, the third-party system with a rate limit and a login flow. Mat is blunt about this: agents "excel at generating code," but ["the path from prompt to production is still filled with obstacles,"](https://www.netlify.com/blog/agent-week-2025/) and the hardest of those is working "with existing legacy code bases and data sources."

![The connectivity gap: the agent generates the first 70% fast, then hits a wall at the seam where real auth, the legacy database, the undocumented API, and third-party systems live](/blogs/two-person-team-domain-expert-engineer/connectivity-gap.png)

This is not a cosmetic gap. The Cloud Security Alliance surveyed 5,600 vibe-coded apps and found that zero of them had CSRF protection, security headers, or properly scoped access policies. The demo runs, the wiring to the real world is missing, and when it's there, it's often wrong in ways the person who prompted it can't see.

That gap has a name in a dozen different write-ups: the "70% problem," Vercel's "90% problem," the "last mile." They're all pointing at the same seam: the code generates, the connections don't.

## Connectivity is the job now

So what does the engineer do on the two-person team? They own the seam.

Not the app, the domain expert can conjure the app. The engineer builds the connective tissue: the API that exposes the legacy system cleanly, the auth that actually holds, the integration that lets the shiny new tool read from the warehouse of record. Yoko Li at a16z put it well: "agents can generate a lot of code, but they still need something solid to plug into." The engineer builds the "something solid."

Danny frames the human half of this as well as anyone. His line is that ["the prompt-and-pray era is over — and that's a good thing,"](https://creators.spotify.com/pod/profile/the-programming-podcast/) and that your value now is "caring, context, judgment, and composing solutions." Not typing the app into existence, but composing the systems it depends on, and having the judgment to know where it will break. He talks about the real production work as state orchestration, constraint generation, infrastructure reliability, and regression testing — none of which the agent volunteers, and all of which decide whether the thing survives contact with real users.

That's a promotion, not a demotion. The engineer stops being the translator between a PM's intent and a codebase, the slow, expensive step in the middle, and becomes the person who makes the domain expert's app real. Higher leverage, less busywork, more of the work that was interesting in the first place.

## So how do you trust what got shipped?

There's a harder question hiding under all of this, and it's the one an engineering leader should actually lose sleep over.

When the person building the app can't read the code, "does it work?" stops meaning "does it compile" and starts meaning "does it do the right thing against real systems, safely, every time." Correctness moves up a level. And the place it's most likely to fail silently is exactly the seam the engineer owns: the API call that succeeds with the wrong scope, the integration that returns stale data, the auth path that lets the wrong person through.

Which means the engineer's contribution isn't just building the connectivity. It's proving the connectivity behaves. Tests, evals, observability into what the app actually does in production: these stop being hygiene you get to later and become the deliverable. On a team where one person can ship something they can't fully inspect, the person who *can* inspect it is what keeps it trustworthy. That's not overhead. On this kind of team, it's the point.

## The team didn't shrink. It re-specialized.

Go back to the two conversations at RenderATL. Mat is right that the translation loop is collapsing and a new cohort of builders is showing up. Danny is right that the engineer's value didn't evaporate. It moved.

Put them together and you don't get a smaller team. You get a differently-shaped one: the domain expert who knows what to build and can now prompt it into being, paired with an engineer who gives that creation a nervous system, the connections to real systems, and the proof that those connections hold.

For anyone staffing or leading engineering, that reframes the whole question. The goal was never to protect engineers from agents, or to replace engineers with them. It's to finally ship the mountain of software that real people needed and never got, because it lived forever at the bottom of a backlog. The domain experts can start it now. The engineers are what make it real.
