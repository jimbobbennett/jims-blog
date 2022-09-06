---
author: "Jim Bennett"
categories: ["Technology", "xamarin", "xamarin.ios", "technology", "xamarin.forms", "jimlib.xamarin", "orientation", "portrait", "landscape"]
date: 2014-10-10T03:52:28Z
description: ""
draft: false
slug: "orientation-with-xamarin-forms"
tags: ["Technology", "xamarin", "xamarin.ios", "technology", "xamarin.forms", "jimlib.xamarin", "orientation", "portrait", "landscape"]
title: "Orientation with Xamarin.Forms"

images:
  - /blogs/orientation-with-xamarin-forms/banner.png
featured_image: banner.png
---


Xamarin.Forms is a great cross platform development tool when it works, but being cross platform it suffers from a sever lack of features.  Some of these are understandable as they are different on each platform so it's hard to provide a consistent experience for the developer.  Some are bad ommisions as they are vital to all platforms.

The current ommission I'm working on is Orientation.  I have yet to see a device that is square.  Every device has two orientations, portrait and landscape and a lot of apps change their UI depending on which orientation is in use.

![Portrait or landscape](bg_13761402694716.jpg)

Out of the box, Xamarin.Forms just provides one content for your page, so if you want to change it based on the device orientation you can't.  Some views will handle changes for you - GridView from the Xamarin.Forms.Labs toolkit changes the number of items across based on the orientation, contols will resize based on the available space - but nothing allows a completly different control layout.

So I've decided to roll my own.  I have my own `BaseContentPage` class derived from `ContentPage` to provide some consistent UI features like an activity spinner and services to the ViewModel, and I've extended this to include orientation helpers.  This is just iOS only for now (if anyone wants to send me a free Xamarin.Andriod business license and Android phone I'll gladly update it to do 'droid as well :) )

First I had to create a new renderer for the page to provide information on the orientation and notification of changes.

```cs
[assembly: ExportRenderer(typeof(BaseContentPage), typeof(BaseContentPageRenderer))]

namespace JimBobBennett.JimLib.Xamarin.ios.Views
{
    public class BaseContentPageRenderer : PageRenderer
    {
        protected override void OnElementChanged(VisualElementChangedEventArgs e)
        {
            base.OnElementChanged(e);
            ((BaseContentPage) Element).Appearing += (s, e1) => SetOrientation();
            SetOrientation();
        }

        public override void DidRotate(UIInterfaceOrientation fromInterfaceOrientation)
        {
            base.DidRotate(fromInterfaceOrientation);
            SetOrientation();
        }

        private void SetOrientation()
        {
            ((BaseContentPage) Element).OrientationChanged(InterfaceOrientation.GetOrientation());
        }
    }
}
```

This render calls the `OrientationChanged` method on the `BaseContentPage` on creation, on appearing and whenever the orientation is changed by overriding the `DidRotate` method on the Page renderer.  The `InterfaceOrientation.GetOrientation()` extension method is my own and converts the iOS `UIInterfaceOrientation` enum into my own `Orientation` enum to allow it to not be platform specific.

In my `BaseContentPage` I've defined two properties, `PortraitContent` and `LandscapeContent`, both of type view.  I've also changed the default property to be `PortraitContent`, so when the content is set in XAML it sets the `PortraitContent` property instead of the `Content` property.  This is done using the `ContentProperty` attribute, same as in WPF.

```cs
[ContentProperty("PortraitContent")]
```

Internally in my page I set the `Content` to be a number of views to support my functionality, so when this property is set externally I route the value to a child of one of my grids and reset the content back to the required views.  I enhanced this to pass the content to the `PortraitContent` property to any C# code that sets this will still work.
To make the magic happen on orientation change I implemented the `OrientationChanged` method to set either the only content available if only one value is set, or to set the content depending on the orientation.  

```cs
if (_portraitContent == null && _landscapeContent == null)
{
    // do nothing
}
else if (_portraitContent != null && _landscapeContent == null)
{
    _contentGrid.Children.Clear();
    _contentGrid.Children.Add(_portraitContent);
}
else if (_portraitContent == null && _landscapeContent != null)
{
    _contentGrid.Children.Clear();
    _contentGrid.Children.Add(_landscapeContent);
}
else
{
    _contentGrid.Children.Clear();
    _contentGrid.Children.Add(Orientation == Orientation.Landscape ? _landscapeContent : _portraitContent);
}
```

This works well except for one problem.  This takes effect after the orientation is changed.  What happens is:

* Orientation is changed
* Screen rotates
* Xamarin.Forms re-lays out the controls based on the new orientaion
* Content is changed

It looks a bit rubbish as the user sees the portrait content laid out in landscape first before the landscape content is shown.  Easy fix though - remove the content before the change, then add the new one after.  This can be detected in the rendereer by overriding `WillRotate`.

```cs
public override void WillRotate(UIInterfaceOrientation toInterfaceOrientation, double duration)
{
    base.WillRotate(toInterfaceOrientation, duration);
    ((BaseContentPage)Element).OrientationChanging();
}
```

```cs
protected internal virtual void OrientationChanging()
{
    _contentGrid.Children.Clear();
}
```

Much nicer.

The only bug I'm left with now that I have yet to fix is for images.  I have an image in both my portrait and landscape views that uses the same image source.  When changing a few times sometimes the portrait image is blank.  I've tried raising property changes to fix it but no dice.  Once I fix it (or more realistically work round it as it looks like a Xamarin bug) I'll update this post with the details.

All the code for this is available on [in JimLib.Xamarin on GitHub](https://github.com/jimbobbennett/JimLib.Xamarin).

