---
author: "Jim Bennett"
categories: ["Technology", "pcl", "jimlib", "weak events", "memory leak"]
date: 2014-09-07T08:05:45Z
description: ""
draft: false
slug: "weakevents-in-pcls"
tags: ["Technology", "pcl", "jimlib", "weak events", "memory leak"]
title: "WeakEvents in PCLs"

images:
  - /blogs/weakevents-in-pcls/banner.png
featured_image: banner.png
---


One of the biggest causes of memory leaks I've seen in C# applications is events.  Although C# can't leak in the same way C++ can, it's easy to unintentionally end up with references you weren't expecting - and what a lot of people don't realise or forget is that subscribing to an event holds a reference from the event source to the event target, essentially keeping the target alive.

A simple example is when you have a long lived object:

```cs
public class FooManager
{
	public event EventHandler FooEvent;
}
```

and subscribe from something like a model that is only meant to live for the lifetime of a popup window or other short lived object.

```cs
public class ShortLivedModel
{
	public ShortLivedModel(FooManager fm)
    {
    	fm.FooEvent += FooHandler;
    }
    
    private void FooHandler(object sender, EventArgs args)
    {
    }
}
```

Just by doing this the `FooManager` internally holds a reference to the `FooModel` keeping it alive.  If you create one model each time the window is popped up you can very quickly build up a big leak, especially if the view model holds onto the model, and the view holds onto the view model - that one model keeps a massic object graph alive.

So how do we deal with it?

The best option is to remember to unsubscribe.  But this isn't always easy.  Especially with WPF code there is no simple way to see when a control is closed if it's not a window.  It's also easy to forget, especially in complicated code where the event subscription could be in a base class you don't know about or don't have access to.

