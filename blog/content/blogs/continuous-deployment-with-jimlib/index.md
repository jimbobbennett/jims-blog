---
author: "Jim Bennett"
categories: ["Technology", "github", "nuget", "jimlib", "technology", "continuous deployment", "appveyor", "git"]
date: 2014-08-27T03:41:57Z
description: ""
draft: false
slug: "continuous-deployment-with-jimlib"
tags: ["Technology", "github", "nuget", "jimlib", "technology", "continuous deployment", "appveyor", "git"]
title: "Continuous deployment with JimLib"

images:
  - /blogs/continuous-deployment-with-jimlib/banner.png
featured_image: banner.png
---


Today I've finally moved to the world of continuous deployment - albeit for one of my projects only so far, but it's a start.  For my [JimLib](http://github.com/jimbobbennett/JimLib) open source API I've automated the whole deployment process so after checkin it builds and deploys to NuGet automatically.

### Steps in the process

I do all my development in Visual Studio, which now can connect to git.  I have this wired up to [my GitHub repo](http://github.com/jimbobbennett/JimLib) so I can commit changes to my local repo and sync back to GitHub.

Once changes are synced, I use [AppVeyor](http://www.appveyor.com) to do my builds.  They provide a free service for public repositories so can automate all open source builds without you spending a penny.  I have set this up to:

* Pick up pushes to my repo
* Increment a version number and set this in AssemblyInfo.cs
* Build everything
* Run all unit tests
* Package up the NuGet package including symbols
* Push the NuGet packages to [NuGet.org](https://www.nuget.org/packages/JimBobBennett.JimLib/)

AppVeyor even provides markdown for a build status:

[![Build status](https://ci.appveyor.com/api/projects/status/pxisjdt5qxf05utr)](https://ci.appveyor.com/project/jimbobbennett/jimlib)

### How can I be sure I'm deploying the right thing?

This is where unit tests come in.  I try to get as much coverage as possible (91% at the moment), and use this to provide a level of certainty that any new changes work (assuming my tests are good) and that I haven't broken anything with any new changes.  The build process runs the tests and won't push the package unless all tests pass.

### Downsides to AppVeyor

AppVeyor is very good, I'm really impressed with what they offer for free.  It's not fast to get a build, sometimes you can be waiting for up to an hour but for free thsi is fine.  The only downside so far is NuGet package restore.  They always provide a clean environment to build on and even with package restore turned on you have to build twice with they don't do.  It means you have to check your packages into git.  Not the end of the world, but a bit annoying.

