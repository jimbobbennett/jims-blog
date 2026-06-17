---
author: "Jim Bennett"
date: 2026-06-29
publishDate: 2026-06-29
description: "Span, trace, session. Three words you'll hear constantly the moment you start tracing an AI app, and they're not interchangeable. Each one is a different zoom level, and you evaluate something different at each."
draft: true
slug: "span-trace-session"
title: "Spans, traces and sessions: the three zoom levels of an AI app"
tags: ["ai", "evals", "llm", "observability"]

images:
  - /blogs/span-trace-session/banner.png
featured_image: banner.png
---

The moment you start tracing an AI app, three words turn up everywhere: span, trace, session. People sling them around as if they're obviously different, and if you're new to this you nod along while quietly wondering whether they're just three names for the same thing.

They're not. They're three zoom levels on the same activity, from a single atomic step all the way out to a whole conversation. And the reason it's worth getting straight is that you evaluate something different at each level. Point an eval at the wrong zoom level and you'll get an answer to a question you didn't mean to ask.

![Infographic: span, trace and session - the three levels you trace and evaluate, from a single atomic operation to a whole multi-turn conversation](/blogs/span-trace-session/banner.png)

*Want it to hand? [Download the infographic as a PDF](/blogs/span-trace-session/infographic.pdf).*

The whole thing runs left to right from *atomic, a single step* to *the whole conversation*. Think of it like zooming out on a map. A span is one building. A trace is the street it's on. A session is the whole neighbourhood. Same place, different altitude, and you ask different questions depending on how high up you are.

## Span

A span is the smallest unit: one atomic operation. One model call. One tool call. One retrieval step. The single thing the app did, on its own, with a start and an end.

When you evaluate at the span level, you're asking a tight, specific question about that one step. Did the retrieval actually pull back relevant documents? Did the tool return the right result for the arguments it was given? Did this one model call produce sensible output? It's the most precise place to look, because there's nowhere for a problem to hide - it's just the one operation, in isolation.

This is where a lot of the most useful debugging happens. When a whole answer comes out wrong, the cause is usually one bad span buried in the middle - a retrieval that grabbed the wrong thing, a tool that quietly failed. Evaluating at the span level is how you find the exact step that let you down.

## Trace

Zoom out one level and you get a trace: all the spans for one user-facing request, strung together. The user asks a question, and the app does a whole sequence of things to answer it - retrieves some context, calls a model, maybe calls a tool, calls the model again - and the trace is that entire path from input to final answer.

Evaluating at the trace level asks the bigger question: did the whole turn actually land? Not "was this one retrieval good", but "given everything the app did, was the final response grounded, correct, and on-task?" This is the level that maps to what the user actually experienced for that one question. Every span in it could look individually fine and the answer could still miss, which is exactly why you need to evaluate the trace as a whole and not just its parts.

## Session

Zoom out once more and you've got a session: a collection of traces making up a whole multi-turn conversation. The full back-and-forth, from the user's first message to the point they leave.

This is the level people forget about, and it's where some of the most important failures live. A single turn can be perfect while the conversation as a whole falls apart. The app contradicts something it said three messages ago. It loses the thread. It technically answers every individual question but never actually helps the person get where they were going. Evaluating at the session level asks the only question that ultimately matters: did the user reach their goal? You're looking at coherence across turns, whether things actually got resolved, and the tell-tale signs of a frustrated human going in circles.

## Pick the right altitude

So when you sit down to evaluate, the first question isn't "what's my eval" - it's "at what level am I asking?"

Checking whether a retrieval step did its job is a span-level question. Checking whether a whole answer was grounded is a trace-level question. Checking whether the user actually got helped is a session-level question. Same app, three different altitudes, three different things worth knowing.

Most teams start and stop at the trace level, because that's the obvious one - it maps to a single question and answer. But the span level is where you debug *why* something broke, and the session level is where you find out whether you're actually helping anyone over the course of a real conversation. Get comfortable moving between all three, and the question of what to evaluate gets a lot clearer. The next thing to sort out is *how* to run those evals once you know what you're asking, which is [a whole spectrum of its own](/blogs/four-ways-to-run-evals).
