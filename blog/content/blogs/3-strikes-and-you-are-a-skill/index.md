---
author: "Jim Bennett"
date: 2026-05-06
description: ""
draft: false
slug: "3-strikes-and-you-are-a-skill"
title: "3 strikes and you're an AI skill"

images:
  - /blogs/3-strikes-and-you-are-a-skill/banner.png
featured_image: banner.png
---

Back in the day when we wrote actual code instead of poking at an AI, I had a general rule for when to refactor repeated code. Do it once, fine. Do it a second time, fine. Do it a third time - refactor.

It's ok to have blocks of identical code in two places, but once I added it to a third place, I'd refactor it to a shared location, such as base class or helper function. Some might say this doesn't follow DRY principles as I should refactor it the second time, but I find it a good balance between pragmatism and clean code. It's too easy to stress over clean code and over complete everything to avoid code duplication, ending up making your code harder to understand.

So how does this apply to AI? I'm going to ignore code duplication here, cos the AI is very good at duplicating code. Instead let's consider how we prompt the AI to do certain tasks.

A typical example is I often ask Copilot or Claude to check its work. I use a prompt like:

```text
Review your work. Check for:

- compliance with the original spec for this work
- unit test coverage
- consistency with the rest of the code base including style, naming, commenting, and architecture
- code reuse, and compliance with DRY principles
- does the code pass the linter
- does the code work

Do multiple passes over all the code changes made using this review plan. When you identify areas that do not pass this review, fix them, then re-run the review.

Work until this review passes.
```

The goal of this is to ensure that Copilot (or Claude, or your coding assistant of choice) takes time to review the changes it has made to ensure they are appropriate, they work, and they confirm to any standards you have for your code. The 'multiple passes' request is to get the agent to review, fix, then re-review. This usually ends up with better quality code after the agent has finished.

My 3 strikes rule not only applies to code, but to prompts as well. The first time I asked my agent to review code, I used a prompt like this. Same with the second time. Once I realized there was a patter here in how I want the coding agent to behave, it was time to create a skill.

## What are skills?

Skills are instructions that are written in plain text or markdown, that provide reusable directions to your agent. You can think of this as analogous to components or packages you use with code. Instead of installing a package from nuget, PyPi, or npm, you add a markdown file that your agent reads.

These skills can be project level, so installed in the same folder as your project, or at a user level so they apply to any session with your coding agent. For example, if you use GitHub Copilot, you can put skills into `~/.copilot/skills` to be used in any coding agent session, or in the `.github/skills` folder in your project to use them just for a single project.

Skills consist of a directory with the name of the skill, containing a file called skill.md, along with additional files or folders that contain more reference information for the skill. The skill.md file contains front matter with the name and description of the skill. This is used by the coding agent to determine when it should use this skill. The rest of this file contains the instructions for the skill, including an example of the kind of prompt a user would use that should trigger this skill.

## Building a code review skill

How do you build a skill? Well the easiest way is to use your coding agent to convert the prompt into a skill. These agents understand skills, so are great at creating them. I asked copilot:

```text
I want to create a user level skill that reviews my code. A typical prompt I use to review code is:

Review your work. Check for:

- compliance with the original spec for this work
- unit test coverage
- consistency with the rest of the code base including style, naming, commenting, and achitecture
- code reuse, and compliance with DRY principles
- does the code pass the linter
- does the code work

Do multiple passes over all the code changes made using this review plan. When you identify areas that do not pass this review, fix them, then re-run the review.

Work until this review passes.

Convert this to a user level skill
```

This was enough for Copilot to create me a skill in my home folder, with the following content:

```markdown
---
name: review-work
description: Review code changes against a multi-criteria checklist (spec compliance, test coverage, consistency, DRY, linter, runtime correctness), fix issues found, and re-run the review until it passes. Use when the user asks to "review your work", "review the code", "do a review pass", or similar.
---

# Review Work

Review the code changes you have made in this session against the checklist below. Make multiple passes. When a pass surfaces issues, fix them, then run the review again. Repeat until a full pass produces no findings.

## Review checklist

For every pass, evaluate the changes against each of these criteria:

1. **Spec compliance** — Do the changes implement what was originally asked? Re-read the original request/spec and verify every requirement is met. Flag missing pieces, scope creep, or anything that drifted from intent.
2. **Unit test coverage** — Are the new/changed code paths covered by unit tests? Are edge cases tested? Are the tests meaningful (asserting behavior, not just running code)?
3. **Consistency with the codebase** — Match the surrounding code's style, naming conventions, commenting patterns, and architectural choices. Don't introduce a new pattern when an existing one fits.
4. **Code reuse / DRY** — Is anything duplicated that should be extracted? Is there an existing helper, utility, or abstraction this code should use instead of reimplementing?
5. **Linter** — Run the project's linter(s). The code must pass with no new warnings or errors.
6. **Does the code work** — Run the tests. Run the build. Where applicable, exercise the feature (CLI invocation, dev server, etc.) to confirm runtime behavior matches the spec. Type-checking and tests passing is necessary but not sufficient — verify the feature actually does what it should.

## Process

1. Identify the scope of changes to review (the work done in this session, or the diff against the base branch — whichever matches the user's request).
2. Run a full pass over all changed code, evaluating against every checklist item. Collect findings.
3. If findings exist, fix them. Don't batch — fix and move on.
4. Re-run the full review. Continue until a complete pass produces zero findings.
5. Report the final result: confirm each checklist item passes, and summarize what was fixed during the review (if anything).

## Notes

- Don't stop after one pass. The first round of fixes can introduce new issues; the loop is the point.
- Run linters and tests with the project's actual commands (check `package.json` scripts, `Makefile`, `pyproject.toml`, etc.). Don't assume `npm test` works if the project uses something else.
- If a check is genuinely not applicable (e.g., a docs-only change has no linter target), say so explicitly rather than skipping silently.
- If you cannot verify runtime behavior (no way to exercise the feature in this environment), say so explicitly — don't claim "it works" based on tests alone.
What's great here is the expansion of the prompt to more detailed instructions. The front matter contains a description of the skill, along with guidance as to what prompt should trigger this. It then has the basics list I provided but expanded with more detailed instructions. "compliance with the original spec for this work" becomes "Spec compliance — Do the changes implement what was originally asked? Re-read the original request/spec and verify every requirement is met. Flag missing pieces, scope creep, or anything that drifted from intent."

It also adds helpful notes, like don't run checks that are not applicable, such as run multiple passes as one pass might introduce new issues, or avoid linter checks for a pure docs change.
```

## Use the skill

Now I have my skill, I can reload my coding agent and it will pick up this new skill. Instead of typing my review prompt in detail each time I need a review, I can just ask `Review your work`, and the coding agent will load this skill and follow it for a thorough review.

I can also iterate on this skill. If there is something I've missed, such as adding rules on running unit tests, or pointing it to a coding style standard, I can update the skill and these changes will be picked up every time I ask the agent to review its work.

## Summary

Skills are a great way to build repeatable processes into how you interact with a coding agent. If you do a task more than once with your agent, consider building it into a skill, a task that is pretty easy to do by asking your coding agent to create the skill for you.

You can get the code for my skill here: [github.com/jimbobbennett/ai-skills](https://github.com/jimbobbennett/ai-skills)
