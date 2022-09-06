---
author: "Jim Bennett"
categories: ["technology", "xamarin", "Visual Studio", "Mac", "extension", "dotnet new"]
date: 2017-11-08T07:06:26Z
description: ""
draft: false
slug: "creating-visual-studio-project-and-solution-templates-part-3-vs-for-mac-extension"
tags: ["technology", "xamarin", "Visual Studio", "Mac", "extension", "dotnet new"]
title: "Creating Visual Studio project and solution templates - Part 3, VS for Mac extension"

images:
  - /blogs/creating-visual-studio-project-and-solution-templates-part-3-vs-for-mac-extension/banner.png
featured_image: banner.png
---


In the [first part of this set of posts](/blogs/creating-dotnet-new-and-visual-studio-project-and-solution-templates/) I looked at creating a dotnet new project template, and in the [second part](/blogs/creating-visual-studio-project-and-solution-templates-part-2-vs-for-windows-extension-2/) I showed how you could easily add this to a Visual Studio for Windows extension. Lets now look at adding it to a Visual Studio for Mac extension, so that our template is available everywhere.

It's really easy to create extensions for VS for Mac for new project types. In a [previous blog post](/blogs/creating-an-add-in-for-xamarin-studio/) I discussed the old way of doing it which, like for VS on Windows, involved a load of files that couldn't be compiled as they had replacement tokens, and no easy way to test the output projects without debugging the extension.

This all changes now. Instead of adding all the project files, you just need to add the NuGet package created for `dotnet new` with a build action of Add-In File, then add an entry into the `Manifest.addin.xml` file to make it available:

```
<Extension path="/MonoDevelop/Ide/Templates">
  <Template
    id="MvvmCrossNativeSinglePage.CSharp"
    _overrideDescription="Creates a new single page native MvvmCross app."
    path="Templates/MvvmCross.Templates.CSharp.Native.SinglePage.iOS.Android.nupkg"
    category="other/net/mvvmcross"
    icon="res:MVVMCross.XSAddIn.Icons.MvvmCross.png"/>
  </Extension>
```

This manifest entry provides a description to show in the File->New dialog, the category in that dialog to put the template into, an icon and the path in the addin to the NuGet package. You can add as many NuGet packages as you want, with one `Template` entry per NuGet package. And that's it - no need to add the project files, `xpt.xml` files or anything hard like that. You can see an example of this with my MvvmCross templates on [my GitHub](https://github.com/jimbobbennett/MvvmCross-Templates).

