---
author: "Jim Bennett"
categories: ["Technology", "xamarin", "add-in", "mvvmcross"]
date: 2016-11-28T23:42:58Z
description: ""
draft: false
slug: "missing-xamarin-studio-add-ins"
tags: ["Technology", "xamarin", "add-in", "mvvmcross"]
title: "Missing Xamarin Studio add-ins"

images:
  - /blogs/missing-xamarin-studio-add-ins/banner.png
featured_image: banner.png
---


In the latest Stable Xamarin Studio (6.1.2) there is a problem with add-ins - the add-in gallery is empty - the add-in endpoint for 6.1.2 is not returning any add-ins.

![Missing add-ins](Screen-Shot-2016-11-29-at-12.33.02-PM.png)

This means if you are planning on using my [Xamarin Studio MvvmCross add-in](/blogs/mvvmcross-add-ins-for-visual-studio-and-xamarin-studio/) then you won't be able to find it.

Luckily there are a number of workarounds:

* Use the Alpha channel - on 6.2 all the add-ins reappear.

* Add the add-in repository from the previous version by opening the 'Add-in manager', going to the 'Gallery' tab, selecting 'Manage Repositories' from the 'Repository' drop-down, tapping 'Add' and entering this url - http://addins.monodevelop.com/Stable/Mac/6.1.2/main.mrep
![](Screen-Shot-2016-11-29-at-12.37.15-PM.png)

* Install the add-in manually by downloading from [here](http://addins.monodevelop.com/Stable/Mac/6.0/MVVMCross.XSAddIn.MVVMCross.XSAddIn-1.1.8.mpack) and installing it using the 'Install from file...' option in the 'Add-in manager'.

This issue has been raised with Xamarin, so hopefully should be fixed soon.

