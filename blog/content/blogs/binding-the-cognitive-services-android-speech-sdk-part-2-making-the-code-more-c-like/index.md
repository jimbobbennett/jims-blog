---
author: "Jim Bennett"
categories: ["Technology", "xamarin", "xamarin.android", "java", "binding", "aar", "jar"]
date: 2018-09-10T11:22:44Z
description: ""
draft: false
slug: "binding-the-cognitive-services-android-speech-sdk-part-2-making-the-code-more-c-like"
tags: ["Technology", "xamarin", "xamarin.android", "java", "binding", "aar", "jar"]
title: "Binding the Cognitive Services Android Speech SDK - Part 2, making the code more C#-like"

images:
  - /blogs/binding-the-cognitive-services-android-speech-sdk-part-2-making-the-code-more-c-like/banner.png
featured_image: banner.png
---


In the [first part](/blogs/binding-the-cognitive-services-android-speech-sdk) of this post, I showed how to get started binding the [Microsoft Cognitive Services speech API](https://docs.microsoft.com/azure/cognitive-services/speech-service/?WT.mc_id=speech-blog-jabenn). In this part I show how to make the code look more C#-like. In the [third part](/blogs/binding-the-cognitive-services-android-speech-sdk-part-3-java-8-fun) I'll show how to use it and fix up a nasty issue with the Android compiler and using jars created with the latest versions of Java.

## Making the namespaces more C#-like

The namespaces that come from Java are different from traditional C# style namespaces. Java namespaces are reverse-URL format, so the default one created for this project is `Com.Microsoft.Cognitiveservices.Speech.Internal`. A more-C# like one wouldn't have the `Com` at the start. The default namespace also capitalizes the first letter of each part, but obviously doesn't know what other letters should be capitalized - in this case the `S` in `CognitiveServices`.

The namespaces can be fixed by another `attr` entry in the `Metadata.xml` file - this time with the `name` set to `managedName`  and the path set to the namespace. You will need one `attr` node for every namespace inside the Java library - so for `com.microsoft.cognitiveservices.speech` as well as the `internal`, `util`, `intent` and `translation` sub-namespaces. Change the namespaces to be more C# like, for example to `Microsoft.Azure.CognitiveServices.Speech.*`.

```xml
<attr path="/api/package[@name='com.microsoft.cognitiveservices.speech']" name="managedName">Microsoft.Azure.CognitiveServices.Speech</attr>
<attr path="/api/package[@name='com.microsoft.cognitiveservices.speech.internal']" name="managedName">Microsoft.Azure.CognitiveServices.Speech.Internal</attr>
<attr path="/api/package[@name='com.microsoft.cognitiveservices.speech.util']" name="managedName">Microsoft.Azure.CognitiveServices.Speech.Util</attr>
<attr path="/api/package[@name='com.microsoft.cognitiveservices.speech.intent']" name="managedName">Microsoft.Azure.CognitiveServices.Speech.Intent</attr>
<attr path="/api/package[@name='com.microsoft.cognitiveservices.speech.translation']" name="managedName">Microsoft.Azure.CognitiveServices.Speech.Translation</attr>
```

Once these namespaces are changed, your code will no longer build as the `StdMapWStringWStringMapIterator` class you added to the `Additions` folder will be using the old namespace, so fix this one up manually. Your code should then now build.

## Handling code with callbacks

The Speech SDK is actually implemented as cross-platform C++ code, with some platform-specific C++ code added to support each platform. This code is than wrapped using [SWIG](http://www.swig.org) to make it available as Java code for Android, C# code for Windows etc.

This model has the problem that events are not implemented as standard Java listeners. If they were, then the binding library would automatically convert them to C# events. Seeing as they are not, you will need to convert them to events manually.

> This is a very specific example for this one library, so it is unlikely that other libraries will need exactly the same code - instead I thought I'd write about it as an example of the kind of thing you may have to do to make the code more C# like.

### How events are implemented in this SDK

In this SDK, events are implemented by passing an object that implements the `IEventHandler` interface to the `AddEventListener` method on a property of type `EventHandlerImpl`. When the event is raised, the `OnEvent` method on the `IEventHandler` interface is called.

For example, in the `SpeechRecognizer` class there is a property called `FinalResultReceived` of type `EventHandlerImpl`, and you subscribe to this 'event' by passing an instance of `IEventHandler` to the `AddEventListener` on this property.

This pattern is not idiomatic C#, and is annoying to use as you will need to declare a class that implements the `IEventHandler` interface just to handle the event.

### Making this code more C#-like

To make this code more C# like, what you can do is:

* Create a generic implementation of `IEventHandler` that raises an event
* Add a C# event to the class has a property of type `EventHandlerImpl`
* Add an instance of the `IEventHandler` implementation to this class, and add this as a listener to the `EventHandlerImpl` property
* In the C# event, explicitly implement the `add` and `remove` methods. In these methods, add or remove the event from the event on the `IEventHandler` implementation
* Hide the `EventHandlerImpl` property from client code by marking it `internal`

### Creating the generic event handler

To create the event handler, add a new class to the `Additions` folder called `EventMapper`. The code for this is:

```cs
class EventMapper<T, T1> : EventMapper, IEventHandler
        where T : class
        where T1 : class
{
    readonly object sender;
    readonly Func<T1, T> argExtractor;
    public EventMapper(object sender, Func<T1, T> argExtractor)
    {
        this.sender = sender;
        this.argExtractor = argExtractor;
    }

    public event EventHandler<EventArgs<T>> EventRaised;
    public void OnEvent(Java.Lang.Object p0, Java.Lang.Object p1)
    {
        EventRaised?.Invoke(sender, new EventArgs<T>(argExtractor(p1 as T1)));
    }
}
```

This is an internal class, so is only available to the binding library. 

This class has two parts - an event and an `argExtractor`. 

The event is a standard C# event using the `EventHander<>` delegate type - so when called it passes the sender as an object and some event arguments that derive from `EventArgs`. The `EventArgs<T>` type is not one that exists in .NET Standard (which I am very surprised about as I've created this so many times, as have others). You will need to implement this yourself, so add a class called `EventArgs` with the code below. This event args class is a simple wrapper for a value that needs to be passed to the event and saves you creating a load of custom event arg classes for each different value type that you want to pass.

```cs
public class EventArgs<T> : EventArgs
{
    public T Value { get; }
    public EventArgs(T value)
    {
        Value = value;
    }
}
```

When events are handled by the SDK, it passes it's own event args implementation containing a value for those args. For example, the `FinalRecognitionResult` event handler on the `SpeechRecogniser` is passed an instance of `SpeechRecognitionResultEventArgs`, containing a `Result` property of type `SpeechRecognitionResult`. These event args don't derive from the standard .NET `EventArgs` class, so you need a way to extract the relevant value and populate that into an `EventArgs` class, and this is what the `argExtractor` does - it takes the SDK args and pulls out the value needed. This is then wrapped in an `EventArgs<T>` and passed to the event invocation.

### Handling an event

In the `SpeechRecogniser` class there is a `FinalRecognitionResult` handler that raises an event passing an instance of `SpeechRecognitionResultEventArgs`, containing a `Result` property of type `SpeechRecognitionResult`. To map this to C#, you would add another part to the `SpeechRecogniser` class:

```cs
public partial class SpeechRecognizer
{
}
```

You would then add a field for the event mapper:

```cs
EventMapper<SpeechRecognitionResult, SpeechRecognitionResultEventArgs> finalResultMapper;
```

Then you add a C# event for the final result:

```cs
public event EventHandler<EventArgs<SpeechRecognitionResult>> FinalResult
{
    add {}
    remove {}
}
```

In the `add` method, if the `EventMapper` hasn't been created yet, you create it and pass it to the `AddEventListener` of the bound handler. When it is created you will need to pass in the `sender` which is passed to the events when invoked, and this is always `this`. You also need to pass in a mapper function to extract the `SpeechRecognitionResult` from the `SpeechRecognitionResultEventArgs`, which can be a simple lambda function to return the `Result` property. Then you subscribe the passed in `value` to the event on the mapper.

```cs
add
{
    if (finalResultMapper == null)
    { 
        finalResultMapper = new EventMapper<SpeechRecognitionResult, SpeechRecognitionResultEventArgs>(sender, e => e.Result);
        finalResultMapper.AddEventListener(handler);
    }
    finalResultMapper.EventRaised += value;
}
```

For the remove function, if the mapper has been created you can unsubscribe the value from the event:

```cs
remove
{
    if (finalResultMapper != null)
        finalResultMapper.EventRaised -= value;
}
```

This is a lot of boilerplate code, so in my version I refactored this into some static methods. You can see these in my [GitHub repo](https://github.com/jimbobbennett/SpeechSdkXamarinSample/blob/master/Microsoft.Azure.CognitiveServices.Speech.Client/Additions/EventMapper.cs). 

### Hiding the original event handler

Now that you have C# style events, it is cleaner to hide the old event handler implementation to stop client code from calling instead of your nice, shiny, C# events. To do this, you can use an `attr` in the `Metadata.xml` file to change the visibility of the properties for the old event handlers to `internal`. Seeing as these are the only places that `IEventHandler` and `EventHandlerImpl` are used, you can also mark these as internal. That way if you leave any `EventHandlerImpl` properties as public, the compiler will give you an error - a great way to ensure you have mapped all the events.

To mark these as internal, grab the paths from the source files in the `obj` folder, and add an `attr` node with the `name` set to `visibility`, and the content of the node set to `internal`. The code below shows this for the `FinalResultReceived` property on the `SpeechRecognizer`, as well as the `IEventHandler` and `EventHandlerImpl` classes. Repeat this for all the event handler properties across all classes.

```xml
<attr path="/api/package[@name='com.microsoft.cognitiveservices.speech']/class[@name='SpeechRecognizer']/field[@name='FinalResultReceived']" name="visibility">internal</attr>

<attr path="/api/package[@name='com.microsoft.cognitiveservices.speech.util']/class[@name='EventHandlerImpl']" name="visibility">internal</attr>
<attr path="/api/package[@name='com.microsoft.cognitiveservices.speech.util']/class[@name='IEventHandler']" name="visibility">internal</attr>
```

<hr/>

In the [final part](/blogs/binding-the-cognitive-services-android-speech-sdk-part-3-java-8-fun), I'll show how you can call this code from a client app, as well as fixing up a nasty issue with the Android compiler and using jars created with the latest versions of Java. You can find the code for this [in my GitHub](https://github.com/jimbobbennett/SpeechSdkXamarinSample), and you can read more on [docs.microsoft.com](https://docs.microsoft.com/xamarin/android/platform/binding-java-library/?WT.mc_id=speech-blog-jabenn)

