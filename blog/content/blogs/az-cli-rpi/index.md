---
author: "Jim Bennett"
categories: ["raspberrypi", "azure", "az", "cli"]
date: 2023-03-08
description: ""
draft: false
slug: "az-cli-rpi"
tags: ["raspberrypi", "appwrite", "rpi", "docker"]
title: "Install the Azure CLI on a Raspberry Pi"

images:
  - /blogs/az-cli-rpi/banner.png
featured_image: banner.png
---

I do a lot with Raspberry Pis, and sometimes I want all my tools installed in one place so I can use my Pi for everything, rather than flipping back to my Mac.

One thing I use a lot is Azure - funny really as I work for Microsoft! I often use the Azure portal as I prefer UIs to CLIs, but when working on a Pi I regularly use Raspberry Pi OS Lite, so don't have a browser to use as I'm always in the terminal or VS Code. So I needed the Azure CLI on my Pi.

## Hardware

I'm currently doing everything on a Raspberry Pi 4 as I have a few of them (will trade one for a Lamborghini - no low ballers, I know what I have), so have one of these set up with Raspberry Pi OS Lite 32-bit. I've not tested this on 64-bit, but I'm guessing it should work.

## Pre-requisites

To install the CLI, you can't just use the apt package - this only currently supports x86, not armhf. Instead it needs to be installed from an install script that installs a raw Python CLI. This has a few dependencies:

* [libffi](https://sourceware.org/libffi/)
* [Python 3.6 or later](https://python.org)
* [OpenSSL](https://www.openssl.org/source/)

Run the following to ensure everything is installed:

```bash
sudo apt install libffi-dev python3-dev python3-pip openssl
```

## Install the Azure CLI

Once the pre-requisites are installed, you can use a handy script from Microsoft to install the CLI:

```bash
curl -L https://aka.ms/InstallAzureCli | bash
```

Run this with all the defaults.

This adds the `az` command to the `/home/pi/bin/` folder, and gives you an option to add this to your path, which you should accept. You'll then need to manually restart your shell or run `exec -l $SHELL` to restart it.

## Login

Once installed, you can log in with `az login`. It's smart enough to realize you don't have a web browser, and take you through the device login path, giving you a code. Head to [https://microsoft.com/devicelogin](https://microsoft.com/devicelogin) and enter the code given to get logged in!
