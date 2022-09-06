---
author: "Jim Bennett"
categories: ["Technology", "open source", "api", "nuget", "jimlib", "technology", "symbols"]
date: 2014-08-15T03:11:18Z
description: ""
draft: false
slug: "symbols-for-nuget-packages"
tags: ["Technology", "open source", "api", "nuget", "jimlib", "technology", "symbols"]
title: "Symbols for NuGet packages"

images:
  - /blogs/symbols-for-nuget-packages/banner.png
featured_image: banner.png
---


Since releaseing [JimLib](https://github.com/jimbobbennett/JimLib) onto [NuGet](https://www.nuget.org/packages/JimBobBennett.JimLib/), I've been dogfooding it as much as possible for my own development.  One area I noticed was lacking was in symbol support - if I wanted to view the inner workings of my classes I had to decompile the source using ReSharper.  Not an ideal situation.

Luckily there is a better way.  [SymbolSource](http://www.symbolsource.org/) is a free service that hosts symbol and source packages for a huge array of NuGet packages and it's integrated into Visual Studio - if a symbol package is available there then with one click you can navigate the source and even step through the code in the debugger.  And if that's not great enough as it is, you can easily create and upload symbol packages right from NuGet with minimal changes.  The docs are [here](http://docs.nuget.org/docs/creating-packages/creating-and-publishing-a-symbol-package) but basically you add the pdb files and source to your .nuspec, then let NuGet do the magic for you - it will create 2 .nupack files when you pack with the `-symbols` flag, one without symbols with the normal name, and one with with an extension of `.symbols.nupkg`.  When publishing there is nothing extra to do - if the `.symbols.nupkg` package is found it will be uploaded to the SymbolSource server at the same time as the main package is uploaded to NuGet.

Check it out - grab the latest [JimLib NuGet package](https://www.nuget.org/packages/JimBobBennett.JimLib/), use it in your app and step into the code.

