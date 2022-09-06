---
author: "Jim Bennett"
categories: ["xamarin", "Technology", "xamarin.android", "java", "binding", "aar", "jar", "COMPILETODALVIK", "invalid opcode ba", "invokedynamic"]
date: 2018-09-10T11:22:55Z
description: ""
draft: false
slug: "binding-the-cognitive-services-android-speech-sdk-part-3-java-8-fun"
tags: ["xamarin", "Technology", "xamarin.android", "java", "binding", "aar", "jar", "COMPILETODALVIK", "invalid opcode ba", "invokedynamic"]
title: "Binding the Cognitive Services Android Speech SDK - Part 3 - Java 8 fun"

images:
  - /blogs/binding-the-cognitive-services-android-speech-sdk-part-3-java-8-fun/banner.png
featured_image: banner.png
---


In the [first part](/blogs/binding-the-cognitive-services-android-speech-sdk) of this post, I showed how to get started binding the [Microsoft Cognitive Services speech API](https://docs.microsoft.com/azure/cognitive-services/speech-service/?WT.mc_id=speech-blog-jabenn). In the [second part](/blogs/binding-the-cognitive-services-android-speech-sdk-part-2-making-the-code-more-c-like) I showed how to make the code look more C#-like. In this part, I'll show how to use it and fix up a nasty issue with the Android compiler and using jars created with the latest versions of Java.

## Using the SDK

To use the SDK, you will need an Android app. Create a new single-view Android app, and reference the SDK binding project. Then build the app and try to run it.

Then marvel, as your app spectacularly fails to compile with a really weird error message.

```sh
COMPILETODALVIK : Uncaught translation error : com.android.dx.cf.code.SimException: invalid opcode ba (invokedynamic requires --min-sdk-version >= 26)
```

WooHoo, invalid opcode ba. Ba indeed! What is this gibberish?

Well the issue comes down to Java versions. Android in the past only supported Java code up to version 7. They are now adding support for later versions but Xamarin doesn't have this yet, and this is only available on newer versions of Android (>= 26). To make your code work on earlier versions and with Xamarin you have to do a thing called desugaring (yes, really), and this alters the Java bytecode to convert Java 8 bytecode to a version that is supported by Java 7.

At the moment there isn't a nice IDE way to turn on desugaring, instead it has to be set inside the `.csproj` file of the client application. Open up the `.csproj` file for your newly created Android app inside [VSCode](https://code.visualstudio.com/?WT.mc_id=speech-blog-jabenn) (other editors are available, but hey - why would you), or by editing the file inside Visual Studio, and add the following to the default `PropertyGroup`:

```xml
<AndroidEnableDesugar>true</AndroidEnableDesugar>
```

Your app should now build without errors!

> I have this working and compiling in the preview versions of Visual Studio on Windows at the time of writing cos that's how I roll. If you are on stable and get weird errors then try with preview as I know support for this is being actively worked on.

> If you do this on VS for Mac then you will get a crash at run-time. The workaround is documented here: https://github.com/xamarin/xamarin-android/pull/1973

## Buiding an app using the SDK

To use the SDK you do need to sign up for the Speech service in Azure. Head to [portal.azure.com](https://portal.azure.com/?WT.mc_id=speech-blog-jabenn) and add a new Speech resource (at the time of writing this is in preview).

<div class="image-div" style="max-width:600px;">
    
![Searching for the speech resource in Azure](2018-09-09_20-43-15.png)
    
</div>

Once you have this, note down the endpoint from the __Overview__ page. It will be a URL, and you will need the bit before `.api.cognitive.microsoft.com`. For example, if your endpoint is `https://northeurope.api.cognitive.microsoft.com/sts/v1.0`, then you will need `northeurope`. You will also need one of the two keys from the __Keys__ page.

You can then create a `SpeechFactory` using these values:

```cs
var factory = SpeechFactory.FromSubscription(<SpeechApiKey>, <endpoint>);
```

Once you have a speech factory, you can create different recognizers - simple speech, a translator, or an intent recognizer using [LUIS](https://www.luis.ai/?WT.mc_id=speech-blog-jabenn). To detect speech, handle the relevant events. You can see an example of using the `TranslationRecognizer` to convert English to spoken German in an example project in my [GitHub repo](https://github.com/jimbobbennett/SpeechSdkXamarinSample/blob/master/SpeechQuickStart/MainActivity.cs).

<blockquote class="twitter-tweet" data-lang="en"><p lang="en" dir="ltr">Had a successful day. Created a <a href="https://twitter.com/hashtag/Xamarin?src=hash&amp;ref_src=twsrc%5Etfw">#Xamarin</a> binding for the <a href="https://twitter.com/Azure?ref_src=twsrc%5Etfw">@Azure</a> <a href="https://twitter.com/hashtag/CognitiveServices?src=hash&amp;ref_src=twsrc%5Etfw">#CognitiveServices</a> Android speech SDK, and built a sample app that translates me voice into spoken German. <a href="https://t.co/Bg4XDvhBjv">pic.twitter.com/Bg4XDvhBjv</a></p>&mdash; Jim Bennett ☁️ (@jimbobbennett) <a href="https://twitter.com/jimbobbennett/status/1035559022743760896?ref_src=twsrc%5Etfw">August 31, 2018</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script> 


<hr/>

In these three posts you have seen how to [create a binding library for the Speech SDK `aar`](/blogs/binding-the-cognitive-services-android-speech-sdk), make the code [more C#-like](/blogs/binding-the-cognitive-services-android-speech-sdk-part-2-making-the-code-more-c-like), then finally use it from a client app, working around a Java bytecode issue. You can check out my implementation and a sample at on [GitHub](https://github.com/jimbobbennett/SpeechSdkXamarinSample). As always, the best source of information with much more depth is the [java binding dos on docs.microsoft.com](https://docs.microsoft.com/xamarin/android/platform/binding-java-library/?WT.mc_id=speech-blog-jabenn).

Let me know what you build with this SDK - my DMs are always open on [Twitter](https://twitter.com/jimbobbennett).

