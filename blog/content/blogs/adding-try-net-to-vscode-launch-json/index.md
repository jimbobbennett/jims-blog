---
author: "Jim Bennett"
categories: ["Technology", "try .net", "dotnet new", "vscode"]
date: 2019-06-11T10:31:32Z
description: ""
draft: false
slug: "adding-try-net-to-vscode-launch-json"
summary: "Learn how to launch Try .NET from VS Code using the debug menu instead of the terminal."
tags: ["Technology", "try .net", "dotnet new", "vscode"]
title: "Adding Try .NET to VSCode launch.json"

images:
  - /blogs/adding-try-net-to-vscode-launch-json/banner.png
featured_image: banner.png
---


I've been playing a lot with [Try .NET](https://github.com/dotnet/try?WT.mc_id=trydotnet-blog-jabenn). I even blogged about it recently - [[jimbobbennett.io/trying-out-try-net](/blogs/trying-out-try-net/)](/blogs/trying-out-try-net/).

One thing that was beginning to annoy me slightly was having to constantly launch the terminal and type `dotnet try` to test out what I was working in. My life would be infinitely improved (not really), if I could run it via **F5** or the debug menu/tab instead of the terminal.

Turns out its pretty easy to do - just add a new entry to your `launch.json` file either directly from the file in the `.vscode` folder, or adding a configuration using the debug menu.

Add this to it:

```json
{
    "name": "Try .NET",
    "type": "coreclr",
    "request": "launch",
    "program": "dotnet",
    "args":"try"
}
```

That's all you need. Now you can run `dotnet try` just by pressing **F5**.

