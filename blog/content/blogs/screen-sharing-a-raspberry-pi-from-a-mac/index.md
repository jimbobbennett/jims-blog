---
author: "Jim Bennett"
categories: ["technology", "raspberry Pi", "VNC", "mac"]
date: 2019-03-31T22:34:10Z
description: ""
draft: false
slug: "screen-sharing-a-raspberry-pi-from-a-mac"
tags: ["technology", "raspberry Pi", "VNC", "mac"]
title: "Screen sharing a Raspberry Pi from a Mac"

images:
  - /blogs/screen-sharing-a-raspberry-pi-from-a-mac/banner.png
featured_image: banner.png
---


I've been playing with a Raspberry Pi for a while, and I'm getting fed up with changing the input to my monitor and using a second keyboard/mouse (yeah, yeah, 1st World Problem I know). I decided to set up a remote screen share so I can share the screen. This means I can use the same monitor/keyboard/mouse that I use for my Mac, but it also means I can un-cable myself and use my Pi from anywhere in the house, and even grab screenshots - useful for some upcoming blog posts I'm planning.

As it turns out, it's really simple to get this set up.

## Configure the Pi

Start by enabling VNC on the Pi. To do this, click the Raspberry Menu and select _Raspberry Pi Configuration_. From the configuration tool, select the _Interfaces_ tab, then check the _Enabled_ option next to _VNC_. Click **OK**, then restart the Pi when prompted.

{{< figure src="2019-03-31_23-12-31.png" caption="" >}}

Once the Pi reboots, you need to configure VNC. Click the VNC icon in the menu bar.

{{< figure src="2019-03-31_23-15-58.png" caption="" >}}

This will launch the _VNC Server_ tool. Click the hamburger and select _Options_.

{{< figure src="2019-03-31_23-19-22.png" caption="" >}}

In the _Security_ tab, set the _Encryption_ to `Prefer off` and the _Authentication_ to `VNC Password`.

{{< figure src="2019-03-31_23-21-21.png" caption="" >}}

In the _Users & Permissions_ tab, select the _Standard user (user)_, and click the **Password...** button. Set the password then click **OK**, then click **OK.**

{{< figure src="2019-03-31_23-22-52-1.png" caption="" >}}

Finally you need the IP address of the Raspberry Pi. Launch a terminal, and type `ifconfig`. Find the `inet` address from `wlan0` and note this down.

{{< figure src="2019-03-31_23-25-59.png" caption="" >}}

## Connecting from the Mac

To connect from the Mac, open Finder, then select _Go -> Connect to server..._. Enter the address as `vnc://<ip address of the Pi>`, for example `vnc://192.168.2.10`. Click **Connect**.

{{< figure src="2019-03-31_23-28-04.png" caption="" >}}

You will be prompted for a password. Enter the password you set up for your VNC standard user and check the box to remember this password. Click **Sign In**.

{{< figure src="2019-03-31_23-30-00.png" caption="" >}}

Screen sharing will launch, showing your Raspberry PI desktop!

{{< figure src="2019-03-31_23-33-15.png" caption="" >}}



