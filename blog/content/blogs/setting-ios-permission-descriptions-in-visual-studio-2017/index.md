---
author: "Jim Bennett"
categories: ["xamarin", "xamarin.ios", "technology", "docs"]
date: 2018-07-05T14:39:40Z
description: ""
draft: false
slug: "setting-ios-permission-descriptions-in-visual-studio-2017"
tags: ["xamarin", "xamarin.ios", "technology", "docs"]
title: "Setting iOS permission descriptions in Visual Studio 2017"

images:
  - /blogs/setting-ios-permission-descriptions-in-visual-studio-2017/banner.png
featured_image: banner.png
---


I spend most of my developer day using Visual Studio for Mac, but occasionally I flip back to Visual Studio 2017 on Windows. Last time I flipped back I tried to build an app that uses the camera and I got stuck on one simple thing - setting the camera usage description.

If you double click on the `info.plist` file in an iOS app project, it will open in the iOS manifest editor. This editor allows you to set or change a number of settings for your app, such as the bundle identifier, app name or scheme URLs that your app uses. But one thing this editor doesn't support is setting the usage descriptions.

After a quick chat to some other developers, I found out how to do it (thanks [Pierce](https://twitter.com/pierceboggan)).

From Visual Studio, right-click on the `info.plist` file, then select __Open With...__.

From the __Open With...__ dialog, select the __Generic PList Editor__.

<div class="image-div" style="max-width:480px;">
    
![Select the Generic PList editor from the open with dialog](InfoEditorSelectionVs.png)
    
</div>

Once the file has been opened, click the __+__ on the bottom row to create a new property. Click the property name to get a drop down showing all the supported properties, then click the one you want.

<div class="image-div" style="max-width:480px;">
    
![Selecting the property key](InfoPListEditorSelectKey.png)
    
</div>

Finally add the description to the __Value__ column.

<div class="image-div" style="max-width:480px;">
    
![Setting the property value](InfoPListSetValue.png)
    
</div>

Read more about this in the [docs](https://docs.microsoft.com/en-us/xamarin/ios/app-fundamentals/security-privacy?tabs=vswin#setting-privacy-keys&WT.mc_id=ios-blog-jabenn).

> At the time of writing, the docs are out of date, showing that there is no `info.plist` editor support in VS on Windows. But worry not, I've already submitted a PR against the docs to fix this, so hopefully by the time you read this the docs will be up to date.

