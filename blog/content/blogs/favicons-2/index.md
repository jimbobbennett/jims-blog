---
author: "Jim Bennett"
categories: ["Technology", "ghost", "apple", "favicon", "theme", "ipad", "iphone"]
date: 2014-07-29T04:21:04Z
description: ""
draft: false
slug: "favicons-2"
tags: ["Technology", "ghost", "apple", "favicon", "theme", "ipad", "iphone"]
title: "Favicons"

images:
  - /blogs/favicons-2/banner.png
featured_image: banner.png
---


After [changing my avatars](/blogs/socialnetworkingandhowtheworldseesme/), I decided to update my Ghost blog to show my new avatar as the icon in the browser/bookmarks and springboard icon on iPhones/iPads.

Coming at this with limited HTML/Web experience I had no idea where to start, so thought I'd write this as a guid to help anyone else wanting to do the same thing.

What you need is called a Favicon.  By default the web browser picks up a file called favicon.ico from the web site root, but it can be changed by using the link tag.
```html
<link rel="icon" ... />
``` 

Wikipedia has a good article on it [here](http://en.wikipedia.org/wiki/Favicon).  Any normal image type can be used assuming you want it to work in the proper browsers (Chrome/Firefox/Safari/Opera), but for IE prior to version 11 you have to use an .ico file.  Converting to ico's is easy - there are plenty of sites that will do it for free.  I used [IconConverter](http://www.icoconverter.com/) for mine.

This works great for browsers, but Apple has the ability to use icons when adding a shortcut to your site to the springboard.  It supports multiple sizes to match the resolutions of different devices (so watch out when a new device comes out with a different resolution, make sure to update the icons).  The details of this are [here](https://developer.apple.com/library/mac/documentation/AppleApplications/Reference/SafariWebContent/ConfiguringWebApplications/ConfiguringWebApplications.html), but it essentially boils down to one link per icon size:

```html
<link rel="apple-touch-icon" href="touch-icon-iphone.png"/>
<link rel="apple-touch-icon" sizes="76x76" href="touch-icon-ipad.png"/>
<link rel="apple-touch-icon" sizes="120x120" href="touch-icon-iphone-retina.png"/>
<link rel="apple-touch-icon" sizes="152x152" href="touch-icon-ipad-retina.png"/>
```

The names in the hrefs are to indicate which device uses which icons, but you can use your own names of course.  The icons get the normal Apple reflective shine etc added to them - but this can be stopped by adding **-precomposed** to the the rel attribute:

```html
<link rel="apple-touch-icon-precomposed" href="touch-icon-iphone.png" />
```

The icon sizes must match the required size for the device.  These sizes are:

* iPhone - 60x60 (note iOS6 was 57x57, iOS7 is 60x60)
* iPad - 76x76
* Retina iPhone (iPhone 4 and later) - 120x120
* Retina iPad (third generation and later) - 152x152

Note that the original iPhone size was changed in iOS7 - so whenever a new iOS version comes out it's worth checking if there are any size changes.

To get these working on my Ghost blog, I edited the theme.  I am using a modified version of [Ghostion](https://github.com/axiantheme/ghostion) which I will be tidying up and making available publicly when I get a moment.  One note about Ghost - it provides it's own favicon in the root, so just by adding one to the root of your theme won't make it work - you will still get thge Ghost one. You have to place it somewhere other than the root and add links to the icons in your header.

**Note**
I made a few changes to this after a comment from  [RealFaviconGenerator](http://realfavicongenerator.net/).  It looks like they have an awesome site to generate all the favicons you could need automatically.  I haven't tried it out myself yet but will do next time I need one.

