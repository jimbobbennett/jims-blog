---
author: "Jim Bennett"
categories: ["Visual Studio", "Technology", "iOS", "ios", "javascript", "technology", "node"]
date: 2014-08-14T02:18:56Z
description: ""
draft: false
slug: "images-for-an-ios-app"
tags: ["Visual Studio", "Technology", "iOS", "ios", "javascript", "technology", "node"]
title: "Images for an iOS app"

images:
  - /blogs/images-for-an-ios-app/banner.png
featured_image: banner.png
---


When developing for iOS there are a number of different image sizes needed.  Just for the springboard icon you need different sizes for iPhones and iPads, both retina and normal versions.  When you add spotlight icons (again both retina and normal), iTunes icons the list gets huge.

To help with this and to practice my Node.js skills, I created a node app that does it for you.  It's based on the default express app, you give it an image file and it downlods you a zip file containing all the possible image sizes you could want all named correctly.
The code uses Express 3.  I know express 4 is out, but 4 doesn't support file uploads using body-parser.  When I work out how to do it, I'll update the code.

This is built using the [Node.js tools for Visual Studio](https://nodejstools.codeplex.com) but the code will run with any node install.  You will need [ImageMagick](http://www.imagemagick.org) installed to make it work.

[Clone it from my GitHub](https://github.com/jimbobbennett/ImageResizer)

