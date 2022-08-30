---
title: "Auto-posting to dev.to using a GitHub action"
date: 2022-02-03
draft: false
featured_image: stream-screenshot.png
images: 
  - stream-screenshot.png
tags: ["github", "github-actions", "docker" ,"python", "ci-cd"]
description: Learn how to auto post markdown from GitHub to dev.to
---

![A screenshot from teh live stream mentioned here](stream-screenshot.png)

I've been wanting to build a tool to post markdown automatically to blogging platforms. That way I (or anyone else) can write a blog post in markdown, save it in a [GitHub](https://github.com) repo, and have it automatically posted to a blogging platform of their choice.

I've created a small Python app to do this, and you can find it on GitHub at [github.com/jimbobbennett/auto-blog-poster](https://github.com/jimbobbennett/auto-blog-poster). You add some special folders to any folders containing README.md files, and it will create a blog post from the markdown. It will also track when the README file changes and update the blog post.

It's slightly annoying to have to remember to run this every time you create or update a post, so I wanted to make it so it could be run automatically. GitHub actions are the perfect way to do this.

## What are GitHub actions?

GitHub actions is GitHubs CI/CD solution. CI is continuous integration, meaning every time code changes, your code can be built and tested. CD is continuous deployment, so once code is tested it can be deployed automatically. 

Essentialy you can specify code that is run whenever someone checks in any changes, merges a branch or PR, or raises issues, creates PRs, any task really that you can do in GitHub. GitHub manages spinning up a VM to run everything, all you have to do is write your action, and pay (obviously - the best things in life are not always free).

GitHub actions are deined using YAML inside your repository (in a `.github\workflows` folder), and you can call out to *actions* that do things, such as checking out code, tagging, running scripts, anything you need. You can also build custom actions.

## Custom actions

A custom action is one you write yourself to do whatever you need. In my case, I want my posting code to be run every time I update a markdown file in another repo, and this is something I can do with a custom action.

Custom actions are either written in JavaScript/TypeScript, or run from a Docker container. My app is Python, so I need to use Docker.

### Creating a Docker custom action

Docker custom actions are Docker containers that can be run, and will stop when they are complete - you package up your app in a container, and provide it with an `ENTRYPOINT` so that Docker can run something.

I created a Dockerfile for my auto post tool, along with a shell script as the entrypoint:

```bash
# Create this docker file based off a Python 3.9 Linux image
FROM python:3.9-slim-buster

# Run everything from /app
WORKDIR /app

# Copy over the files
COPY requirements.txt requirements.txt
COPY app.py app.py
COPY dev_to.py dev_to.py
COPY github_access.py github_access.py
COPY entrypoint.sh entrypoint.sh

# Install the Python requirements
RUN pip3 install -r requirements.txt

# Execute the shell script as the entrypoint
ENTRYPOINT /app/entrypoint.sh ${@}
```

This Dockerfile creates a container using a Python base image, copies all my files over, installs my Pip package dependencies, then sets the entrypoint.

The interesting thing to note here is the parameter passed to the `entrypoint.sh` script - `${0}`. My app needs some secrets passed to it - an API key for Dev.to to allow it to post, the repo to post from, and a GitHub token to allow it to update the repo once the post is up. I don't want these embedded in the container as I want to be able to use this action from different repositories (and allow others to use it), so I want these passed when the action is run. The `${0}` syntax means everything that is set as an environment variable when running the container, so this passes all the environment variables to the shell script, where they can be used in the app.

This means running the container like this:

```bash
docker run ghcr.io/jimbobbennett/auto-blog-poster:main 
    --env DEV_TO_API_KEY=xxx
    GITHUB_ACCESS_TOKEN=xxx
    REPO=xxx/yyy
```

Will pass `DEV_TO_API_KEY=xxx GITHUB_ACCESS_TOKEN=xxx REPO=xxx/yyy` to the shell script, and this can be set as a local environment variable in the container.

Once created, I can build this container and publish it to the GitHub container registry from an action inside the repo for my post tool.

This is my action to publish my Docker container:

```yaml
name: Docker Image CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:

  build:

    runs-on: ubuntu-latest

    steps:
      - name: Log in to the Container registry
        uses: docker/login-action@f054a8b539a109f9f41c372932f1ae047eff08c9
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - uses: actions/checkout@v2
      
      - name: Extract metadata (tags, labels) for Docker
        id: meta
        uses: docker/metadata-action@98669ae865ea3cffbcbaa878cf57c20bbf1c6c38
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}

      - name: Build and push Docker image
        uses: docker/build-push-action@ad44023a93711e3deb337508980b4b5e9bcdc5dc
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
```

This action is run on a push or PR on the main branch. It runs on an Ubuntu VM, logs into the GitHub container registry, checks out my code, gets the tag for the package, builds it and pushed it to the registry.

This code has some variables that come from GitHub. Any variable that starts `${{ github.xxx }}` is set automatically by GitHub to a relevant value such as the repo name. `${{ steps.meta.outputs.xxx }}` are set as outputs of certain steps, and `${{ secrets.xxx }}` are secrets you can set on your repo. `${{ secrets.GITHUB_TOKEN }}` is a special secret you don't need to set that provides an API token to interact with the current repo.

Once this container is pushed, I can use it from an action inside my blog repo!

### Using a Docker custom action

To use a Docker custom action, I can just pull it from inside my blog repo action and run it. Here's the action YAML:

```yaml
on: [push]

env:
  REGISTRY: ghcr.io

jobs:

  build:
    runs-on: ubuntu-latest

    steps:
      - name: Log in to the Container registry
        uses: docker/login-action@f054a8b539a109f9f41c372932f1ae047eff08c9
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
    
      - name: Use Docker CLI
        uses: actions-hub/docker/cli@master
        env:
          SKIP_LOGIN: true

      - run: docker pull ghcr.io/jimbobbennett/auto-blog-poster:main

      - run: >
          docker run ghcr.io/jimbobbennett/auto-blog-poster:main 
          --env DEV_TO_API_KEY=${{ secrets.DEV_TO_API_KEY }}
          GITHUB_ACCESS_TOKEN=${{ secrets.GITHUB_TOKEN }}
          REPO=${{ github.repository }}
```

This action uses a docker custom action to log in to the GitHub container registry, pull my container, then run it, passing in an API key for Dev.to, the GitHub token and the current repository.

That's it - now every time the blog post markdown changes in my repo, it is automatically deployed to Dev.to.
At the moment this is just a playground, but the plan is to build out a new blog that uses this - all the posts will be in GitHub, and it will post to another blogging platform and Dev.to at every checkin.

## Learn more

GitHub actions are a lot of fun, and a great way to set up CI/CD. I did a live stream where I worked all this out here:

{{< youtube MSfeKTOO1Tc >}}
<br>
You can also read more on the great [GitHub Actions docs](https://docs.github.com/actions).