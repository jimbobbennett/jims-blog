---
author: "Jim Bennett"
categories: ["xamarin", "Visual Studio", "Mac", "Technology"]
date: 2017-05-23T23:28:34Z
description: ""
draft: false
slug: "opening-multiple-solutions-in-visual-studio-for-mac"
tags: ["xamarin", "Visual Studio", "Mac", "Technology"]
title: "Opening multiple solutions in Visual Studio for Mac"

images:
  - /blogs/opening-multiple-solutions-in-visual-studio-for-mac/banner.png
featured_image: banner.png
---


One area Macs are very different to Windows PCs is in the way documents are opened. Mac apps manage documents internally instead of being able to tap a start button again and open a second instance of your app to load a new document.

This means that on Windows Xamarin developers can open multiple instances of Visual Studio at the same time, allowing them to have multiple solutions open. On the Mac this ability has been missing - you click VS again and it just focuses on the same instance that's already running. There have been a number of workarounds for Xamarin Studio and Visual Studio the apps you can run that will launch another instance, but actually - you don't need to!

Unlike VS on Windows, VS on Mac (and Xamarin Studio for those who haven't updated) can open multiple solutions at the same time in the same window. The option to do so is a bit hidden, but it's there.

What you do is:

* Open your first solution
* Select 'File->Open'
* Select your solution in the Open dialog (just a single click, don't double click to open it)
* Click the 'Options' button
* Uncheck 'Close current workspace'

<div class="image-div" style="max-width: 500px;"> 
    
![Uncheck 'Close current workspace'](Screen-Shot-2017-05-24-at-11.29.14-AM.png)
    
</div>

* Now click 'Open'

Viola! Multiple solutions in the same solution pad.

<div class="image-div" style="max-width: 300px;"> 
    
![Multiple solutions in the same solution pad](Screen-Shot-2017-05-24-at-11.29.46-AM.png)
    
</div>

If the solution is in your recent list you can also open it in the same workspace by holding down the Control key whilst clicking on the solution. Thanks to [Lluis Sanchez Gual](https://twitter.com/slluis) for this one.


<blockquote class="twitter-tweet" data-lang="en"><p lang="en" dir="ltr"><a href="https://twitter.com/CodeMillMatt">@CodeMillMatt</a> A little trick: to quickly open a solution without closing the current one, hold Control while clicking on a file in Recent Solutions</p>&mdash; Lluis Sanchez Gual (@slluis) <a href="https://twitter.com/slluis/status/867662561663234048">May 25, 2017</a></blockquote> <script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>

