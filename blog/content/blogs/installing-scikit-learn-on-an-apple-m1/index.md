---
title: "Installing Scikit-Learn on a Apple Silicon"
date: 2021-01-31T17:01:05Z
draft: false
featured_image: banner.png
images: 
  - blogs/installing-scikit-learn-on-an-apple-m1/banner.png
tags: ["ai", "python", "scikit-learn" ,"apple", "applesilicon"]
description: Learn how to install and run Scikit-learn on Apple Silicon (Apple M1)
---

At the end of last year I splashed out on a shiny new Apple MacBookAir with the M1 processor as I was fed up with an old Intel-based MacBookPro that was quite honestly crippled by corporate anti-virus software.

Out the box this machine is amazing. It's ridiculously fast, and lasts for ever on battery. Seriously - I charge it every 2 days and manage a full day of coding, writing, emails, Teams, the lot. Did I also mention it's fast? I can have all the things running and it barely breaks a sweat, even with only 8GB of RAM.

The downside is that not all software works on the new ARM-64 architecture. Apple have a translation layer called Rosetta 2 (Rosetta 1 was their translation from PowerPC to Intel), and this works great most of the time for every day apps, but it doesn't always work for development tools and libraries, as the mix of translated and untranslated stuff just breaks down.

One library I needed to use that isn't supported is Scikit-Learn. Now I'm no Python expert, and I don't really understand what Scikit-Learn does, I just know I need it to train some TinyML models to [recognize wake words on an Arduino Nano 33 sense board](https://eloquentarduino.github.io/2020/08/better-word-classification-with-arduino-33-ble-sense-and-machine-learning/). If I try a normal pip install scikit-learn, I get a whole wall of errors, both using Python 3.9 for the M1, and Python 3.8 under Rosetta.

So what to do?

It turns out the solution is to use [Miniforge](https://github.com/conda-forge/miniforge), a version of Conda that is comparable to Miniconda, but supports various CPU architectures. Whatever that means. As I said, I'm no Python expert, but this tool essentially allows me to create virtual environments and install packages compiling them for the M1 chip! Any packages it doesn't support can then be installed from pip.

So how do I install all this?

Firstly - I need to install Miniforge. The install script is on the GitHub page, or you can download it by clicking [this link](https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-MacOSX-arm64.sh). It wanted to activate it in every terminal, which I didn't want so I turned that off by running:

```bash
conda config --set auto_activate_base false
```

Next I went to the folder containing my Python code, and created a virtual environment:

```bash
conda create -n .venv python
```

This is pretty much the same as creating a virtual environment with Python, just using a different tool. Like with Python, the virtual environment then needs to be activated:

```bash
conda activate .venv
```

Finally, I can install Scikit-Learn:

```bash
conda install scikit-learn
```

Done! For the particular thing I'm working on, I needed a package that isn't available from Miniforge, so I just installed it with pip:

pip install micromlgen
Done! I could then run my Python script as normal, and it all worked nicely. And fast - my M1 ran the script in question in 2 seconds, 5 times faster than the 10 seconds my Surface Book took.