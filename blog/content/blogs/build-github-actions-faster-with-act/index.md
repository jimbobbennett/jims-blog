---
title: "Build GitHub Actions faster with act"
date: 2024-09-23
draft: false
featured_image: banner.webp
images: 
  - banner.webp
image: banner.webp
tags: ["github", "devops", "cicd", "githubactions"]
description: The hardest part of CI/CD pipelines, like GitHub Action, is not being able to easily run your workflows locally to debug them. This post shows you how to use act to run GitHub Actions locally so you can debug before raising a PR.
---

If I said to you that I made 34 commits to a repo, each one with small changes to a single file, with commit messages like "Hoping this works", "Please work", and "For f*cks sake, work this time", you would know exactly why - I'm setting up a **CI/CD pipeline**!

We've all been through this - having to commit our changes to GitHub to test them out as there is no way to do it locally, and ending up with way too many commits because our only feedback loop is to run and check the logs. Compound this with repo permissions where every commit needs to be a PR that is reviewed and approved, and you have way too much work and time spent working on what should be a simple task. If only there was a better way...

There is! This post is all about [**act**](https://nektosact.com/introduction.html), a tool for running **GitHub Actions** locally, so you can debug and fix them before committing to your repo. It shows act off using the real world example of the GitHub Action I created for the [Pieces for Developers C# SDK](https://github.com/pieces-app/pieces-os-client-sdk-for-csharp).

## What is act

> "Think globally, `act` locally"

The goal of [**act**](https://nektosact.com/introduction.html) is to provide a way to spin up a GitHub Action locally, running them in a container as if they were running in GitHub. It can handle environment variables, secrets, using external actions and more, with a file system setup that mimics what GitHub has. And best of all, this is a free, open source project!

### Install act

Installation of act is pretty simple. It uses [Docker](https://www.docker.com), so you need that installed (or a compatible container engine), then after that you can install from your package manager of choice. All the options are listed in [the act installation guide](https://nektosact.com/installation/index.html). I'm a mac user, so used [homebrew](https://formulae.brew.sh/formula/act#default):

```bash
brew install act
```

### Run act

You can run act from the command line. When run, it will run all the jobs in your `.github/workflows` folder.

```bash
act
```

The first time you run act, it will give you a choice of what type of container you want to run everything in - from huge with everything, to tiny with minimal support for external actions. I chose the middle ground, with a 500MB download (which conveniently enough I was able to do on airplane WiFi).

You can configure which jobs are run by passing [events](https://nektosact.com/usage/index.html#events) to the command line. This allows you to simulate a pull request, or a push to a branch. For example, to only run actions triggered by a push, run:

```bash
act push
```

## Use act to build an action

I recently used act to help me build out a GitHub Action to build and publish the [Pieces for Developers C# SDK](https://github.com/pieces-app/pieces-os-client-sdk-for-csharp) to nuget. This action needs to do the following:

1. Be triggered from a new tag
1. Install .NET 8 (the current LTS version)
1. Compile the SDK with a release build, passing the version from the tag to the build command
1. Sign the created nuget package (this is created on build) using a cert and password from the secrets
1. Push the package to nuget, using an API key that is a secret

### Use external actions with act

Act has full support for external actions made available with a `uses` statement. It will clone the action locally, then run it with docker so that it runs as if it was in a GitHub Action. In my case, this means I can check out my code, and install .NET using the default GitHub `actions/setup-dotnet` action.

```yaml
name: Release

on:
  push:
    tags:
      - '*'

jobs:
  publish-to-nuget:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - name: Setup .NET
      uses: actions/setup-dotnet@v4
      with:
        dotnet-version: 8.0.*
```

> Top tip - running an action that installs a large tool like .NET on airplane WiFi is not recommended! Ask me how I know...

### Use a tag with act

The next step is to build the nuget package. As part of this, I want to set the version from the tag.

```yaml
- name: Build
  working-directory: ./src/Client
  run: dotnet build -c Release -p:Version=${GITHUB_REF#refs/tags/v}
```

GitHub automatically passes this tag through to the action as a [default environment variable](https://docs.github.com/actions/writing-workflows/choosing-what-your-workflow-does/store-information-in-variables#default-environment-variables) when run inside GitHub Actions. With act, I can also set environment variables either by passing them into the command line, or adding them to a .env file:

```ini
GITHUB_REF=refs/tags/v0.0.7-beta
```

This allows me to set the tag used for each run, in this example to `refs/tags/v0.0.7-beta`. The syntax of my build command, `${GITHUB_REF#refs/tags/v}` strips the `refs/tags/v` section, so my build sets the version to `0.0.7-beta`.

### Use secrets with act

GitHub Actions supports [secrets](https://docs.github.com/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions) - special values you can configure as the owner of the repo that are surfaced to your actions, but not visible to anyone looking at the repo. These are great for things like API keys or passwords. In my case I need 3 secrets - a certificate to sign my nuget package, a password for the certificate, and an API key for nuget to show it's me uploading the package.

```yaml
- name: Get the nuget signing certificate
  id: cert_file
  uses: timheuer/base64-to-file@v1.2
  with:
    fileName: 'certfile.pfx'
    encodedString: ${{ secrets.NUGET_CERTIFICATE }}
- name: Sign the nuget package
  working-directory: ./src/Client
  run: |
    dotnet nuget sign ./bin/Release/Pieces.OS.Client.${GITHUB_REF#refs/tags/v}.nupkg 
      --certificate-path /tmp/certfile.pfx
      --certificate-password ${{ secrets.NUGET_CERTIFICATE_PASSWORD }}
      --timestamper http://timestamp.digicert.com
- name: Push to NuGet
  working-directory: ./src/Client
  run: |
    dotnet nuget push ./bin/Release/*.nupkg -k ${{ secrets.NUGET_API_KEY }}
    -s https://nuget.org
```

With act, you can [pass secrets using a `.secrets` file](https://nektosact.com/usage/index.html#secrets). This is similar to the `.env` file, just with your secrets in it. I created a local `.secrets` file with the secrets I needed.

For the signing certificate, I need a `.pfx` file, so my way to do this is to encode the contents of the file in base64, upload that as a secret, then use the `timheuer/base64-to-file@v1.2` action to convert that secret to a file on the local file system. More details in [this blog post from Tim](https://www.timheuer.com/blog/use-nuget-with-github-actions-github-packages/).

```ini
NUGET_API_KEY=<key>
NUGET_CERTIFICATE_PASSWORD=<password>
NUGET_CERTIFICATE=<base64 encoded cert>
```

> Always add the `.secrets` to your `.gitignore` to avoid accidentally exposing them by adding this file to your repo!

## Test it out

With my environment variables and secrets all set up, I was able to test out my action. As always, things failed with each run, but I was able to iterate locally without needing to push my action, raise a PR, get it reviewed and approved, merge it, then tag each time.

The kind of errors I hit were:

- Not setting the working directory
- Setting the version of the build wrong
- Getting the path of the certificate file wrong
- Inconsistent case of `release` and `Release` for the output folder

All these are easy mistakes to make when you can't run locally, and would normally take multiple fixes. All fixed locally before I committed my code.

The action ran as if I was inside a GitHub Action - not only did it actually check out my code and build it, it also signed the nuget package and pushed it to the nuget repo. I could see the result with the new package visible inside nuget. This gave me the confidence to raise my PR.

## Conclusion

If you are using GitHub Actions, act is an invaluable tool to help you develop your actions and test them locally. Check it out at [github.com/nektos/act](https://github.com/nektos/act).