There is an easier way - weak events.  These don't hold a reference to the target allowing the target to be GC'd without unsubscribing.  Even better , you can use them in the event implementation making it transparent to the subscriber.  This is quite a standard pattern and Microsoft provides a good implementation of both a [specific](http://msdn.microsoft.com/en-us/library/system.windows.weakeventmanager%28v=vs.110%29.aspx) and [generic](http://msdn.microsoft.com/en-us/library/hh199438%28v=vs.110%29.aspx) weak event manager.  The problem with these is that they don't work for PCL projects - they are too heavily linked to reflection.

Luckily it's not that hard to create your own that is PCL compliant.

The pattern I'm going to use is to change the event implementation to wire the target of the event into the weak event manager, then tell the weak event manager to fire the event when needed.

Lets start with the calling code first, then build up the weak event manager from there.

```cs
public class MyClass
{
    private WeakEventManager _manager = new WeakEventManager();
    
    public event EventHandler MyEvent
    {
        add
        {
            _manager.AddEventHandler("MyEvent", value);
        }
        remove
        {
            _manager.RemoveEventHandler("MyEvent", value);
        }
    }

    protected virtual void void OnMyEvent()
    {
        _manager.HandleEvent(this, EventArgs.Empty, "MyEvent");    
    }
}
```

In the above code we are declaring a `WeakEventManager`, then wiring up the value passed to the add handler for the event to it.  When we want to invoke our event we tell the `WeakEventManager` to invoke the event by name with whatever sender and args we require.

Lets look at the implementation now.  The full code contains thread safety, a static to get one manager per source object and other helpful bits.  The code here is just the basics for brevity.

**First, adding the event handlers.**

```cs
public class WeakEventManager
{
    private readonly Dictionary<string, List<Tuple<WeakReference, MethodInfo>>> _eventHandlers = new Dictionary<string, List<Tuple<WeakReference, MethodInfo>>>();
    
    public void AddEventHandler<TEventArgs>(string eventName, EventHandler<TEventArgs> value)
        where TEventArgs : EventArgs
    {
        BuildEventHandler(eventName, value.Target, value.GetMethodInfo());
    }

    public void AddEventHandler(string eventName, EventHandler value)
    {
        BuildEventHandler(eventName, value.Target, value.GetMethodInfo());
    }

    private void BuildEventHandler(string eventName, object handlerTarget, MethodInfo methodInfo)
    {
        List<Tuple<WeakReference, MethodInfo>> target;
        if (!_eventHandlers.TryGetValue(eventName, out target))
        {
            target = new List<Tuple<WeakReference, MethodInfo>>();
            _eventHandlers.Add(eventName, target);
        }

        target.Add(Tuple.Create(new WeakReference(handlerTarget), methodInfo));
    }
}
```

There are 2 `AddEventHandler` methods to cover events that are of type `EventHandler` and those of type `EventHandler<args>`.  Both route through to the same helper but are needed as they are not convertible.
The code here has a dictionary of a list of handlers and targets to the event name.  Each item in the list contains the `MethodInfo` of the handler (lambdas still have method info so they can be used as the event target) allowing the invocator to call the method, and a weak reference to the target so we know what to call the method on.  The weak reference bit is important here.  We don't want to keep a string reference as that would keep the target alive - the thing we're trying to avoid!
For each call we add the passed in handler and a weak reference to it's target to the list held against the event name.  Notice no type safety with the event names.  There is nothing that validates that the name given is an event on the source object - the manager doesn't even know what the source object is!  This provides to my mind greater flexibility so the manager can also be used as an event broker.

**Next, the event invocator.**

```cs
public void HandleEvent(object sender, object args, string eventName)
{
    var toRaise = new List<Tuple<object, MethodInfo>>();

    List<Tuple<WeakReference, MethodInfo>> target;
    if (_eventHandlers.TryGetValue(eventName, out target))
    {
        foreach (var tuple in target.ToList())
        {
            var o = tuple.Item1.Target;

            if (o == null)
            	target.Remove(tuple);
            else
            	toRaise.Add(Tuple.Create(o, tuple.Item2));
        }
    }

    foreach (var tuple in toRaise)
        tuple.Item2.Invoke(tuple.Item1, new[] {sender, args});
}
```

This code finds the event with the given name in the dictionary, and if it finds it works through the list of handlers.  Each target in the list is evaluated to see if it's null or not.  With a `WeakReference`, the `Target` returns null if it has been GC'd.  There is an `IsAlive` method but this is pretty useless as there is a race condition, it could be GC'd between the call to `IsAlive` and the call to `Target`.  The best way is to get a reference to the target, if the target is null the reference is null and if the target is not null the reference stops it being GC'd until we've finished using it.
If the target is null, we remove the item from the list and carry on.  If it's not null, we store it in a list to invoke at the end.
Once we have all the alive handlers, we loop through them invoking the method on the target.

**Lastly, we need the remove code.**

```cs
public void RemoveEventHandler<TEventArgs>(string eventName, EventHandler<TEventArgs> value)
    where TEventArgs : EventArgs
{
    RemoveEventHandlerImpl(eventName, value.Target, value.GetMethodInfo());
}

public void RemoveEventHandler(string eventName, EventHandler value)
{
    RemoveEventHandlerImpl(eventName, value.Target, value.GetMethodInfo());
}

private void RemoveEventHandlerImpl(string eventName, object handlerTarget, MemberInfo methodInfo)
{
    List<Tuple<WeakReference, MethodInfo>> target;
    if (_eventHandlers.TryGetValue(eventName, out target))
    {
        foreach (var tuple in target.Where(t => t.Item1.Target == handlerTarget &&
            t.Item2.Name == methodInfo.Name).ToList())
            target.Remove(tuple);
    }
}
```

This just loops through the list against the event name and removes the entries for the given target and method name.  This is needed to ensure intentionaly unsubscribing from the events works but as mentioned above is not needed to allow the target to be GC'd.

The full code for this is on [GitHub](https://github.com/jimbobbennett/JimLib/blob/master/JimLib/Events/WeakEventManager.cs) and it's part of the [JimLib NuGet package](https://www.nuget.org/packages/JimBobBennett.JimLib/).

