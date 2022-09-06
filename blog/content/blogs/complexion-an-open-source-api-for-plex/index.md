---
author: "Jim Bennett"
categories: ["Technology", "open source", "moomoo.io", "api", "plex", "github", "nuget", "c#", "alpha", "pcl", "portable class library"]
date: 2014-08-04T02:46:47Z
description: ""
draft: false
slug: "complexion-an-open-source-api-for-plex"
tags: ["Technology", "open source", "moomoo.io", "api", "plex", "github", "nuget", "c#", "alpha", "pcl", "portable class library"]
title: "Complexion - an open source API for Plex"

images:
  - /blogs/complexion-an-open-source-api-for-plex/banner.png
featured_image: banner.png
---


I've just released the first alpha version of [Complexion](https://github.com/jimbobbennett/ComPlexion), available on my [GitHub page](https://github.com/jimbobbennett/ComPlexion).  This is my first true open source API, which I hope to put up on NuGet in the near future.

This is a portable .Net API that connects to [Plex](http://plex.tv) - either to a local Plex Media Server specified by it's IP or hostname, or via MyPlex to discover your media servers.  This does require a [PlexPass](https://plex.tv/subscription/about) subscription.

To use the API via MyPlex, create an instance of the MyPlexConnection and connect using your MyPlex username and password to get all supported devices and servers that use your MyPlex account.

```
var myPlexConnection = new MyPlexConnection();
await plex.ConnectAsync(<userName>, <password>);
```

From each device, you can connect to a Server using the Server class.  You can also connect using a local URI if you don't want to connect to MyPlex.

```
var myPlexServer = myPlexConnection.Servers.First();
var server = new Server(myPlexServer, <userName>, <password>);
await server.ConnectAsync();
```

or

```
var server = new Server("192.168.1.1"); // IP address of local server
await server.ConnectAsync();
```

From here you can get a list of videos now playing on each client:

```
var videos = await server.GetNowPlayingAsync();
foreach (var video in videos)
  Console.WriteLine(video.title + " on " video.Player.title);
```

This is still a very early alpha - I haven't even checked in the unit tests yet, so the API will very likely change and may not even work (I haven't been able to test it using a remote connection as my current network setup doesn't allow my to open the port).  Please try it out and send me feedback or pull requests.

I will be dogfooding this API - I'm working on an app that uses it for [Moo Moo](http://MooMoo.io)

