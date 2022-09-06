---
author: "Jim Bennett"
categories: ["Technology", "xamarin", "xamarin.ios", "technology", "xamarin.forms", "jimlib.xamarin", "pull to refresh", "scrollview"]
date: 2014-09-28T08:38:16Z
description: ""
draft: false
slug: "ios-pull-to-refresh-without-using-a-uitableview"
tags: ["Technology", "xamarin", "xamarin.ios", "technology", "xamarin.forms", "jimlib.xamarin", "pull to refresh", "scrollview"]
title: "iOS pull to refresh without using a UITableView"

images:
  - /blogs/ios-pull-to-refresh-without-using-a-uitableview/banner.png
featured_image: banner.png
---


I've been working on the UI for my current app, trying to make some usability improvements.  The main screen is a list of data containing an image and some text.  Although this is a standard UI pattern, the problem I'm having with it is one of size.  List rows are usually short and full width.  For text this is fine, but not so good for images, then end up being small and not very easy to see.  For the data I'm showing the image is just as important as the text, if not more so for quick identification of the data.  I's also wasting a lot of space as there number of rows will be very small most of the time, probably only one or 2 rows.
To improve this I've decided to move to a grid like layout, with varying columns depending on if the view is portrait or landscape.  The end result is much nicer to look at and use, but coding it up let to a problem.

I was using a derivative of the Xamarin.Forms `ListView` class with support for pull to refresh courtesy of [James Montemagno's blog](http://motzcod.es/post/87917979362/pull-to-refresh-for-xamarin-forms-ios).  This provides a Xamarin wrapper around the well known `UIRefreshControl` and tying it to a `UITableView`.
This is all great, until you change from a `ListView` to something else, in my case a custom generated grid view.

Luckily, `UIScrollView` also supports pull to refresh, just it's not as well documented.  It has to be a `UIScrollView` or derivative, not any other control as it needs the pull down bounce to trigger the refresh.

To implement it in my grid view I first created a `PullToRefreshScrollView` and associated renderer to host my grid.
The code for the view lives in my portable project and just defines some bindable properties for the command to execute when refreshing, a flag to turn on the refresh indicator and a refresh message.  All lifted directly from James's [PullToRefreshListView](https://github.com/jamesmontemagno/Xamarin.Forms-PullToRefreshListView/blob/master/PullToRefresh/PullToRefreshListView.cs).

```cs
public class PullToRefreshScrollView : ScrollView
{
    public static readonly BindableProperty IsRefreshingProperty =
        BindableProperty.Create<PullToRefreshScrollView, bool>(p => p.IsRefreshing, false);

    public static readonly BindableProperty RefreshCommandProperty =
        BindableProperty.Create<PullToRefreshScrollView, ICommand>(p => p.RefreshCommand, null);

    public static readonly BindableProperty MessageProperty =
        BindableProperty.Create<PullToRefreshScrollView, string>(p => p.Message, string.Empty);

    public bool IsRefreshing
    {
        get { return (bool)GetValue(IsRefreshingProperty); }
        set { SetValue(IsRefreshingProperty, value); }
    }

    public ICommand RefreshCommand
    {
        get { return (ICommand)GetValue(RefreshCommandProperty); }
        set { SetValue(RefreshCommandProperty, value); }
    }

    public string Message
    {
        get { return (string)GetValue(MessageProperty); }
        set { SetValue(MessageProperty, value); }
    }
}
```

The next bit is a wrapper for the `UIRefreshControl` - again lifted from the [same place](https://github.com/jamesmontemagno/Xamarin.Forms-PullToRefreshListView/blob/master/iOS/Renderers/FormsUIRefreshControl.cs) and put into my iOS project.

```cs
public class FormsUIRefreshControl : UIRefreshControl
{
	public FormsUIRefreshControl()
	{
		ValueChanged += (sender, e) => 
		{
			var command = RefreshCommand;
			if(command  == null)
				return;

			command.Execute(null);
		};
	}

	private string _message;

	public string Message 
	{ 
		get { return _message;}
		set 
		{ 
			_message = value;
			if (string.IsNullOrWhiteSpace (_message))
				return;

			AttributedTitle = new MonoTouch.Foundation.NSAttributedString(_message);
		}
	}

	private bool _isRefreshing;

	public bool IsRefreshing
	{
		get { return _isRefreshing;}
		set
		{ 
			_isRefreshing = value; 
			if (_isRefreshing)
				BeginRefreshing();
			else
				EndRefreshing();
		}
	}

    public ICommand RefreshCommand { get; set; }
}
```

Finally the renderer.  To create the refresh control in the scroll view, it's a simple case of creating the `UIRefreshControl` and adding it as a subview of the `UIScrollView`.  When you pull the scroll view down it will trigger a ValueChange event on the `UIRefreshControl`, which our `FormsUIRefreshControl` handles to execute the provided command.
Now for the gotcha - the refresh only happens when you pull the scroll view down far enough.  If the contents of the scroll view is smaller than the available space then it won't scroll in either direction, stopping the pull action from doing anything.  Good news is we can make the scroll view always scroll by setting:
```cs
AlwaysBounceVertical = true;
```

Here's the full code for the renderer:
```cs
public class PullToRefreshScrollViewRenderer : ScrollViewRenderer
{
    private FormsUIRefreshControl _refreshControl;

    protected override void OnElementChanged(VisualElementChangedEventArgs e)
    {
        base.OnElementChanged(e);

        if (_refreshControl != null)
            return;

        var pullToRefreshScrollView = (PullToRefreshScrollView)Element;
        pullToRefreshScrollView.PropertyChanged += OnElementPropertyChanged;

        _refreshControl = new FormsUIRefreshControl
        {
            RefreshCommand = pullToRefreshScrollView.RefreshCommand,
            Message = pullToRefreshScrollView.Message
        };

        AlwaysBounceVertical = true;

        AddSubview(_refreshControl);
    }

    private void OnElementPropertyChanged(object sender, System.ComponentModel.PropertyChangedEventArgs e)
    {
        var pullToRefreshScrollView = Element as PullToRefreshScrollView;
        if (pullToRefreshScrollView == null)
            return;

        if (e.PropertyName == PullToRefreshScrollView.IsRefreshingProperty.PropertyName)
            _refreshControl.IsRefreshing = pullToRefreshScrollView.IsRefreshing;
        else if (e.PropertyName == PullToRefreshScrollView.MessageProperty.PropertyName)
            _refreshControl.Message = pullToRefreshScrollView.Message;
        else if (e.PropertyName == PullToRefreshScrollView.RefreshCommandProperty.PropertyName)
            _refreshControl.RefreshCommand = pullToRefreshScrollView.RefreshCommand;
    }
}
```

This control is now part of [JimLib.Xamarin, available on GitHub](Xamarin).

