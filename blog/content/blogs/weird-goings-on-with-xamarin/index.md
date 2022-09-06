---
author: "Jim Bennett"
categories: ["Technology", "xamarin", "xamarin.ios", "technology", "crash", "mono", "sigsegv", "storekit", "skproductsrequest", "json", "newtonsoft", "build error"]
date: 2014-09-06T07:40:58Z
description: ""
draft: false
slug: "weird-goings-on-with-xamarin"
tags: ["Technology", "xamarin", "xamarin.ios", "technology", "crash", "mono", "sigsegv", "storekit", "skproductsrequest", "json", "newtonsoft", "build error"]
title: "Weird goings on with Xamarin"

images:
  - /blogs/weird-goings-on-with-xamarin/banner.png
featured_image: banner.png
---


Yesterday and today I had some weird things happening with Xamarin, so I thought it was work documenting them in case anyone else has the same issue.

### First - Build errors.

I upgraded to the latest Xamarin and suddenly building for an iPhone using Visual Studio was failing with an odd error:

`Failed to resolve "System.Reflection.Emit.ModuleBuilder" reference from "mscorlib, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089"    C:\Program Files(x86)\MSBuild\Xamarin\iOS\Xamarin.iOS.Common.targets`

It works on the simulator and from Xamarin Studio on the Mac, but not from Visual Studio.  Not a good thing realy seeing as I paid a few hundred dollars extra for my license to enable me to develop in VS.

Luckily someone else had also seen this and a workaround is available.  The bug is reported in the [Xamarin BugZilla](https://bugzilla.xamarin.com/show_bug.cgi?id=22636), so check this to see if it's been fixed.
The problem was caused by NewtonSoft.Json.  Their .Net 4.5 portable library isn't that portable it seems, so shows this error.  I've [raised it with NewtonSoft](https://github.com/JamesNK/Newtonsoft.Json/issues/366) so hopefull yit'll be fixed.  The weird thing here is it only fails when building for the device from VS, not from Xamarin Studio on OXS (I haven't tried Xamarin Studio on Windows yet).
The [workaround](https://bugzilla.xamarin.com/show_bug.cgi?id=22636#c11) on Windows is to repoint the dll reference from the `portable-net45+wp80+win8+wpa81` version to the `portable-net40+sl4+wp7+win8`.  Unfortunatley, this breaks the build on Xamarin Studio on OSX, so to build there you have to put it back.
Repointing the reference involves a change to the .csproj file:

```
<Reference Include="Newtonsoft.Json">
  <HintPath>..\..\packages\Newtonsoft.Json.6.0.4\lib\portable-net45+wp80+win8+wpa81\Newtonsoft.Json.dll</HintPath>
</Reference>
```

becomes:

```
<Reference Include="Newtonsoft.Json">
  <HintPath>..\..\packages\Newtonsoft.Json.6.0.4\lib\portable-net40+sl4+wp7+win8\Newtonsoft.Json.dll</HintPath>
</Reference>
```

### Second - Weird crashes with StoreKit

This one had me scratching my head for a while.  I was using StoreKit for in app purchasing, and when I was loading the list of available products it would crash.  Most of the time.  No proper error, no debugger breaking, just a crash with a mono SIGSEGV error.  When I debugged it it wouldn't always crash and sometimes it would just work.  It was the kind of weird thing that I would normally contribute to a race condition but there wasn't any threading issues that I could see.
In my frustration after a couple of hours I did what I should have done at the start - search StackOverflow.  One quick search and I [had my answer](http://stackoverflow.com/questions/3324596/storekit-skproductsrequest-crash).  When making a request, the request has to stay alive long enough for the callbacks.  If you declare it as a local variable like I was doing it can be GC'd before the callbacks.  The non deterministic nature of the GC was why it didn't always happen.

My code was:

```cs
public void LoadAvailableProducts(params string[] productIdentifiers)
{
    var productKeys = new NSSet(productIdentifiers);
    var request = new SKProductsRequest(productKeys);

    request.RequestFailed += (s, e) => { /* Do something */};
    request.ReceivedResponse += (s, e) => { /* Do something */};
    request.Start();
}
```
 
Notice the local variable `request`?  That was my culprit.  One change to a field and it all works:

```cs
private SKProductsRequest _request;

public void LoadAvailableProducts(params string[] productIdentifiers)
{
    var productKeys = new NSSet(productIdentifiers);
    _request = new SKProductsRequest(productKeys);

    _request.RequestFailed += (s, e) => { /* Do something */};
    _request.ReceivedResponse += (s, e) => { /* Do something */};
    _request.Start();
}
```

