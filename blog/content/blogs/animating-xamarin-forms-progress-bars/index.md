---
author: "Jim Bennett"
categories: ["xamarin", "xamarin.forms", "Technology", "UI", "animation"]
date: 2017-01-05T08:43:11Z
description: ""
draft: false
slug: "animating-xamarin-forms-progress-bars"
tags: ["xamarin", "xamarin.forms", "Technology", "UI", "animation"]
title: "Animating Xamarin Forms progress bars"

images:
  - /blogs/animating-xamarin-forms-progress-bars/banner.png
featured_image: banner.png
---


Don't you just hate boring UIs? With no animations to bring them to life?

Me too! Especially progress bars - they increment or decrement instantly giving a dull UI.

<div class="image-div" style="max-width: 300px;"> 
    
![Boring unanimated progress bar](Progress-1.gif)
    
</div>

As you can see from the image above, as the progress bar changes value, the UI updates instantly and it looks a bit dull. What would be nicer is if the progress bar smoothly animated its progress.

Out of the box Xamarin.Forms provides a method to do this - an extension method called `ProgressTo`. You can call this code from inside your UI to smoothly animate the progress value to whatever value you like. This is great, but it's not ideal as it relies on the animation happening in the view, so the view needs to know what the value is to animate to. I'm a big fan of MVVM (true - I even [written a book on how to use MVVM to build Xamarin apps](http://xam.jbb.io)). The progress value should be in a view model, but then we'd have to wire up a number of UI components to watch view models for changes then start the animation. Ideally it would be better to have a bindable property that we could use to trigger this animation.

We could get this bindable property by creating our own control derived from ProgressBar that has a property for the animation, but that involves a custom control. What would be even better is if we could use the existing progress bar and somehow add a property to it that we can bind to and when the value changes the progress animates to the new value. Happily for us, Xamarin Forms supports this in the form of [Attached Properties](https://docs.microsoft.com/en-gb/xamarin/xamarin-forms/xaml/attached-properties/?WT.mc_id=formsanimations-blog-jabenn).

Attached properties are bindable properties, just like the ones you would create in your own controls, except that they can be 'attached' to any other control. You define them on one class, and attach them to another. Using these we can create a property on a utility class that is attached to `ProgressBar`. These properties don't directly change anything on the class they are attached to, instead you can hook into the property change mechanism to do whatever you need to do.

For example, if we wanted an animated progress bar we could create a new attached property called `AnimatedProgress` attached to `ProgressBar`, and every time the value changes we could tell the progress bar to change it's progress value via the `ProgressTo` extension method:

```
public static class AttachedProperties
{
   public static BindableProperty AnimatedProgressProperty =
      BindableProperty.CreateAttached("AnimatedProgress",
                                      typeof(double),
                                      typeof(ProgressBar),
                                      0.0d,
                                      BindingMode.OneWay,
                                      propertyChanged: (b, o, n) => 
                                      ProgressBarProgressChanged((ProgressBar)b, (double)n));

   private static void ProgressBarProgressChanged(ProgressBar progressBar, double progress)
   {
      ViewExtensions.CancelAnimations(progressBar);
      progressBar.ProgressTo((double)progress, 800, Easing.SinOut);
   }
}
```

In this code we are defining a static helper class with the static attached property. This property is called `"AnimatedProgress"`, has a `double` value, is attached to `ProgressBar`, has a default value of `0.0`. It defaults to bind one way, and this is fine as users cannot interact with a progress bar to change this value. The cool part is the `propertyChanged` action, this calls a method that animates the progress bar to the new value every time it changes.

Once we've defined this property we can attach it to any progress bar we want, using XAML or code behind. The XAML way to set it is:

```
?xml version="1.0" encoding="utf-8"?>
<ContentPage xmlns="http://xamarin.com/schemas/2014/forms"
	   		 xmlns:x="http://schemas.microsoft.com/winfx/2009/xaml"
			 xmlns:local="clr-namespace:AnimatedProgress"
			 x:Class="AnimatedProgress.AnimatedProgressPage">
	<StackLayout Padding="20,100" Spacing="40">
		<ProgressBar local:AttachedProperties.AnimatedProgress="{Binding Progress}"/>
		<Entry Text="{Binding ProgressPercent}"/>
	</StackLayout>
</ContentPage>
```

In this XAML we define the `local` XML namespace pointing to our local C# namespace, then bind the property using `local:AttachedProperties.AnimatedProgress="{Binding Progress}"`. This code assumes you have a view model for the page with a property called `Progress`.

You can also set this in code:

```
MyProgressBar.SetBinding(AttachedProperties.AnimatedProgressProperty,
                                  "Progress");
```

Once this is wired up we get a lovely animation when we change our progress!

![Nice, shiny animated progress changing](AnimatedProgress-1.gif)

You can find the code for this post on my [GitHub Repo](https://github.com/jimbobbennett/AnimatedProgress).

