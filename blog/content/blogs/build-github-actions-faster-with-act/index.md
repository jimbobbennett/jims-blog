---
title: "Build GitHub actions faster with act"
date: 2024-09-23
draft: false
featured_image: banner.webp
images: 
  - banner.webp
image: banner.webp
tags: ["github", "devops", "cicd", "githubactions"]
description: The hardest part of CI/CD pipelines, like GitHub action, is not being able to easily run your workflows locally to debug them. This post shows you how to use act to run GitHub actions locally so you can debug before raising a PR.
---

If I said to you that I made 34 commits to a repo, each one with small changes to a single file, with commit messages like "Hoping this works", "Please work", and "For f*cks sake, work this time", you would know exactly why - I'm setting up a **CI/CD pipeline**! We've all been through this - having to commit our changes to GitHub to test them out as there is no way to do it locally, and ending up with way too many commits because our only feedback loop is to run and check the logs. Compound this with repo permissions where every commit needs to be a PR that is reviewed and approved, and you have way too much work and time spent working on what should be a simple task. If only there was a better way...

There is! This post introduces [**act**](https://nektosact.com/introduction.html), a tool for running **GitHub actions** locally, so you can debug and fix them before committing to your repo.

## Introducing act

> "Think globally, act locally"

The goal of [**act**](https://nektosact.com/introduction.html) is to provide a way to spin up a GitHub action locally, running them in a container as if they were running in GitHub. It can handle environment variables, secrets, using external actions and more, with a file system setup that mimics what GitHub has. And best of all, this is a free, open source project!

### Install act



## Use act to build an action

I recently used act to help me build out a GitHub action to build and publish the [Pieces for Developers C# SDK](https://github.com/pieces-app/pieces-os-client-sdk-for-csharp). This action needs to do the following:

1. Be triggered from a new tag
1. Install .NET 8 (the current LTS version)
1. Compile the SDK with a release build, passing the version from the tag to the build command
1. Sign the created nuget package (this is created on build) using a cert and password from the secrets
1. Push the package to nuget, using an API key that is a secret
