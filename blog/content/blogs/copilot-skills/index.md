---
author: "Jim Bennett"
date: 2026-03-30
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

## More useful skills

Now it's debatable how useful a Star Wars skill is. Some would say **very**, but others may disagree. Where skills become more powerful is when you add detailed useful instructions related to tools or services.

For example, if you have a SaaS product, and you want coding agents to interact with it, what do you do. You *could* create an MCP server, which is a lot of work, especially if you already have a CLI for your users to use. Instead you could write a skills file that instructs the agent on how to use your CLI tool. You can then release CLI updates along with skill updates, and the coding agents are ready to use it immediately.

## Skill standards

To make skills work, there needs to be standards! The [Agent Skills](https://agentskills.io/home) standard has been created by Anthropic, and is used by pretty much all the agents. This spec defines how you define your own skills, the format for the documentation you provide with each skill, and so on.

Skills can live in a folder, so can be installed for a single project, or at a user level so are available to all projects. For example, you might want a skill to interact with the GitHub CLI available everywhere, so you would install it at the user level. Then when working on an AI app, you would want the [Arize skill](https://github.com/Arize-ai/arize-skills) in the folder for your project so that it doesn't confuse a coding agent working on a non-AI project.

The only non-standard is where skills live. Claude wants skills in the `.claude` folder. GitHub Copilot wants them in the `.copilot` folder, but will also use skills in the `.claude` folder, which makes it easier to migrate from Claude to Copilot.

### Awesome Copilot

The [Awesome Copilot](https://awesome-copilot.github.com) repo contains a mix of skills, agent definitions, plugins (containing multiple skills in one package), and more, that can be installed into any agent.

You can install a plugin for example, using this command:

```bash
copilot plugin install <plugin-name>@awesome-copilot
```

Replacing `<plugin-name>` with the name of the relevant plugin.

### Vercel skills package

Vercel published an [open source tool for managing skills](https://github.com/vercel-labs/skills). This tool makes it easy to install tools from a repo into any project. They have a registry of skills you can reference, or you can install from anywhere.

For example, to install skills from the [Arize skill](https://github.com/Arize-ai/arize-skills), use the following command:

```bash
npx skills add Arize-ai/arize-skills
```

You can then interactively choose which skills, which coding agent, and the scope (user or project).

## Summary

Skills are a really powerful way to expand the capabilities of your coding agent, or to make your product available to your users agents.
