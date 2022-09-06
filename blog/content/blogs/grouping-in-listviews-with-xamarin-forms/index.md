---
author: "Jim Bennett"
categories: ["Technology", "xamarin", "jimlib", "technology", "xamarin.forms", "ListView"]
date: 2014-08-15T03:38:39Z
description: ""
draft: false
slug: "grouping-in-listviews-with-xamarin-forms"
tags: ["Technology", "xamarin", "jimlib", "technology", "xamarin.forms", "ListView"]
title: "Grouping in ListViews with Xamarin.Forms"

images:
  - /blogs/grouping-in-listviews-with-xamarin-forms/banner.png
featured_image: banner.png
---


Xamarin.Forms provides a lot of cool features to use for mobile app development, and the documentation is pretty good - but sometimes the cool features you want to use are a bit lacking in docs.  There are example projects but it can be hard to interpret what you need to do to get something working.

The latest area that was confusing me was grouping in [ListView](http://iosapi.xamarin.com/?link=T%3aXamarin.Forms.ListView).  There are properties for specifiying the grouping, but no details on the correct way to use it.  After a bit of trial an error, I managed to work out the following:

* Your `ItemsSource` should be a collection of something derived from a collection - each of the inner collection objects is a group (e.g. for people grouped by first initial you would have a maximum of 26 items in your outer collection - each item being a collection of people with the same first initial).
* The `GroupDisplayBinding`	property should be set to a property on the inner collection objects - so rather that have a collection of collections, you need a collection of something derived from collection that adds a property to provide the group name.
* If you want fast scrolling you need to provide the `GroupShortNameBinding` property to bind to the short name (e.g. first letter of a name).
* If you want more magic in the group header, set the `GroupHeaderTemplate` instead of the `GroupDisplayBinding` to have a custom header (setting `GroupDisplayBinding` clears `GroupHeaderTemplate`, so you can only set one or the other).

Here's an example of the kind of classes you can use for the `ItemsSource` property:

```
public class InnerCollection : List<string>
{
	public string Title { get; set; }
}

public class ItemsSourceCollection : List<InnerCollection>
{
}
```

Then use this like so:

```
public class MyPage : ContentPage
{
	public MyPage()
    {
    	var listView = new ListView();
        var items = new ItemsSourceCollection();
        
        listView.ItemsSource = items;
        
        // bind the grouping to the title of the inner collection
        listView.GroupDisplayBinding = new Binding("Title");
    }
}
```

Rather than create this structure each time, [JimLib](https://www.nuget.org/packages/JimBobBennett.JimLib/) contains a handy `ListItemCollection<T>` class to provide all this functionality and more.

