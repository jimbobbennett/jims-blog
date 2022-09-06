---
author: "Jim Bennett"
categories: ["xamarin", "xamarin.ios", "Technology", "firewall"]
date: 2017-08-10T01:19:54Z
description: ""
draft: false
images:
  - /blogs/firewall-issues-with-ios-simulators/banner.png
featured_image: banner.png
slug: "firewall-issues-with-ios-simulators"
tags: ["xamarin", "xamarin.ios", "Technology", "firewall"]
title: "Firewall issues with iOS simulators"

images:
  - /blogs/firewall-issues-with-ios-simulators/banner.png
featured_image: banner.png
---


I keep getting an annoying issue with my iOS simulators. When I run an app in a simulator that needs any form of network connection I get a dialog box popup from the built in Mac firewall asking if I want to allow incoming connections. Even though I click 'allow', I get asked this every time and it's getting tedious.

<div class="image-div" style="max-width: 500px;">
    
![Firewall request from the simulator](Screen-Shot-2017-08-10-at-13.10.13-1.png)
    
</div>

The issue seems to be in the firewall. When I allow an iOS app it permits the app to access the network, but the iOS simulator does not seem to have permissions. The firewall gets confused - the simulator doesn't have permissions so the network request is blocked pending approval from me, but the firewall doesn't 'see' the simulator, instead it sees the iOS app and gives that permission.

The problems comes from Xcode, it should set the firewall permissions when you install it but sometimes it fails. There is an easy fix - I've got a script that opens up the firewall to the simulator. It turns the firewall off (so make sure you are disconnected from the internet or not anywhere dodgy), enables Xcode and the iOS simulator as a firewall exception, then turns it back on.

```bash
# temporarily shut firewall off:
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate off

# put Xcode as an exception:
/usr/libexec/ApplicationFirewall/socketfilterfw --add /Applications/Xcode.app/Contents/MacOS/Xcode

# put iOS Simulator as an exception:
/usr/libexec/ApplicationFirewall/socketfilterfw --add /Applications/Xcode.app/Contents/Developer/Applications/Simulator.app/Contents/MacOS/Simulator

# re-enable firewall:
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate on
```

Run this, give it your password as it needs `sudo` access and bingo, problem goes away. You may need to run this every time Xcode is updated though...

