---
author: "Jim Bennett"
categories: ["Technology", "xamarin", "plex", "xamarin.ios", "pcl", "httpclient", "portable class library", "REST"]
date: 2014-07-30T07:16:02Z
description: ""
draft: false
slug: "portable-class-libraries"
tags: ["Technology", "xamarin", "plex", "xamarin.ios", "pcl", "httpclient", "portable class library", "REST"]
title: "Portable class libraries"

images:
  - /blogs/portable-class-libraries/banner.png
featured_image: banner.png
---


Portable class libraries (or PCLs) are the flavour of the month at the moment.  They are a .net library designed to be cross platform - so they work just as well on Windows 8 as they do on Xamarin.  Where Microsoft are supporting Xamarin as much as possible, they are releasing a number of their core libraries as PCL.

Unfortunately, where they are only recently a big thing, NuGet package support is limited.  I'm writing a client library for the [Plex](http://plex.tv) media server which I want to use from a Xamarin app (and will put up [here on GitHub](https://github.com/jimbobbennett/ComPlexion) once it's ready) and this makes hits the Plex REST API for it's communication.  Luckily, REST is easy on .Net thanks to RestSharp, an awesome NuGet package that simplifies creating REST clients.

Problem is, it's not PCL.  There is a PortableREST package but this doesn't have authentication which I need.  In the end, I decided to roll my own using Microsofts PCL [HttpClient](http://msdn.microsoft.com/en-us/library/system.net.http.httpclient%28v=vs.110%29.aspx).

Another downside is the support for different platforms.  Creating a PCL requires selecting which platforms will be supported, and not all of them have all the classes you may want to use.  For example, I'm using ObservableCollection, which is not supported in Silverlight 5, so my PCL doesn't support that platform.  Annoyingly, when you change the supported platform, you have to re-install any NuGet packages that target multiple platforms to get the version that targets the platforms you've selected.  Seems a bit of a faff really.

Going forward, I plan to make all my libraries PCL.  Hopefully more and more people will also do this.  And hopefully, the process will get easier.

