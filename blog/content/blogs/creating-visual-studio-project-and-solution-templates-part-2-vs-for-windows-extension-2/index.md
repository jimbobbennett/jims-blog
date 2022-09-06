---
author: "Jim Bennett"
categories: ["technology", "xamarin", "Visual Studio", "extension", "dotnet new", "windows"]
date: 2017-11-06T23:42:10Z
description: ""
draft: false
slug: "creating-visual-studio-project-and-solution-templates-part-2-vs-for-windows-extension-2"
tags: ["technology", "xamarin", "Visual Studio", "extension", "dotnet new", "windows"]
title: "Creating Visual Studio project and solution templates - Part 2, VS for Windows extension"

images:
  - /blogs/creating-visual-studio-project-and-solution-templates-part-2-vs-for-windows-extension-2/banner.png
featured_image: banner.png
---


In the [first part of this set of posts](/blogs/creating-dotnet-new-and-visual-studio-project-and-solution-templates/) I looked at creating a dotnet new project template. These are great if you like the cli, but if, like me, you'd rather be able to do File->New then dotnet new is not much use. Instead you need a Visual Studio extension that provides a new project or solution type to the IDE. The good news is that you can easily take what you've built for your dotnet new templates and create extensions for Visual Studio for both Windows and Mac with not much extra work.

In this post I'll look at VS 2017 for Windows, in the next post I'll cover VS for Mac. Although I'll look is not really correct - instead I'll be lazy and link to someone else's content ;op.

There is an extension for VS for Windows called [Sidewaffle Creator](https://marketplace.visualstudio.com/items?itemName=Sayed-Ibrahim-Hashimi.SidewaffleCreator2017) from [Sayed I. Hashimi](https://twitter.com/sayedihashimi) that provides all the help you need. You load up the project that you generated your NuGet package from into VS, then add a new Template Pack Template project from the SideWaffle extension - this new project is your VSIX.

You can see all this in detail in this YouTube video from Sayed:

{{< youtube g6az_N95dVM >}}

