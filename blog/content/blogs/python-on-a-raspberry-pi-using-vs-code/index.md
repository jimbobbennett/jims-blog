---
author: "Jim Bennett"
categories: ["technology", "raspberry Pi", "Visual Studio Code", "invalid opcode ba", "vscode", "Python"]
date: 2019-04-02T14:32:05Z
description: ""
draft: false
images:
  - /blogs/python-on-a-raspberry-pi-using-vs-code/banner.png
featured_image: banner.png
slug: "python-on-a-raspberry-pi-using-vs-code"
summary: "Want to use VS Code on a Raspberry Pi to code in Python?\n\nHere's how to do it."
tags: ["technology", "raspberry Pi", "Visual Studio Code", "invalid opcode ba", "vscode", "Python"]
title: "Python on a Raspberry Pi using VS Code"

images:
  - /blogs/python-on-a-raspberry-pi-using-vs-code/banner.png
featured_image: banner.png
---


I've recently been playing with a Raspberry Pi with the aim of learning Python. These are great little computers and have been an amazing success, selling 19 million as of March 2018, and kids everywhere are using them to learn to code with [Scratch](https://scratch.mit.edu) and Python.

{{< figure src="IMG_0252.jpg" >}}

The IDE for Python that is shipped by default is IDLE. This is a great IDE that comes as part of the standard Python install - it has an interactive shell and file editor, debugger and everything you need. It's good enough, but not quite on par with the world class editor that is [Visual Studio Code](https://code.visualstudio.com/?WT.mc_id=vscodepi-blog-jabenn).

Currently there aren't any official builds for VS Code for ARM processors, although there is a request for it on GitHub. Please head to this link and upvote it:

[https://github.com/Microsoft/vscode/issues/6442](https://github.com/Microsoft/vscode/issues/6442)

There is however a community build, courtesy of [Jay Rodgers](https://github.com/headmelted). You can find the installation instructions on [code.headmelted.com](https://code.headmelted.com), but I've found that these instructions don't work due to an [issue with the GPG key](https://github.com/headmelted/codebuilds/issues/71). There is a workaround!

To get the GPG key installed, launch a terminal and enter the following commands.

```sh
wget https://packagecloud.io/headmelted/codebuilds/gpgkey
sudo apt-key add gpgkey
```

Once done, you can run the installer script. Enter sudo mode using:

```sh
sudo -s
```

Then run the installer:

```sh
. <( wget -O - https://code.headmelted.com/installers/apt.sh )
```

This will install a non-VS branded version of code. The lack of Visual Studio branding is intentional - the code is open source, but the logos are copyright Microsoft. This means that a community build can't use these icons. You can launch this from the menu, _Raspberry->Programming->Code - OSS (Headmelted)_.

There is an [issue with v1.32](https://github.com/headmelted/codebuilds/issues/67). It will launch, but not run properly. The fix is to rollback to an earlier version, v1.29. To do this, run this command:

```sh
apt-get install code-oss=1.29.0-1539702286
```

This rolls back to an earlier version. This does mean if you run `apt-get update` at a later date the latest version will be installed, breaking it again. To stop this happening, you can lock the version using:

```sh
apt-mark hold code-oss
```

Once a fix has been released, you can remove the version lock with:

```sh
apt-mark unhold code-oss
```

Once you launch code you will be able to install the extensions you need. In my case, I wanted the Python extension.

{{< figure src="2019-04-02_15-22-17.png" >}}

Quick restart later and I'm up and running with a full Python environment inside VS Code, with a full debugger and all the goodies I could ever want!

