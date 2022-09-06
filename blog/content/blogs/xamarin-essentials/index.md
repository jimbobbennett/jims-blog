---
author: "Jim Bennett"
categories: ["xamarin", "technology", "iOS", "Android", "nuget", "Xamarin.Essentials"]
date: 2018-05-08T15:48:04Z
description: ""
draft: false
images:
  - /blogs/xamarin-essentials/banner.png
featured_image: banner.png
slug: "xamarin-essentials"
tags: ["xamarin", "technology", "iOS", "Android", "nuget", "Xamarin.Essentials"]
title: "Xamarin Essentials"

images:
  - /blogs/xamarin-essentials/banner.png
featured_image: banner.png
---


TL;DR - check out Xamarin Essentials in the [official documentation](https://docs.microsoft.com/en-gb/xamarin/essentials/?WT.mc_id=pocketmoney-blog-jabenn).

<hr/>

Like a lot of developers, I love how Xamarin allows me to share business logic between iOS and Android apps, and share UI using Forms, but still have access to the native APIs. But one thing has been missing - a consistent, out of the box way of accessing native APIs from cross-platform code. The power of Xamarin is you have full API access allowing you to take advantage of the unique features of each platform, but sometimes you just want to do something in one line of code that applies to all platforms.

Plugins have helped with this - so you can install a NuGet package such as the [permissions](https://www.nuget.org/packages/Plugin.Permissions/) or [connectivity](https://www.nuget.org/packages/Xam.Plugin.Connectivity/) plugins from James Montemagno and have a nice cross-platform API, but discoverability has always been a bit hard, you have to know there is a plugin and what the NuGet package is called.

To make it easier, there is now [Xamarin.Essentials](https://www.nuget.org/packages/Xamarin.Essentials/), a single package that you can install into any Xamarin app to get cross-platform access to a wide range of APIs such as accelerometer, compass, network connectivity, keeping the screen awake and more. You can see the full list of supported features on the [Xamarin Essentials GitHub page](http://github.com/xamarin/Essentials). This package currently has 24 different API sets, with more planned. Essentials is for all Xamarin apps, both traditional and Forms apps.

<div class="image-div" style="max-width: 128px;"> 
    
![Xamarin Essentials logo](xamarin.essentials_128x128.png)
    
</div>

I've started building an app to track my daughters pocket money - I don't use cash so it's hard to regularly put cash into a piggy bank, instead I though I'd write an app I can use to regularly put an amount into a virtual account, and when she wants to spend it, use my card for the purchase (easier with Amazon for example) and deduct the cost from her virtual piggy bank. The first part of this app is logging in, and for that I'm going to use [social auth and Azure](/blogs/authenticating-your-xamarin-app-with-azure-and-facebook/), but there is no point in showing a login screen if the user is not connected to the internet, so I thought I'd give Essentials a spin and use the connectivity part.

Setting it up is easy, just install the NuGet package into all projects in your app (it must be all as it has the platform specifics in the iOS and Android packages). For Android you do need to initialize the library and set up some permissions stuff in all activities. I'm using Xamarin Forms, so only have one activity to do it in:

```cs
protected override void OnCreate(Bundle savedInstanceState)
{
    ...
    Forms.Init(this, savedInstanceState);
    Xamarin.Essentials.Platform.Init(this, savedInstanceState);
    ...
}

public override void OnRequestPermissionsResult(int requestCode, 
                                                string[] permissions, 
                                                [GeneratedEnum] Permission[] grantResults)
{
    Xamarin.Essentials.Platform.OnRequestPermissionsResult(requestCode, permissions, grantResults);
    base.OnRequestPermissionsResult(requestCode, permissions, grantResults);
}
```

Done - Essentials is all set up. Checking connectivity is now really easy:

```cs
using Xamarin.Essentials;
...
if (Connectivity.NetworkAccess != NetworkAccess.Internet)
{
   ... // no internet access	
}
```

Checking network access is as simple as checking the value of the `Connectivity.NetworkAccess` static property. If this is set to `NetworkAccess.Internet` then there is internet access. There is also an enum member called `ConstrainedInternet` when there is a connection but with a poor signal. Otherwise - no internet.

> These properties are all static, which might seem odd to developers who prefer interfaces for use in IoC containers. There is a discussion around this on the [README.md on GitHub](https://github.com/xamarin/Essentials#where-are-the-interfaces).

I might also want to be notified when the users internet access has changed. For example if I hide the login button when they are not connected due to being in airplane mode, I'd want my app to know when they turned airplane mode off so it can show the login button again. I can do this using the `Connectivity.ConnectivityChanged` event. This means the code for my login page can be:

```cs
public LoginPage()
{
    ...
    Connectivity.ConnectivityChanged += e => ShowOrHideLoginButton();
    ShowOrHideLoginButton();
}

void ShowOrHideLoginButton()
{
    LoginButton.IsVisble = (Connectivity.NetworkAccess == NetworkAccess.Internet ||
                            Connectivity.NetworkAccess == NetworkAccess.ConstrainedInternet);
}
```

You can read more about Xamarin Essentials in the [official documentation](https://docs.microsoft.com/en-gb/xamarin/essentials/?WT.mc_id=pocketmoney-blog-jabenn). Also check out the [GitHub page](https://github.com/xamarin/Essentials) - this library is fully open source like all Xamarin goodness, and you can raise issues or pull request there if you feel like contributing to this awesome project.

