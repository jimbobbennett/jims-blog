---
author: "Jim Bennett"
date: 2016-11-26T00:19:40Z
description: ""
draft: false
slug: "effects-in-xamarin-forms"
title: "Effects in Xamarin.Forms"

images:
  - /blogs/effects-in-xamarin-forms/banner.png
featured_image: banner.png
---


Xamarin.Forms is pretty awesome, it provides an abstraction over the UI layer of iOS, Android and UWP apps allowing you to define you UI once either in code (C# or F#), or using XAML - an XML markup language. Write your UI once and it works natively on all devices rendering your UI using the native controls for each platform.

The upside is write-once UIs, the downside is to make this work you only have access to a subset of the APIs available to each UI control so that the Forms code you write will work on all platforms.

Right from the first version of Forms there was a way around this - custom rendered. Forms uses a renderer for each UI control - a native class that takes the Forms element and renders it using a native control. For example if you have a forms `Button`, the iOS renderer will put a `UIKit.UIButton` on the screen, the Android renderer will use an `Android.Widget.Button`. If you wanted to change the way the controls were rendered you could subclass the renderer and add any feature you wanted.

This is good, but is a bit heavyweight if all you want to do is a single property change, and falls down if you want to apply this same property change to multiple elements (you end up writing multiple renderers, one for each element).

Luckily Xamarin Forms has introduced a new technique - [effects](https://developer.xamarin.com/guides/xamarin-forms/effects/introduction/). This are classes that you can attach to any Xamarin Forms view, and they can manipulate the Forms element or underlying control in any way you want.

To create an effect you have to write a number of classes - a cross-platform `RoutingEffect` class, and a `PlatformEffect` for each platform you want to support.

As an example lets create an effect to capitalize the keyboard for an `Entry` control.

First we create the cross-platform `RoutingEffect` in our PCL:

```
namespace Organon.XForms.Effects
{
  public class CapitalizeKeyboardEffect : RoutingEffect
  {
    public CapitalizeKeyboardEffect() :
      base("Organon.Effects.CapitalizeKeyboardEffect")
    {
    }
  }
}
```

This class derives from `RoutingEffect`, is named using <something>Effect, and passes a `string` to the base constructor. This string is used to route the effect to the relevant platform specific implementation.

To write the iOS implementation we need to derive from `PlatformEffect`:

```
[assembly: ResolutionGroupName("Organon.Effects")]
[assembly: ExportEffect(typeof(CapitalizeKeyboardEffect), nameof(CapitalizeKeyboardEffect))]

namespace Organon.XForms.Effects.iOS.Effects
{
    [Preserve(AllMembers = true)]
	public class CapitalizeKeyboardEffect : PlatformEffect
	{
		protected override void OnAttached()
		{
            var editText = Control as UITextField;
			if (editText != null)
                editText.AutocapitalizationType = UITextAutocapitalizationType.AllCharacters;
		}

		protected override void OnDetached()
		{
		}
	}
}
```

This class has 2 methods we need to implement - `OnAttached` which is called when the effect is attached to a Forms view, and `OnDetached` when the effect is detached. You update the native control by accessing the `Control` property (this is a `UIView` on iOS and `View` on Android) and setting it up as needed in `OnAttached`, then revert your changes in `OnDetached`. You can also access the Forms element if needed via the `Element` property. In this example we're checking that the `Control` is a `UITextField`, and if set setting the auto caps to capitalize everything. We could then write something similar in Android.

To use this effect you add it to the `Effects` collection on your Forms control:

```
<Entry Placeholder="start typing..." VerticalOptions="Start">
  <Entry.Effects>
   <effects:CapitalizeKeyboardEffect />
  </Entry.Effects>
</Entry>
```

You can see a couple of effects including this one here:
![Clear entry and capitalize keyboard effects](ClearEntryAndAllCaps_thumb.gif)

I've been working with a few awesome people on creating an open source library of effects. It's currently on [GitHub](https://github.com/OrganonKit/Organon) under the name 'OrganonKit', but is about to be renamed - watch this space for more details plus info on when it will be available as a nuget package.

