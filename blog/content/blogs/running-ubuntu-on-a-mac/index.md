---
author: "Jim Bennett"
categories: ["Technology", "apple", "mac", "Apple Silicon", "M1", "VM", "Virtual machine", "ubuntu"]
date: 2023-01-24
description: ""
draft: false
images:
  - /blogs/running-ubuntu-on-a-mac/banner.jpg
featured_image: banner.jpg
slug: "running-ubuntu-on-a-mac"
tags: ["Technology", "apple", "mac", "Apple Silicon", "M1", "VM", "Virtual machine", "ubuntu"]
title: "Run an Ubuntu VM on your Mac with a single command"
---

I recently needed to run Linux so I could test out what Python version was installed, and how to upgrade it for some documentation I'm creating.

I don't have a spare machine to set up as a Linux box, and didn't want to use a Raspberry Pi, I wanted a clean Ubuntu install.

My original thought was to use VMWare Fusion Player, and spin up a VM, but things got a bit tricky - I installed it, created a new Ubuntu VM, and it just didn't work. It didn't have any install media, and just failed to boot. I'm not sure why, I just assumed 'Create an Ubuntu VM' would just work...

So digging for an ISO, I cam across another method to install - [Multipass from Canonical](https://multipass.run). No, this isn't cheap movie tickets, instead its a free way to manage VMs using the hypervisor built into your OS - Hyper-V on Windows, QEMU and HyperKit on macOS and LXD on Linux.

## Installing Multipass

Multipass was easy to install on my Mac - it can be installed via homebrew:

```bash
brew install --cask multipass
```

```output
==> Downloading https://github.com/canonical/multipass/releases/download/v1.11.0
==> Downloading from https://objects.githubusercontent.com/github-production-rel
######################################################################## 100.0%
==> Installing Cask multipass
==> Running installer for multipass; your password may be necessary.
Package installers may write to any location; options such as `--appdir` are ignored.
Password:
installer: Package name is multipass
installer: Installing at base path /
installer: The install was successful.
🍺  multipass was successfully installed!
```

I had to enter my password (which makes sense as this installs some OS level stuff), but in a few seconds it was installed.

## Creating a VM

Creating a new VM is easy - just one command to create and launch it:

```bash
multipass launch
```

This takes a loooooooong time the first time as it needs to download an image and create the new VM. Once the VM is created it will launched given a two-word name.

```output
➜  ~ multipass launch
Launched: disarming-woodcock  
```

You can get more info on the VM using the `info` command with the instance name:

```bash
➜  ~ multipass info disarming-woodcock
```

```output 
Name:           disarming-woodcock
State:          Running
IPv4:           192.168.64.2
Release:        Ubuntu 22.04.1 LTS
Image hash:     8593ce1c6bbd (Ubuntu 22.04 LTS)
CPU(s):         1
Load:           0.27 0.17 0.07
Disk usage:     1.4GiB out of 4.7GiB
Memory usage:   149.2MiB out of 962.7MiB
Mounts:         --
```

Once the VM is running, you can log in to it using the `shell` command with the instance name:

```bash
multipass shell disarming-woodcock
```

Done! I now have an Ubuntu VM ready to play with.
