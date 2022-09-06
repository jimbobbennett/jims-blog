---
author: "Jim Bennett"
categories: ["Technology", "xamarin", "xamarin.ios", "technology", "xamarin.forms", "timers"]
date: 2015-03-07T15:22:21Z
description: ""
draft: false
slug: "timers-backgrounding"
tags: ["Technology", "xamarin", "xamarin.ios", "technology", "xamarin.forms", "timers"]
title: "Device.StartTimer and iOS backgrounding"

images:
  - /blogs/timers-backgrounding/banner.png
featured_image: banner.png
---


I recently completed a lecture on backgrounding in iOS and Android as part of the [Xamarin University](https://university.xamarin.com).  During this lecture, one topic of discussion came up with no real answer - how `Device.StartTimer()` in Xamarin.Forms affects backgrounding.  With iOS, if you enable backgrounding using `BeginBackgroundTask()`, you have 3 minutes to stop all background tasks before the OS kills your app, so I was wondering what would happen if you create a timer using Xamarin.Forms and background the app - will the timer continue or stop.

So I did a little experimenting.  I created a new Forms solution, deleting the 'droid project' (it would be great to have some more project/solution types available such as forms apps for one platform).  I then added the code to enable backgrounding, but commented it out:

```cs
public override bool FinishedLaunching (UIApplication app, NSDictionary options)
{
	global::Xamarin.Forms.Forms.Init ();
	LoadApplication (new App ());
    //UIApplication.SharedApplication.BeginBackgroundTask(() => {});
	return base.FinishedLaunching (app, options);
}
```

Then I added a timer to my Forms app:

```cs
public App ()
{
	MainPage = new ContentPage 
	{
		Content = new StackLayout 
		{
			VerticalOptions = LayoutOptions.Center,
			Children = 
			{
				new Label 
				{
					XAlign = TextAlignment.Center,
					Text = "Welcome to Xamarin Forms!"
				}
			}
		}
	};

	Device.StartTimer(TimeSpan.FromSeconds(5), () =>
		{
			Debug.WriteLine("Timer tick");
			return true;
		});
}
```

The timer just logs to the console every 5 seconds so  I can see that it is running.

When I tested this out, all was as expected.  I open the app, I see the timer ticks, I background the app, the timer stops ticking, I restore the app and ticks resume.

I then uncommented the code to enable backgrounding and tried again.  The result is as I expected/feared - the timer ticks, I background the app, it **still** ticks.  After 3 minutes, bang!  iOS kills the app.

So be wary - if you are using platform specific iOS code to do backgrounding beware of any Forms timers.  Remember to stop them when the app is backgrounded and restart them once it is restored.

The sample code for this is on [my GitHub repo](https://github.com/jimbobbennett/DeviceStartTimerTest).

