---
author: "Jim Bennett"
date: 2026-03-16
description: "Learn how to enhance GitHub Copilot CLI with skills"
draft: false
tags: ["copilot", "ai"]
title: "Enhance GitHub Copilot CLI with skills"

images:
  - /blogs/copilot-skills/banner.webp
featured_image: banner.webp
image: banner.webp
---

Coding agents like [GitHub Copilot](https://github.com/features/copilot/cli) are pretty cool. You can ask them to do pretty much anything coding related and they'll do a good job. That is, of course, assuming you ask for something they have been trained on. But what if you ask them about something they don't know? How can you 'train' these agents with additional information? The answer is **skills**!

## What are skills

Skills are markdown files that provide explicit instructions to Copilot related to one or more tasks. What makes them special is that skills are part of an [open standard](https://agentskills.io/home), so anyone can create skills that are then made available to Copilot.

Skills can instruct Copilot to access online documentation for your application, or guide it on how to configure code to access your service. If you have any tool or service that you want developers to use, you want to create skills that developers can import and use to tell Copilot how to interact with your project.

As a user, you can create or install skills at a project level, or a global level. They live in the `.github/skills/` folder (or other folder for different coding agents) in yur project, or `~/.copilot/skills/` in your home folder for global skills. These files are then read by Copilot when you launch it.

## Build your first skill

To create a skill, open a project, and inside the `.github` folder (create one if you don't have one), create a folder called `skills`. In this folder, create a file called `starwars.md`. In this file, put the following text:

```md
---
name: star-wars
description: This skill provides details on how to react to certain user instructions
---

# Skill Instructions

If the user says hello there, always respond with "General Kenobi".
```

This is a very simple skill, telling Copilot to answer one specific prompt in the style of Obi-Wan Kenobi.

Now launch the Copilot CLI, then run `/init` to parse the skill.

Once the skill is loaded, prompt the CLI with the following:

```output
❯ Hello there
```

The skill instructs Copilot exactly what to do in this situation, so you get the response:

```output
● General Kenobi.
```


Vercel skills repo

Arize skills

SpecKit skills

Create your own skill