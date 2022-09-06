---
author: "Jim Bennett"
categories: ["Technology", "open source", "api", "nuget", "jimlib"]
date: 2014-08-10T03:34:31Z
description: ""
draft: false
slug: "my-first-nuget-package"
tags: ["Technology", "open source", "api", "nuget", "jimlib"]
title: "My first NuGet package"

images:
  - /blogs/my-first-nuget-package/banner.png
featured_image: banner.png
---


For pretty much every project I've worked on I've used the same set of extensions and helper classes to make my life easier.  For example:

* Fluent API on strings `myString.IsNullOrEmpty()` instead of `string.IsNullOrEmpty(myString)`.
* An `ObservableCollectionEx<T>` class that allows adding multiple items but only raising on `CollectionChanged` event.

For my latest project, I've found myself creating these all over again. Seeing as I'm using this for an open source API, I thought it might be time to wrap these up into another open source library and make it available on NuGet.  Therefore I present JimLib to the world.

The source is on [GitHub](https://github.com/jimbobbennett/JimLib) with the API described on the [Wiki](https://github.com/jimbobbennett/JimLib/wiki).

The package is available from [NuGet](http://www.nuget.org/packages/JimBobBennett.JimLib/).

Install using `Install-Package JimBobBennett.JimLib`.

Submissions and feedback are welcome.  I'll be expanding this library as I go along.

