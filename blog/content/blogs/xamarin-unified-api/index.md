---
author: "Jim Bennett"
categories: ["Technology", "xamarin", "xamarin.ios", "technology", "xamarin.forms", "build error", "bug", "unified API", "64-bit"]
date: 2015-01-13T22:37:52Z
description: ""
draft: false
slug: "xamarin-unified-api"
tags: ["Technology", "xamarin", "xamarin.ios", "technology", "xamarin.forms", "build error", "bug", "unified API", "64-bit"]
title: "Xamarin Unified API"

images:
  - /blogs/xamarin-unified-api/banner.png
featured_image: banner.png
---


Recently Apple announced some changes to their requirements for apps submitted to the iOS app store.  From the 1st February all new apps must support 64-bit (for updates to existing apps, it's 1st June).

Xamarin, not wanting to do anything the easy way have decided that as well as supporting this, they will overhaul their API and unify their Mac and iOS APIs.  Based on how poorly they managed the iOS rollout (like not being able to build iOS 8 apps using Visual Studio or on Yosemite until a week after iOS 8 was live), I'm very sceptical about how successful this will be.  Combine this with a major update ot Xamarin.Forms at the same time and this is a recipe for disaster.  Luckily they decided to have an extra weeks testing and it's only just [been released to their stable channel](http://blog.xamarin.com/xamarin.ios-unified-api-with-64-bit-support/), with 3 weeks to go until Apple's deadline.

Tonight I decided to upgrade [JimLib.Xamarin](https://github.com/jimbobbennett/JimLib.Xamarin).  The first thing to note is they have a tool to do the hard work for you.  At least they do in Xamarin Studio for Mac - not in the Windows version or in Visual Studio.
So the first step in the upgrade is to load it all up in Xamarin Studio on my Mac and run the wizard.  So far, so good.  This changes the references to monotouch to point to Xamarin.iOS and updates namespaces.  Unfortunately if you are using Xamarin.Forms or Xamarin.Settings these referencs stay around, even upgrading their nuget packages to the latest version which supports 64-bit.  The easiest thing I found to do was completely remove and re-add these packages.
Xamarin.Forms has a nasty thing though - it adds an error condition to the .csproj file if the nuget package is not there, and it doesn't remove this when removing the nuget package.  The fix is to edit the .csproj file and manually remove the error condition.  Which is nice.

The next thing to do is fix any type issues.  They've changed things like int and float (standard C# types) to use nint and nfloat (weird iOS types), which seems non-intuative.  Int already changes from 32 to 64 bit depending on platform so I fail to see why they need nint.

The next step is to get it to build.  This wasn't too hard, just cleaning up the mess in the csproj files, changing some types etc.

Finally, I'm tring to build it on Visual Studio.  This doesn't work.  I'm getting:

` The name InitializeComponent does not exist in the current context `

This works on Xamarin Studio on the Mac, obviously, not on Visual Studio.

Will update this once I know more about why...

Update:

I've finally got to the bottom of why it was not compiling. To do this I created a new Xamarin.Forms app, added a Xaml file and compared the .csproj files by hand.
It seems somewhere on the way the Generator property on the Xaml file was set to `MSBuild:Compile`.  On the new project, it is set to `MSBuild:UpdateDesignTimeXaml`.  I manually updated the .csproj files and it works.

Nasty!

Update 2:

It seems this was documented in the [release notes in the Xamarin.Forms forum](https://forums.xamarin.com/discussion/29934/xamarin-forms-1-3-0-released/p1), but not in the Unified API migration guide.  Thanks to Robert Stubbs on the forums for pointing this out.  Hopefully Xamarin will improve the docs at some point.

