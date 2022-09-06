---
author: "Jim Bennett"
categories: ["technology", "xamarin", "fabulous", "f#", "xamarin.forms"]
date: 2019-02-16T20:35:51Z
description: ""
draft: false
slug: "xamarin-f"
tags: ["technology", "xamarin", "fabulous", "f#", "xamarin.forms"]
title: "Xamarin ❤ F#"

images:
  - /blogs/xamarin-f/banner.png
featured_image: banner.png
---


[Xamarin](aka.ms/XamDocs) and [Xamarin.Forms](aka.ms/XamFormsDocs) need no introduction. I'm sure by now you are well aware of these technologies and have seen many examples of building cross-platform mobile apps using C#. If not, I can highly recommend my book [Xamarin in Action](xam.jbb.io) which if you follow [this link](xam.jbb.io) and use code 'xamarininaction' you can get 40% off the cover price.

What you many not realize however, is you don't have to just use C#. Yes, C# is a fantastic object-oriented language, but what if you like functional programming?

The answer is [F#](https://aka.ms/learnfs). F# is a functional-first programming language that is fully compatible with the .NET stack. What does 'functional-first' mean? Well it means it is a functional programming language that also supports object-orientation, classes and inheritance and whatnot. Essentially it encourages function programming whilst still supporting enough to interact with the OO world of the .NET framework.

For Xamarin developers, this is pretty awesome. Out the box F# is supported. This means you can build your apps in the same way as you would with C#, just using F#. You can write all your internal logic in a functional style, then take advantage of the OO features to interact with the APIs - derive a class from `UIApplicationDelegate` to configure your iOS app, derive a class from `Activity` for your Android app.

As is, this is pretty good combining the best of both worlds. This is far from perfect though for functional programmers - if you are going to use a functional programming language then you want to take advantage of everything the language has to offer, and not flip-flop from FP to OO style.

This dilemma has lead to a new framework being created, [Fabulous](https://fsprojects.github.io/Fabulous/guide.html). This framework sits on top of Xamarin.Forms and provides an MVU style architecture, putting a FP layer over the OO of UI code.

MVU stands for Model-View-Update and consists of 4 main parts:

**Model** - this is an immutable model containing all the state of your application. This model cannot change, and this is enforced by using an [F# record type](https://docs.microsoft.com/dotnet/fsharp/language-reference/records/?WT.mc_id=fsharp-blog-jabenn) which is immutable by default. This allows you to stop worrying about the state of you application, as it is always in this model - in a single, well defined place.

**Message** - these define a start transformation request, and are triggered by either UI events like a button tap, or background events like a network call finishing or a push notification. These have a defined type, and can optionally have data taking advantage of the [F# discriminated union type](https://docs.microsoft.com/dotnet/fsharp/language-reference/discriminated-unions/?WT.mc_id=fsharp-blog-jabenn).

**Update** - this is a function that takes a model and a message and returns a new model. This is the only place that the state of the system can change, and is called synchronously removing any worries about race conditions.

**View** - this is a function that takes the model and returns a virtual UI based off the model. This virtual UI is lightweight, and can be thought of as analogous to HTML as text, a raw representation that is rendered on screen creating heavyweight UI components. The framework takes the virtual UI returned by this function and compares it to the actual UI. If any differences are found, the real UI is updated to match. This is called a differential update.

This design pattern brings the full power of functional programming to the OO based world of UI development, allowing you to craft great mobile apps using Xamarin, but sticking to the amazing power, flexibility and development pace of F#. And because it is built on Xamarin.Forms you get to maximize the amount of cross-platform code you write, but still can access all the native features you need, including being able to access the native controls being rendered, call any native API and even use native libraries from Java or Objective-C.

I recently spoke about this pattern at NDC London, and you can find my code, slides and some great links on [my GitHub](https://github.com/jimbobbennett/BuildingCrossPlatformMobileAppsWithFabulous). The video of my talk will be up there soon.

Go check it out, I promise you once you start using Fabulous you won't be disappointed.

