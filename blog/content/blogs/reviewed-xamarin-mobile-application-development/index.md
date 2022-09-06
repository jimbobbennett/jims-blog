---
author: "Jim Bennett"
categories: ["xamarin", "xamarin.forms", "review", "book"]
date: 2015-07-27T18:03:59Z
description: ""
draft: false
slug: "reviewed-xamarin-mobile-application-development"
tags: ["xamarin", "xamarin.forms", "review", "book"]
title: "Reviewed - Xamarin Mobile Application Development"

images:
  - /blogs/reviewed-xamarin-mobile-application-development/banner.png
featured_image: banner.png
---


# Xamarin Mobile Application Development
#### By [Dan Hermes (@ lexiconsystems)](https://twitter.com/lexiconsystems)

<div style='text-align:center'>
<a href='http://www.amazon.co.uk/gp/product/1484202155/ref=as_li_qf_sp_asin_il_tl?ie=UTF8&camp=1634&creative=6738&creativeASIN=1484202155&linkCode=as2&tag=expecti-21'>
    
![Xamarin Mobile Application Development](51fV5TiEetL-_SX346_BO1-204-203-200_.jpg)
    
</a>
</div>
<br/>

Recently I was lucky enough to get my hands on an early draft of Xamarin Mobile Application Development by Dan Hermes.  This is a book aimed at the .Net developer who wants to get started with Xamarin, primarily with Xamarin.Forms.

Let me start by saying this isn't a 'read it on the train' book - it's very code heavy.  As each new concept is introduced, you get sparse text with a code example to cement the concepts - so I would say it's very much aimed at the developer sitting at their laptop who can read and then work through the example code.  Luckily the examples are excellent and are available in pure C# code in the book, and in both C# and Xaml on GitHub.  Personally I would have preferred if the code focused on Xaml, but then I am a huge Xaml fan.  Perhaps a suggestion to the author is to have 2 versions - a pure C# version and a Xaml version (or even 3 and do an F# one).

The book is primarily aimed at iOS and Android development, but it does sometimes dip in to Windows Phone - for example the Xamarin.Forms screenshots and sample code includes Windows Phone, as does some of the cross platform chapters.  But this is about the limit of the Windows Phone code - there's nothing on the platform specific Windows Phone controls for example, wheres iOS and Android controls are covered in detail.  Seeing as the market for Windows Phone is so small, this is not a huge omission but Windows Phone developers need to be aware of this.

The book starts off with a brief introduction to cross platform development before diving right into the UI - a sensible place to start and ideal for the new developer as it allows you to quickly get a 'Hello, World!' type app running in next to no time.  As it introduces the UI's it discusses the different approaches - native or cross platform.  This is an important choice for the developer to make and the pros and cons of each approach are discussed.  It then jumps into the controls and provides simple examples of the standard control set available through Xamarin.Forms.  This is followed up by describing the same controls from the native platforms, giving a thorough understanding of the widget sets available (although not Windows Phone).  These examples are not API level depth - it doesn't discuss all the properties, methods, events and usage patterns of each control, instead it gives you the basics providing a springboard for your own self discovery.  As mentioned before - this is a book for someone who is reading it whilst writing code so can explore the depth of what each control has to offer in their own time.

The controls take up a large part of the book- understandable as there are a lot, and these are the fundamental building blocks of a mobile app.  The biggest difference between Mobile apps and other apps you may have been working on is primarily the UI, both the controls and the user interaction patterns so it makes sense to focus a lot on these.  Server side code or business logic is the same regardless of platform, so this isn't really covered here.
As well as the basic widgets, navigation patters and their associated control sets are also covered.  This is important with a mobile app, as a user needs to navigate using a standard control set.

What is covered next is how your app should integrate with the business logic and back end code, followed by how to do platform specific things in a cross platform code base.  I would recommend reading the chapters in a different order to the book at this point though.  It covers data access and binding, which is how you app will interact with data and how it can be updated on screen using the standard MVVM design pattern that all Xamarin.Forms apps uses, then talks about platform specific UI before discussing cross platform architectures.  My recommendation is to read chapter 9 (Cross-platform architecture) before chapters 7 (Data access and data binding) and 8 (Custom rendered and platform-specific UI), so you can get an understanding of how and why to use the different cross platform techniques before you use them in anger.  The coverage of the two different methods, PCLs and shared projects, is good, but I would personally like it to lean heavier on the PCL side - especially as Xamarin themselves are saying this is the preferred method.

## TL;RD
Overall it's a good book for C# coders who want to get into Xamarin for cross platform development.  I like Dan's writing style - it is terse and to the point, but friendly to read.  The nearest competitor to this book at the moment is <span><a href="http://www.amazon.co.uk/gp/product/B00VYSSNJW/ref=as_li_tl?ie=UTF8&camp=1634&creative=19450&creativeASIN=B00VYSSNJW&linkCode=as2&tag=expecti-21&linkId=SDHB4LS764DZDT6Q">Creating Mobile Apps with Xamarin.Forms by Charles Petzold (affiliate link)</a><img src="http://ir-uk.amazon-adsystem.com/e/ir?t=expecti-21&l=as2&o=2&a=B00VYSSNJW" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" /></span> and whilst this has the huge advantage of being free and written at the behest of Xamarin (with access to the newest features before they become available), I don't like the writing style.  This is something I've always found with Petzold - the guy is a genius and provides excellent materials in his books but they are hard to read with a very dry style.  Dan's book is easier to read.
The examples are good, and if you dive into this book willing to code as you read it provides a great introduction.

There are downsides with this book.  I would like it to go further - technology moves quickly and Xamarin.Forms is constantly changing including new features like styles and behaviours which are not covered.  This is the downside to print, but hopefully the eBook will be able to be updated to cover the latest features, or a follow up will be written.  I would also like more on custom renderers as this is a massively powerful way to extent a cross platform app.  The basics are covered but this topic is huge.  Again, perhaps a follow up book would cover this.  
The other downside is the price - Petzold's book is free and although it's not as good I can imagine developers dipping into Xamarin for the first time might prefer the free option to get started.

All in all though, it is a good book and well worth buying to work through armed with your favourite IDE in hand.  I'm certainly looking forward to any follow ups that Dan writes.


[Buy it from Amazon here (affiliate link)](http://www.amazon.co.uk/gp/product/1484202155/ref=as_li_qf_sp_asin_il_tl?ie=UTF8&camp=1634&creative=6738&creativeASIN=1484202155&linkCode=as2&tag=expecti-21)

